# %% imports
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

from py.helper import helper


# %% generate_chi_square_samples
def generate_chi_square_samples(df, num_samples):
    chi_square_data = []
    for _ in range(num_samples):
        # 1. Generate 'df' independent standard normal values (Mean=0, Std=1)
        normal_samples = np.random.normal(loc=0.0, scale=1.0, size=df)

        # 2. Square each value and sum them up
        chi_square_value = np.sum(normal_samples**2)

        chi_square_data.append(chi_square_value)

    return np.array(chi_square_data)


df = 4

# Generate 5,000 samples for 4 degrees of freedom
my_samples = generate_chi_square_samples(df=df, num_samples=5000)
my_samples

# %% plot_hist
# 1. Plot the histogram of your generated samples

plt.hist(
    my_samples,
    bins=50,
    density=True,
    alpha=0.6,
    color="skyblue",
    edgecolor="black",
    label="Simulated Data",
)

# 2. Overlay the ideal theoretical Chi-Square curve
x = np.linspace(0, max(my_samples), 1000)
plt.plot(
    x,
    stats.chi2.pdf(x, df=df),
    color="red",
    linewidth=2,
    label="Theoretical Curve (df=4)",
)

# 3. Add labels and legend
plt.title("Chi-Square Distribution Simulation")
plt.xlabel("Value")
plt.ylabel("Probability Density")
plt.legend()
plt.grid(True, alpha=0.3)
plt.close()


# %%
# Define the Chi-Square PDF from scratch
def chi_square_pdf_scratch(x, df):
    power_exponent = (df / 2) - 1
    power_term = x**power_exponent
    exp_term = math.exp(-x / 2)

    numerator = power_term * exp_term

    # Step 3: Calculate the components of the denominator
    two_power_term = 2 ** (df / 2)
    gamma_input = df / 2
    gamma_term = math.gamma(gamma_input)

    denominator = two_power_term * gamma_term

    result = numerator / denominator

    return result


# Vectorize the function so it can accept NumPy arrays of x-values
chi_square_pdf_vectorized = np.vectorize(chi_square_pdf_scratch)

# Generate custom line points
df_value = 4
x_axis = np.linspace(0.01, 20, 500)
y_axis = chi_square_pdf_vectorized(x_axis, df=df_value)

# %%
# Create the visualization
plt.figure(figsize=(8, 5))
plt.plot(
    x_axis,
    y_axis,
    label=f"Degrees of Freedom (df) = {df_value}",
    color="blue",
    lw=2,
)

# Add styling and labels
plt.title("Chi-Square Distribution PDF (From Scratch)", fontsize=14)
plt.xlabel("x", fontsize=12)
plt.ylabel("Probability Density", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=11)
plt.close()

# %%
# Generate custom line points
x_axis = np.linspace(0.01, 20, 500)
y_axis = chi_square_pdf_vectorized(x_axis, df=4)
