import numpy as np
import matplotlib.pyplot as plt

# Constants
L = 1

# Input energy level
n = int(input("Enter the energy level (n): "))

# Define functions
def P(x):
    """Probability density function derived from psi(x)."""
    psi = np.sqrt(2 / L) * np.sin(n * np.pi * x / L)  # psi(x)
    return psi**2  # P(x)

def Q(x):
    """Proposal uniform distribution."""
    return np.sqrt(2 / L)

# Number of samples
N = 100000

# Metropolis-Hastings sampling
x = np.zeros(N)
i = 0
while i < N:
    # Generate a sample from the proposal distribution
    x1 = np.random.rand()  # Uniform distribution in [0, 1]
    
    # Calculate acceptance ratio
    accept_ratio = P(x1) / Q(x1)
    
    # Generate a random number for acceptance/rejection
    u = np.random.rand()
    
    # Accept or reject the sample
    if u <= accept_ratio:
        x[i] = x1
        i += 1

# Plot histogram of generated samples
plt.hist(x, bins=100, density=True, alpha=0.75, label="Sampled Distribution")
plt.xlabel("x")
plt.ylabel("Probability Density")
plt.title("Histogram of Generated Samples")
plt.legend()
plt.grid(True)
plt.show()
