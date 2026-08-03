import numpy as np
import matplotlib.pyplot as plt


def continuous_signal():
    amplitude = float(input("Enter amplitude [V]: "))
    frequency = float(input("Enter frequency [Hz]: "))
    sample_number = int(input("Enter sample number [n]: "))

    t = np.linspace(0, 1 / frequency, sample_number)
    signal = amplitude * np.sin(2 * np.pi * frequency * t)

    plt.plot(t, signal)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Continuous-Time Sine Wave")
    plt.grid(True)
    plt.show()


def discrete_signal():
    amplitude = float(input("Enter amplitude [V]: "))
    omega = float(input("Enter angular frequency [rad/sample]: "))
    sample_number = int(input("Enter sample number [n]: "))

    n = np.arange(sample_number)
    signal = amplitude * np.sin(omega * n)

    plt.stem(n, signal)
    plt.xlabel("n")
    plt.ylabel("Amplitude")
    plt.title("Discrete-Time Sine Wave")
    plt.grid(True)
    plt.show()


def main():
    signal_type = input("Continuous or discrete? (c/d): ").lower()

    if signal_type == "c":
        continuous_signal()

    elif signal_type == "d":
        discrete_signal()

    else:
        print("Invalid signal type!")


if __name__ == "__main__":
    main()