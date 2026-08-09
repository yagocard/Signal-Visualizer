import numpy as np
import matplotlib.pyplot as plt

def get_waveform(prompt):
    while True:
        waveform = input(prompt).strip().lower()

        if waveform in ("sine", "cosine", "square", "sawtooth"):
            return waveform

        print("Invalid waveform! Please enter sine, cosine, square, or sawtooth.")
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
    waveform = get_waveform(
        "Select waveform (sine/cosine/square/sawtooth): "
    )
    amplitude = get_float("Enter amplitude [V]: ")
    frequency = get_positive_float("Enter frequency [Hz]: ")
    duration = get_positive_float("Enter duration [s]: ")
    sampling_frequency = get_positive_float("Enter sampling frequency [Hz]: ")
    phase_deg = get_phase("Enter phase [deg]: ")
    phase_rad = np.deg2rad(phase_deg)
    nyquist_rate = 2 * frequency

    if sampling_frequency < nyquist_rate:
        print(
            f"Warning: Nyquist criterion not satisfied! "
            f"Sampling frequency should be at least {nyquist_rate} Hz. "
            f"Aliasing may occur."
        )
    t = np.arange(0, duration, 1 / sampling_frequency)
    match waveform:
        case "sine":
            signal = amplitude * np.sin(
                2 * np.pi * frequency * t + phase_rad
            )

        case "cosine":
            signal = amplitude * np.cos(
                2 * np.pi * frequency * t + phase_rad
            )

        case "square":
            signal = amplitude * np.sign(
                np.sin(2 * np.pi * frequency * t + phase_rad)
            )
        case "sawtooth":
            signal = amplitude * (
                    2 * ((frequency * t + phase_rad / (2 * np.pi)) % 1) - 1
            )

        case _:
            print("Invalid waveform!")
            return
    # FFT
    fft_result = np.fft.fft(signal)
    magnitude = np.abs(fft_result)

    # Frequency axis
    frequency_axis = np.fft.fftfreq(
        len(signal),
        d=1 / sampling_frequency
    )

    half = len(signal) // 2

    positive_frequency = frequency_axis[:half]
    positive_magnitude = (2 / len(signal)) * magnitude[:half]



    fig, ax = plt.subplots(2, 1)

    # Time domain
    ax[0].plot(t, signal)
    ax[0].set_xlabel("Time [s]")
    ax[0].set_ylabel("Amplitude [V]")
    ax[0].set_title("Time Domain")
    ax[0].grid(True)

    # Frequency domain
    ax[1].stem(positive_frequency, positive_magnitude)
    ax[1].set_xlabel("Frequency [Hz]")
    ax[1].set_ylabel("Magnitude")
    ax[1].set_title("Frequency Spectrum")
    ax[1].grid(True)

    plt.tight_layout()
    plt.show()



def discrete_signal():
    amplitude = get_float("Enter amplitude [V]: ")
    omega = get_float("Enter angular frequency [rad/sample]: ")
    sample_number = get_positive_integer("Enter sample number [n]: ")
    phase_deg = get_phase("Enter phase [deg]: ")
    phase_rad = np.deg2rad(phase_deg)

    n = np.arange(sample_number)
    signal = amplitude * np.sin((omega * n)+ phase_rad)
    fft_result = np.fft.fft(signal)
    magnitude = np.abs(fft_result)
    frequency_axis = np.fft.fftfreq(sample_number, d=1)
    omega_axis = 2 * np.pi * frequency_axis

    # Positive-frequency half
    half = sample_number // 2
    positive_omega = omega_axis[:half]
    positive_magnitude = (2 / sample_number) * magnitude[:half]

    # Plots
    fig, ax = plt.subplots(2, 1)

    # Time domain
    ax[0].stem(n, signal)
    ax[0].set_xlabel("Sample index [n]")
    ax[0].set_ylabel("Amplitude [V]")
    ax[0].set_title("Discrete-Time Signal")
    ax[0].grid(True)

    # Frequency domain
    ax[1].stem(positive_omega, positive_magnitude)
    ax[1].set_xlabel("Angular Frequency [rad/sample]")
    ax[1].set_ylabel("Magnitude")
    ax[1].set_title("Frequency Spectrum")
    ax[1].grid(True)

    plt.tight_layout()
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