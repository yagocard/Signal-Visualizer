import numpy as np
import matplotlib.pyplot as plt

def get_phase(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a number.")

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a number.")


def get_positive_float(prompt):
    while True:
        value = get_float(prompt)

        if value > 0:
            return value

        print("Value must be greater than zero.")


def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value > 1:
                return value

            print("Sample number must be greater than one.")

        except ValueError:
            print("Invalid input! Please enter an integer.")


def continuous_signal():
    amplitude = get_float("Enter amplitude [V]: ")
    frequency = get_positive_float("Enter frequency [Hz]: ")
    duration = get_positive_float("Enter duration [s]: ")
    sampling_frequency = get_positive_float("Enter sampling frequency [Hz]: ")
    phase_deg = get_phase("Enter phase [deg]: ")
    phase_rad = np.deg2rad(phase_deg)

    t = np.arange(0, duration, 1 / sampling_frequency)
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase_rad)

    plt.plot(t, signal)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude [V]")
    plt.title("Continuous-Time Sine Wave")
    plt.grid(True)
    plt.show()


def discrete_signal():
    amplitude = get_float("Enter amplitude [V]: ")
    omega = get_float("Enter angular frequency [rad/sample]: ")
    sample_number = get_positive_integer("Enter sample number [n]: ")
    phase_deg = get_phase("Enter phase [deg]: ")
    phase_rad = np.deg2rad(phase_deg)

    n = np.arange(sample_number)
    signal = amplitude * np.sin((omega * n)+ phase_rad)

    plt.stem(n, signal)
    plt.xlabel("Sample index [n]")
    plt.ylabel("Amplitude [V]")
    plt.title("Discrete-Time Sine Wave")
    plt.grid(True)
    plt.show()


def main():
    signal_type = input("Continuous or discrete? (c/d): ").strip().lower()

    if signal_type == "c":
        continuous_signal()

    elif signal_type == "d":
        discrete_signal()

    else:
        print("Invalid signal type! Please enter 'c' or 'd'.")


if __name__ == "__main__":
    main()