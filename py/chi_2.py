# %% imports
import math

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


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
print(df)

# Generate 5,000 samples for 4 degrees of freedom
my_samples = generate_chi_square_samples(df=df, num_samples=5000)
my_samples

# %%
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


# start snippet main
def main():
    print("It works!")


# end snippet main
