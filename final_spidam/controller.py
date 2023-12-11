import numpy as np
from view import GUI
from model import Model
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import wave, sys


class Controller:
    def update(self):
        global view
        global model
        global resonanceVar
        global diffVar
        global lengthVar

        model.convert_file(view.getAudio())
        file = model.clean_file()

        resonanceVar.set("Resonance: " + str(model.length_and_max_freq(file)[1]))
        lengthVar.set("Length: " + str(model.length_and_max_freq(file)[0]))
        diffVar.set("RT60 Difference: " + str(model.rt60diff(file)))

    def plotLow(self):
        global view
        global model
        global lowBoo
        global midBoo
        global highBoo
        global combBoo

        lowBoo = True
        midBoo = False
        highBoo = False
        combBoo = False

        # Get info for graph
        model.convert_file(view.getAudio())
        file = model.clean_file()
        data_db_l, rt_60_l, iom_l, iom_5_l, iom_25_l = model.rt60_vals(model.low, file)
        samp_rate, d, spectrum, freqs, y = model.data(file)
        low_data = model.frequency_check(model.low, file)

        # Create Graph for Low Freq
        fig = plt.figure(figsize=(7.5, 4.5))
        plotL = fig.add_subplot(111)
        plotL.set_title('Low Freq RT60 Plot')
        plotL.set(xlabel="Time (s)", ylabel="Power (dB)")

        plotL.plot(y, low_data, label=f'Low Frequency ({model.low} Hz)', linewidth=1,
                   alpha=0.7, color='red')
        plotL.plot(y[iom_l], low_data[iom_l], 'go')
        plotL.plot(y[iom_5_l], low_data[iom_5_l], 'yo')
        plotL.plot(y[iom_25_l], low_data[iom_25_l], 'ro')

        plotL.legend()

        # Add plot to tkinter gui
        tkPlotLow = FigureCanvasTkAgg(fig, view)
        tkPlotLow.draw()

        tkPlotLow.get_tk_widget().place(x=23, y=280)

    def plotMid(self):
        global view
        global model
        global lowBoo
        global midBoo
        global highBoo
        global combBoo

        lowBoo = False
        midBoo = True
        highBoo = False
        combBoo = False

        # Get info for graph
        model.convert_file(view.getAudio())
        file = model.clean_file()
        data_db_m, rt_60_m, iom_m, iom_5_m, iom_25_m = model.rt60_vals(model.mid, file)
        samp_rate, d, spectrum, freqs, y = model.data(file)
        mid_data = model.frequency_check(model.mid, file)

        # Create Graph for Mid Freq
        fig = plt.figure(figsize=(7.5, 4.5))
        plotM = fig.add_subplot(111)
        plotM.set_title('Mid Freq RT60 Plot')
        plotM.set(xlabel="Time (s)", ylabel="Power (dB)")

        plotM.plot(y, mid_data, label=f'Mid Frequency ({model.mid} Hz)', linewidth=1,
                   alpha=0.7, color='red')
        plotM.plot(y[iom_m], mid_data[iom_m], 'go')
        plotM.plot(y[iom_5_m], mid_data[iom_5_m], 'yo')
        plotM.plot(y[iom_25_m], mid_data[iom_25_m], 'ro')

        plotM.legend()

        # Add plot to tkinter gui
        tkPlotMid = FigureCanvasTkAgg(fig, view)
        tkPlotMid.draw()

        tkPlotMid.get_tk_widget().place(x=23, y=280)

    def plotHigh(self):
        global view
        global model
        global lowBoo
        global midBoo
        global highBoo
        global combBoo

        lowBoo = False
        midBoo = False
        highBoo = True
        combBoo = False

        # Get info for graph
        model.convert_file(view.getAudio())
        file = model.clean_file()
        data_db_h, rt_60_h, iom_h, iom_5_h, iom_25_h = model.rt60_vals(model.high, file)
        samp_rate, d, spectrum, freqs, y = model.data(file)
        high_data = model.frequency_check(model.high, file)

        # Create Graph for High Freq
        fig = plt.figure(figsize=(7.5, 4.5))
        plotH = fig.add_subplot(111)
        plotH.set_title('High Freq RT60 Plot')
        plotH.set(xlabel="Time (s)", ylabel="Power (dB)")

        plotH.plot(y, high_data, label=f'High Frequency ({model.high} Hz)', linewidth=1, alpha=0.7, color='red')
        plotH.plot(y[iom_h], high_data[iom_h], 'go')
        plotH.plot(y[iom_5_h], high_data[iom_5_h], 'yo')
        plotH.plot(y[iom_25_h], high_data[iom_25_h], 'ro')

        plotH.legend()

        # Add plot to tkinter gui
        tkPlotHigh = FigureCanvasTkAgg(fig, view)
        tkPlotHigh.draw()

        tkPlotHigh.get_tk_widget().place(x=23, y=280)

    def plotCombined(self):
        global view
        global model
        global lowBoo
        global midBoo
        global highBoo
        global combBoo

        lowBoo = False
        midBoo = False
        highBoo = False
        combBoo = True

        # Get info for graph
        model.convert_file(view.getAudio())
        file = model.clean_file()
        samp_rate, d, spectrum, freqs, y = model.data(file)
        data_db_l, rt_60_l, iom_l, iom_5_l, iom_25_l = model.rt60_vals(model.low, file)
        low_data = model.frequency_check(model.low, file)
        data_db_m, rt_60_m, iom_m, iom_5_m, iom_25_m = model.rt60_vals(model.mid, file)
        mid_data = model.frequency_check(model.mid, file)
        data_db_h, rt_60_h, iom_h, iom_5_h, iom_25_h = model.rt60_vals(model.high, file)
        high_data = model.frequency_check(model.high, file)

        # Create Graph for All Freq
        fig = plt.figure(figsize=(7.5, 4.5))
        plotC = fig.add_subplot(111)
        plotC.set_title('Combined RT60 Plot')
        plotC.set(xlabel="Time (s)", ylabel="Power (dB)")

        plotC.plot(y, low_data, label=f'Low Frequency ({model.low} Hz)', linewidth=1, alpha=0.7, color='red')
        plotC.plot(y, mid_data, label=f'Mid Frequency ({model.mid} Hz)', linewidth=1, alpha=0.7, color='green')
        plotC.plot(y, high_data, label=f'High Frequency ({model.high} Hz)', linewidth=1, alpha=0.7, color='blue')

        plotC.plot(y[iom_l], low_data[iom_l], 'go')
        plotC.plot(y[iom_5_l], low_data[iom_5_l], 'yo')
        plotC.plot(y[iom_25_l], low_data[iom_25_l], 'ro')

        plotC.plot(y[iom_m], mid_data[iom_m], 'go')
        plotC.plot(y[iom_5_m], mid_data[iom_5_m], 'yo')
        plotC.plot(y[iom_25_m], mid_data[iom_25_m], 'ro')

        plotC.plot(y[iom_h], high_data[iom_h], 'go')
        plotC.plot(y[iom_5_h], high_data[iom_5_h], 'yo')
        plotC.plot(y[iom_25_h], high_data[iom_25_h], 'ro')

        plotC.legend()

        # Add plot to tkinter gui
        tkPlotHigh = FigureCanvasTkAgg(fig, view)
        tkPlotHigh.draw()

        tkPlotHigh.get_tk_widget().place(x=23, y=280)

    def waveform(self):
        global view
        global model

        # Get info for graph
        file = wave.open('audio.wav')
        signal = file.readframes(-1)
        signal = np.frombuffer(signal, dtype="int16")

        f_rate = file.getframerate()
        time = np.linspace(
            0,  # start
            len(signal) / f_rate,
            num=len(signal)
        )

        # Create Waveform Plot
        fig = plt.figure(figsize=(7.5, 4.5))
        plt.plot(time, signal, linewidth=1, alpha=0.7, color='red')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')

        # Add plot to tkinter gui
        tkPlotHigh = FigureCanvasTkAgg(fig, view)
        tkPlotHigh.draw()

        tkPlotHigh.get_tk_widget().place(x=23, y=280)

    def spectrogramPlot(self):
        global view
        global model

        # Get info for graph
        model.convert_file(view.getAudio())
        f = model.clean_file()
        samp_rate, d, spectrum, freqs, t = model.data(f)

        # Create Spectrogram Plot
        fig = plt.figure(figsize=(7.5, 4.5))
        spectrum, freqs, t, im = plt.specgram(d, Fs=samp_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar = plt.colorbar(im)
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        cbar.set_label('Intensity (dB)')

        # Add plot to tkinter gui
        tkPlotHigh = FigureCanvasTkAgg(fig, view)
        tkPlotHigh.draw()

        tkPlotHigh.get_tk_widget().place(x=23, y=280)

    def __init__(self):
        global view
        global model
        global resonanceVar
        global diffVar
        global lengthVar
        global lowBoo
        global midBoo
        global highBoo
        global combBoo

        # Initialize GUI and Model classes as objects
        view = GUI()
        model = Model()
        lowBoo = False
        midBoo = False
        highBoo = False
        combBoo = False

        # Creates buttons for freq so model and view can communicate
        lowFreqBut = ttk.Button(view, text="Low Freq", width=15, command=self.plotLow)
        lowFreqBut.place(x=20, y=150)
        midFreqBut = ttk.Button(view, text="Mid Freq", width=15, command=self.plotMid)
        midFreqBut.place(x=20, y=175)
        highFreqBut = ttk.Button(view, text="High Freq", width=15, command=self.plotHigh)
        highFreqBut.place(x=20, y=200)
        mergeFreqBut = ttk.Button(view, text="Merge Freq", width=15, command=self.plotCombined)
        mergeFreqBut.place(x=20, y=225)
        waveformBut = ttk.Button(view, text="Waveform", width=15, command=self.waveform)
        waveformBut.place(x=300, y=225)
        spectrogramBut = ttk.Button(view, text="Spectrogram", width=15, command=self.spectrogramPlot)
        spectrogramBut.place(x=400, y=225)
        updateBut = ttk.Button(view, text="Update Data", width=15, command=self.update)
        updateBut.place(x=160, y=180)

        # File Name
        diffVar = StringVar()
        diffVar.set("RT60 Difference:")
        rt60Diff = Label(view, textvariable=diffVar, bg='white', font=("Arial", 15), width=40, anchor=W)
        rt60Diff.place(x=160, y=100)

        # File Size
        resonanceVar = StringVar()
        resonanceVar.set("Resonance:")
        resonance = Label(view, textvariable=resonanceVar, bg='white', font=("Arial", 15), width=40, anchor=W)
        resonance.place(x=160, y=125)

        # File Size
        lengthVar = StringVar()
        lengthVar.set("Length:")
        length = Label(view, textvariable=lengthVar, bg='white', font=("Arial", 15), width=40, anchor=W)
        length.place(x=160, y=150)

        # Create Blank Plot
        fig = plt.figure(figsize=(7.5, 4.5))
        plotB = fig.add_subplot(111)
        plotB.set(xlabel="Time (s)", ylabel="Power (dB)")
        plotB.legend()

        plotB.plot()

        tkPlotHigh = FigureCanvasTkAgg(fig, view)
        tkPlotHigh.draw()

        tkPlotHigh.get_tk_widget().place(x=23, y=280)

        # Start the Tkinter main loop
        view.mainloop()
