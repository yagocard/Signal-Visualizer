import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# -----------------------------
# Main window
# -----------------------------

app = ctk.CTk()
app.title("Signal Visualizer")
app.geometry("1100x750")


# -----------------------------
# Functions
# -----------------------------

def update_signal_type(selected_type):
    if selected_type == "Continuous":
        waveform_label.grid()
        waveform_menu.grid()

        frequency_label.configure(text="Frequency [Hz]")
        duration_label.grid()
        duration_entry.grid()
        sampling_frequency_label.grid()
        sampling_frequency_entry.grid()

    else:
        waveform_label.grid_remove()
        waveform_menu.grid_remove()

        frequency_label.configure(
            text="Angular Frequency [rad/sample]"
        )

        duration_label.grid_remove()
        duration_entry.grid_remove()

        sampling_frequency_label.grid_remove()
        sampling_frequency_entry.grid_remove()


def show_error(message):
    status_label.configure(
        text=message,
        text_color="red"
    )


def show_warning(message):
    status_label.configure(
        text=message,
        text_color="orange"
    )


def clear_status():
    status_label.configure(text="")


def generate_signal():
    clear_status()

    try:
        amplitude = float(amplitude_entry.get())
        phase_deg = float(phase_entry.get())
        phase_rad = np.deg2rad(phase_deg)

    except ValueError:
        show_error("Amplitude and phase must be numbers.")
        return

    signal_type = signal_type_menu.get()

    # Clear old graph
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # -----------------------------
    # Continuous signal
    # -----------------------------

    if signal_type == "Continuous":

        waveform = waveform_menu.get()

        try:
            frequency = float(frequency_entry.get())
            duration = float(duration_entry.get())
            sampling_frequency = float(
                sampling_frequency_entry.get()
            )

        except ValueError:
            show_error(
                "Frequency, duration and sampling frequency "
                "must be numbers."
            )
            return

        if frequency <= 0:
            show_error("Frequency must be greater than zero.")
            return

        if duration <= 0:
            show_error("Duration must be greater than zero.")
            return

        if sampling_frequency <= 0:
            show_error(
                "Sampling frequency must be greater than zero."
            )
            return

        nyquist_rate = 2 * frequency

        if sampling_frequency < nyquist_rate:
            show_warning(
                f"Warning: Nyquist criterion not satisfied! "
                f"Sampling frequency should be at least "
                f"{nyquist_rate:.2f} Hz. Aliasing may occur."
            )

        t = np.arange(
            0,
            duration,
            1 / sampling_frequency
        )

        if len(t) < 2:
            show_error(
                "Not enough samples. Increase duration or "
                "sampling frequency."
            )
            return

        match waveform:

            case "Sine":
                signal = amplitude * np.sin(
                    2 * np.pi * frequency * t
                    + phase_rad
                )

            case "Cosine":
                signal = amplitude * np.cos(
                    2 * np.pi * frequency * t
                    + phase_rad
                )

            case "Square":
                signal = amplitude * np.sign(
                    np.sin(
                        2 * np.pi * frequency * t
                        + phase_rad
                    )
                )

            case "Sawtooth":
                signal = amplitude * (
                    2 * (
                        (
                            frequency * t
                            + phase_rad / (2 * np.pi)
                        ) % 1
                    ) - 1
                )

            case _:
                show_error("Invalid waveform.")
                return

        # FFT
        fft_result = np.fft.fft(signal)
        magnitude = np.abs(fft_result)

        frequency_axis = np.fft.fftfreq(
            len(signal),
            d=1 / sampling_frequency
        )

        half = len(signal) // 2

        positive_frequency = frequency_axis[:half]

        positive_magnitude = (
            2 / len(signal)
        ) * magnitude[:half]

        # Figure
        fig, ax = plt.subplots(
            2,
            1,
            figsize=(8, 6)
        )

        # Time domain
        ax[0].plot(t, signal)

        ax[0].set_xlabel("Time [s]")
        ax[0].set_ylabel("Amplitude [V]")
        ax[0].set_title("Time Domain")
        ax[0].grid(True)

        # Frequency domain
        ax[1].stem(
            positive_frequency,
            positive_magnitude
        )

        ax[1].set_xlabel("Frequency [Hz]")
        ax[1].set_ylabel("Magnitude")
        ax[1].set_title("Frequency Spectrum")
        ax[1].grid(True)

    # -----------------------------
    # Discrete signal
    # -----------------------------

    else:

        try:
            omega = float(frequency_entry.get())
            sample_number = int(sample_entry.get())

        except ValueError:
            show_error(
                "Angular frequency must be a number and "
                "sample number must be an integer."
            )
            return

        if sample_number <= 1:
            show_error(
                "Sample number must be greater than one."
            )
            return

        n = np.arange(sample_number)

        signal = amplitude * np.sin(
            omega * n + phase_rad
        )

        # FFT
        fft_result = np.fft.fft(signal)
        magnitude = np.abs(fft_result)

        frequency_axis = np.fft.fftfreq(
            sample_number,
            d=1
        )

        omega_axis = (
            2 * np.pi * frequency_axis
        )

        half = sample_number // 2

        positive_omega = omega_axis[:half]

        positive_magnitude = (
            2 / sample_number
        ) * magnitude[:half]

        # Figure
        fig, ax = plt.subplots(
            2,
            1,
            figsize=(8, 6)
        )

        # Time domain
        ax[0].stem(n, signal)

        ax[0].set_xlabel("Sample index [n]")
        ax[0].set_ylabel("Amplitude [V]")
        ax[0].set_title(
            "Discrete-Time Signal"
        )
        ax[0].grid(True)

        # Frequency domain
        ax[1].stem(
            positive_omega,
            positive_magnitude
        )

        ax[1].set_xlabel(
            "Angular Frequency [rad/sample]"
        )
        ax[1].set_ylabel("Magnitude")
        ax[1].set_title(
            "Frequency Spectrum"
        )
        ax[1].grid(True)

    # -----------------------------
    # Put matplotlib inside GUI
    # -----------------------------

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(
        fig,
        master=graph_frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )

    plt.close(fig)


