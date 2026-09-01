#!/usr/bin/env bash

extract_block() {
    local file="$1"
    local label="$2"
    awk -v label="$label" '
        !found && index($0, "# %% " label) == 1 { found=1; next }
        found && $0 ~ /^# %%/ { exit }
        found { print }
        END { if (!found) exit 1 }
    ' "$file"
}

mkdir -p docs_to_render

for qmd in docs/*.qmd; do
    [[ -f "$qmd" ]] || continue
    [[ "$qmd" == *.release.qmd ]] && continue

    release="docs_to_render/$(basename "${qmd%.qmd}").qmd"

    frontmatter_state=0
    global_code_file=""

    inside_python=0
    block_code_file=""
    code_block_label=""
    buffer=()

    while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
        line="${raw_line%$'\r'}"

        # --- Frontmatter detection ---
        if [[ "$line" == '---' ]]; then
            if (( frontmatter_state == 0 )); then
                frontmatter_state=1
                printf '%s\n' "$line"
                continue
            elif (( frontmatter_state == 1 )); then
                frontmatter_state=2
                printf '%s\n' "$line"
                continue
            fi
        fi

        if (( frontmatter_state == 1 )); then
            if [[ "$line" =~ ^code-file:[[:space:]]*(.*)$ ]]; then
                global_code_file="${BASH_REMATCH[1]}"
                global_code_file="${global_code_file%"${global_code_file##*[![:space:]]}"}"
                continue
            fi
            printf '%s\n' "$line"
            continue
        fi

        # --- Normal body processing ---
        if (( inside_python == 0 )) && [[ "$line" == '```{python}' ]]; then
            inside_python=1
            block_code_file=""
            code_block_label=""
            buffer=()
            printf '%s\n' "$line"
            continue
        fi

        if (( inside_python == 1 )) && [[ "$line" == '```' ]]; then
            active_code_file="${block_code_file:-$global_code_file}"

            if [[ -n "$active_code_file" && -n "$code_block_label" ]]; then
                if [[ ! -f "$active_code_file" ]]; then
                    echo "Error: Referenced file not found: $active_code_file (in $qmd)" >&2
                    inside_python=0
                    printf '%s\n' "$line"
                    continue
                fi

                extracted=$(extract_block "$active_code_file" "$code_block_label")
                if [[ $? -ne 0 ]]; then
                    echo "Error: Code block '${code_block_label}' not found in ${active_code_file} (in $qmd)" >&2
                    inside_python=0
                    printf '%s\n' "$line"
                    continue
                fi

                for b in "${buffer[@]}"; do
                    if [[ "$b" =~ ^#[|][[:space:]]*code-file:[[:space:]]*(.+)$ ]]; then
                        continue
                    elif [[ "$b" =~ ^#[|][[:space:]]*code-block:[[:space:]]*(.+)$ ]]; then
                        printf '#| label: %s\n' "${BASH_REMATCH[1]}"
                    else
                        printf '%s\n' "$b"
                    fi
                done

                if [[ -n "$extracted" ]]; then
                    printf '%s\n' "$extracted"
                fi
            else
                for b in "${buffer[@]}"; do
                    printf '%s\n' "$b"
                done
            fi

            printf '%s\n' "$line"
            inside_python=0
            continue
        fi

        if (( inside_python == 1 )); then
            buffer+=("$line")
            if [[ "$line" =~ ^#[|][[:space:]]*code-file:[[:space:]]*(.+)$ ]]; then
                block_code_file="${BASH_REMATCH[1]}"
            elif [[ "$line" =~ ^#[|][[:space:]]*code-block:[[:space:]]*(.+)$ ]]; then
                code_block_label="${BASH_REMATCH[1]}"
            fi
        else
            printf '%s\n' "$line"
        fi
    done < "$qmd" > "$release"

    echo "Generated: $release"
done
