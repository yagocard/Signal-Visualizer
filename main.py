import numpy as np
import matplotlib.pyplot as plt
signal_type = input("Continuous or discrete? (c/d): ")
if signal_type == "c":
    amplitude = float(input("Enter amplitude[V]: "))
    frequency = float(input("Enter frequency[Hz]: "))
    sample_number = int(input("Enter sample number[n]: "))
    t = np.linspace(0, 1 / frequency, int(sample_number))
    signal = amplitude * np.sin(2 * np.pi * frequency * t)

    plt.plot(t, signal)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Sine Wave")
    plt.grid()
    plt.show()

elif signal_type == "d":
    amplitude = float(input("Enter amplitude[V]: "))
    omega = float(input("Enter angular frequency[rad/sample]: "))
    sample_number = int(input("Enter sample number[n]: "))

    n = np.arange(sample_number)

    signal = amplitude * np.sin(omega * n)

    plt.stem(n, signal)
    plt.xlabel("n")
    plt.ylabel("Amplitude")
    plt.title("Discrete-Time Sine Wave")
    plt.grid()
    plt.show()
else:
    print("Invalid signal type!")