# -----------------------------
# Layout
# -----------------------------

title = ctk.CTkLabel(
    app,
    text="Signal Visualizer",
    font=("Arial", 28, "bold")
)

title.pack(pady=15)


main_frame = ctk.CTkFrame(app)
main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


# -----------------------------
# Input panel
# -----------------------------

input_frame = ctk.CTkFrame(
    main_frame,
    width=300
)

input_frame.pack(
    side="left",
    fill="y",
    padx=10,
    pady=10
)


# Signal type

signal_type_label = ctk.CTkLabel(
    input_frame,
    text="Signal Type"
)

signal_type_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)


signal_type_menu = ctk.CTkOptionMenu(
    input_frame,
    values=[
        "Continuous",
        "Discrete"
    ],
    command=update_signal_type
)

signal_type_menu.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Waveform

waveform_label = ctk.CTkLabel(
    input_frame,
    text="Waveform"
)

waveform_label.grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)


waveform_menu = ctk.CTkOptionMenu(
    input_frame,
    values=[
        "Sine",
        "Cosine",
        "Square",
        "Sawtooth"
    ]
)

waveform_menu.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Amplitude

amplitude_label = ctk.CTkLabel(
    input_frame,
    text="Amplitude [V]"
)

amplitude_label.grid(
    row=2,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)


amplitude_entry = ctk.CTkEntry(
    input_frame
)

amplitude_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)

amplitude_entry.insert(0, "1")


# Frequency / Omega

frequency_label = ctk.CTkLabel(
    input_frame,
    text="Frequency [Hz]"
)

frequency_label.grid(
    row=3,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)


frequency_entry = ctk.CTkEntry(
    input_frame
)

frequency_entry.grid(
    row=3,
    column=1,
    padx=10,
    pady=10
)

frequency_entry.insert(0, "10")


# Duration

duration_label = ctk.CTkLabel(
    input_frame,
    text="Duration [s]"
)

duration_label.grid(
    row=4,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)


duration_entry = ctk.CTkEntry(
    input_frame
)

duration_entry.grid(
    row=4,
    column=1,
    padx=10,
    pady=10
)

duration_entry.insert(0, "1")


# Sampling frequency

sampling_frequency_label = ctk.CTkLabel(
    input_frame,
    text="Sampling Frequency [Hz]"
)

sampling_frequency_label.grid(
    row=5,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)


sampling_frequency_entry = ctk.CTkEntry(
    input_frame
)

sampling_frequency_entry.grid(
    row=5,
    column=1,
    padx=10,
    pady=10
)

sampling_frequency_entry.insert(
    0,
    "100"
)


# Sample number

sample_label = ctk.CTkLabel(
    input_frame,
    text="Sample Number [n]"
)

sample_label.grid(
    row=6,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)


sample_entry = ctk.CTkEntry(
    input_frame
)

sample_entry.grid(
    row=6,
    column=1,
    padx=10,
    pady=10
)

sample_entry.insert(
    0,
    "100"
)


# Phase

phase_label = ctk.CTkLabel(
    input_frame,
    text="Phase [deg]"
)

phase_label.grid(
    row=7,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)


phase_entry = ctk.CTkEntry(
    input_frame
)

phase_entry.grid(
    row=7,
    column=1,
    padx=10,
    pady=10
)

phase_entry.insert(0, "0")


# Generate button

generate_button = ctk.CTkButton(
    input_frame,
    text="Generate Signal",
    command=generate_signal
)

generate_button.grid(
    row=8,
    column=0,
    columnspan=2,
    pady=20
)


# Status / warning

status_label = ctk.CTkLabel(
    input_frame,
    text="",
    wraplength=280
)

status_label.grid(
    row=9,
    column=0,
    columnspan=2,
    padx=10,
    pady=10
)


# -----------------------------
# Graph panel
# -----------------------------

graph_frame = ctk.CTkFrame(
    main_frame
)

graph_frame.pack(
    side="right",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# Initialize
signal_type_menu.set("Continuous")
waveform_menu.set("Sine")

update_signal_type("Continuous")


app.mainloop()
