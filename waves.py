import numpy as np
import matplotlib.pyplot as plt

# Input amplitudes
A = np.array(list(map(float, input("Enter the amplitudes of the harmonics (space-separated): ").split())))
n = len(A)  # Number of harmonics

# Display wave type options
print("Choose the type of wave:")
print("1 - Traditional wave")
print("2 - Triangular wave")
print("3 - Square wave")
print("4 - Sawtooth wave")
option = int(input(""))

t = np.linspace(0, np.pi, 1000)

# Wave calculation
y = np.zeros_like(t)
if option == 1:
    for i in range(1, n + 1):
        y += A[i - 1] * np.sin(2 * np.pi * i * t)
    title = "Resulting wave from the sum of sinusoidal harmonics"
elif option == 2:
    for i in range(1, n + 1):
        if i % 2 == 1:  # Include only odd harmonics
            y += (8 / np.pi**2) * ((-1)**((i - 1) // 2) / (i**2)) * np.sin(2 * np.pi * i * t)
    title = "Resulting triangular wave"
elif option == 3:
    for i in range(1, n + 1):
        k = 2 * i - 1  # Odd harmonic order
        y += A[i - 1] * np.sin(2 * np.pi * k * t) / k
    title = "Resulting square wave"
elif option == 4:
    for i in range(1, n + 1):
        y += (1 / (2 * i * np.pi)) * np.sin(2 * np.pi * i * t)
    title = "Resulting sawtooth wave"
else:
    print("Invalid option!")
    exit()

# Plot the result
plt.plot(t, y)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title(title)
plt.grid(True)
plt.show()