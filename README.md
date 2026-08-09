# Signal Visualizer

Signal Visualizer is a Python-based application for generating, visualizing, and analyzing continuous-time and discrete-time signals.

The project provides both time-domain and frequency-domain representations of signals using the Fast Fourier Transform (FFT). It also includes a graphical user interface built with CustomTkinter.

## Features

* Continuous-time and discrete-time signal generation
* Sine, cosine, square, and sawtooth waveforms for continuous signals
* Adjustable amplitude, frequency, phase, duration, and sampling frequency
* Discrete-time sinusoidal signal generation using angular frequency
* Time-domain visualization
* Frequency-domain analysis using FFT
* Nyquist criterion check and aliasing warning
* Input validation
* Graphical user interface with CustomTkinter

## Technologies

* Python
* NumPy
* Matplotlib
* CustomTkinter

## Signal Analysis

For continuous signals, the application generates samples according to the selected waveform and sampling frequency.

The frequency spectrum is calculated using NumPy's Fast Fourier Transform:

```python
fft_result = np.fft.fft(signal)
```

The corresponding frequency bins are generated using:

```python
frequency_axis = np.fft.fftfreq(
    len(signal),
    d=1 / sampling_frequency
)
```

For discrete-time signals, the frequency spectrum is represented using angular frequency in rad/sample.

## Nyquist Criterion

For continuous signals, the application checks whether the selected sampling frequency satisfies the Nyquist criterion:

[
f_s \geq 2f
]

If the sampling frequency is below the Nyquist rate, the application displays a warning indicating that aliasing may occur.

## Graphical User Interface

The GUI allows signal parameters to be changed interactively and displays both the time-domain signal and its frequency spectrum.

The interface is built using CustomTkinter, while Matplotlib is embedded inside the application for visualization.

## Installation

Clone the repository:

```bash
git clone https://github.com/yagocard/Signal-Visualizer.git
cd Signal-Visualizer
```

Install the required dependencies:

```bash
pip install numpy matplotlib customtkinter
```

Run the graphical interface:

```bash
python gui.py
```

The command-line version can also be run using:

```bash
python main.py
```

## Project Structure

```text
Signal-Visualizer/
├── main.py
├── gui.py
├── README.md
└── .gitignore
```

## Purpose

This project was developed as a practical introduction to signal processing concepts and Python-based engineering applications.

The main concepts explored in the project include:

* Signal generation
* Sampling
* Nyquist criterion
* Aliasing
* Discrete-time signals
* Fast Fourier Transform (FFT)
* Frequency spectrum visualization
* GUI development with Python

## Future Improvements

Possible future improvements include:

* Window functions such as Hann and Hamming
* Multiple signal components
* Signal filtering
* Audio signal analysis
* Exporting generated signals
* Additional discrete-time waveforms


