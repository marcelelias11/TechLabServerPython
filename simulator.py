import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

# Abstract Base Class for Simulator
class SimulatorBase:
    def send(self):
        raise NotImplementedError("Subclasses must implement the `send` method.")

# Concrete implementation for Waves
class Waves(SimulatorBase):
    def __init__(self, harmonics: list, option: int):
        self.harm = harmonics
        self.op = option

    def send(self):
        return {"graph": self.__waves()}

    def __waves(self):
        A = np.array(list(map(float, self.harm)))
        n = len(A)  # Number of harmonics
        option = self.op
        t = np.linspace(0, np.pi, 1000)  # Time domain
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
            raise ValueError("Invalid wave option!")

        plt.plot(t, y)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title(title)
        plt.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graph_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()
        return graph_base64

# Concrete implementation for ProbWell
class ProbWell(SimulatorBase):
    __L = 1  # Constants

    def __init__(self, energy: int):
        self.energy = energy

    def send(self):
        return {"graph": self.__prob_well()}

    def __prob_well(self):
        def P(x):
            psi = np.sqrt(2 / self.__L) * np.sin(self.energy * np.pi * x / self.__L)  # psi(x)
            return psi**2  # P(x)

        def Q(x):
            return np.sqrt(2 / self.__L)

        N = 100000
        x = np.zeros(N)
        i = 0
        while i < N:
            x1 = np.random.rand()
            accept_ratio = P(x1) / Q(x1)
            u = np.random.rand()
            if u <= accept_ratio:
                x[i] = x1
                i += 1

        plt.hist(x, bins=100, density=True, alpha=0.75, label="Sampled Distribution")
        plt.xlabel("x")
        plt.ylabel("Probability Density")
        plt.title("Histogram of Generated Samples")
        plt.legend()
        plt.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graph_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()
        return graph_base64

# Factory class to create Simulator instances
class Simulator:
    @staticmethod
    def create_simulator(simulator_type: str, args:dict) -> SimulatorBase:
        if simulator_type == "waves":
            return Waves(args["harmonics"], args["option"])
        elif simulator_type == "prob_well":
            return ProbWell(args["energy"])
        else:
            raise ValueError(f"Unknown simulator type: {simulator_type}")