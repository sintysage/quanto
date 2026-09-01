import os
import pathlib
from dataclasses import dataclass, field

import boto3
from IPython.display import Markdown


@dataclass(frozen=True)
class Helper:
    BUCKET_NAME: str = field(
        default_factory=lambda: str(os.getenv("BUCKET_NAME"))
    )
    AWS_S3_ENDPOINT_URL: str = field(
        default_factory=lambda: str(os.getenv("AWS_S3_ENDPOINT_URL"))
    )
    QUARTO_DOCUMENT_FILE: str = field(
        default_factory=lambda: str(os.getenv("QUARTO_DOCUMENT_FILE"))
    )

    def __post_init__(self):
        object.__setattr__(
            self,
            "SAVE_DIR",
            "artifacts/" + pathlib.Path(self.QUARTO_DOCUMENT_FILE).stem,
        )
        s3_client = boto3.client(
            "s3",
            endpoint_url=self.AWS_S3_ENDPOINT_URL,
        )
        object.__setattr__(self, "s3_client", s3_client)
        try:
            s3_client.list_objects_v2(Bucket=self.BUCKET_NAME)
        except Exception as e:
            print(f"Error connecting to S3: {e}")

    def upload_file(
        self, file_path: str, obj_name: str, content_type: str = "image/png"
    ):
        """Upload a local file to the configured S3 bucket.

        The file is stored under the key ``{SAVE_DIR}/{plot_name}``,
        where ``SAVE_DIR`` is derived from the current Quarto document's filename.

        Args:
            file_path: Path to the local file to upload.
            plot_name: Name to use as the S3 object key (within ``SAVE_DIR``).
            content_type: MIME type to set for the uploaded object.
                Defaults to ``"image/png"``.

        Returns:
            None
        """

        self.s3_client.upload_file(
            Filename=file_path,
            Bucket=self.BUCKET_NAME,
            Key=f"{self.SAVE_DIR}/{obj_name}",
            ExtraArgs={"ContentType": content_type},
        )

        return f"{self.AWS_S3_ENDPOINT_URL}/{self.BUCKET_NAME}/{self.SAVE_DIR}/{obj_name}"

    def upload_visualize(
        self,
        file_path: str,
        obj_name: str,
        content_type: str = "image/png",
        is_preview: bool = False,
    ):
        obj_ref = self.upload_file(file_path, obj_name, content_type)

        if is_preview:
            return Markdown(f"![]({obj_ref}){{.preview-image}}")
        else:
            return Markdown(f"![]({obj_ref})")


helper = Helper()
