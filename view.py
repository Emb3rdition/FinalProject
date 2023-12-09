from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import winsound
import os


class GUI(Tk):
    # Function to select .wav file
    def openAudio(self):
        global file
        global name
        file = filedialog.askopenfilename(filetypes=[('Waveform Files', '*.wav'), ('All Files', '*')])
        if file:
            name = os.path.split(file)[1]

    # Function to play .wav file
    def playAudio(self):
        global file
        if file:
            winsound.PlaySound(str(file), winsound.SND_ASYNC)

    # Function to stop .wav file
    def stopAudio(self):
        global file
        winsound.PlaySound('silence.wav', winsound.SND_ASYNC)

    # Function to access the opened .wav file
    def getAudio(self):
        global file
        return file

    def __init__(self):
        # Initializing the self window
        super(GUI, self).__init__()
        self.title('Audio Viewer')
        self.geometry("800x800")
        self.maxsize(800, 800)
        self.minsize(800, 800)
        self.config(bg='#e0e0e0')

        # Creating the frames for the self formatting

        buttonsFrame = Frame(self, width=114, height=244, bg='#242424')
        buttonsFrame.place(x=13, y=13)
        buttonsFrame = Frame(self, width=110, height=240, bg='white')
        buttonsFrame.place(x=15, y=15)

        buttonsFrame = Frame(self, width=514, height=244, bg='#242424')
        buttonsFrame.place(x=150, y=13)
        buttonsFrame = Frame(self, width=510, height=240, bg='white')
        buttonsFrame.place(x=152, y=15)

        buttonsFrame = Frame(self, width=770, height=510, bg='#242424')
        buttonsFrame.place(x=13, y=270)
        buttonsFrame = Frame(self, width=766, height=506, bg='white')
        buttonsFrame.place(x=15, y=272)

        # Creating the buttons for the self

        uploadButton = ttk.Button(self, text="Open File", command=self.openAudio, width=15)
        uploadButton.place(x=20, y=20)

        playAudio = ttk.Button(self, text="Play Audio", width=15, command=self.playAudio)
        playAudio.place(x=20, y=60)
        pauseAudio = ttk.Button(self, text="Stop Audio", width=15, command=self.stopAudio)
        pauseAudio.place(x=20, y=85)

        lowFreqBut = ttk.Button(self, text="Low Freq", width=15)
        lowFreqBut.place(x=20, y=150)
        midFreqBut = ttk.Button(self, text="Mid Freq", width=15)
        midFreqBut.place(x=20, y=175)
        highFreqBut = ttk.Button(self, text="High Freq", width=15)
        highFreqBut.place(x=20, y=200)
        mergeFreqBut = ttk.Button(self, text="Merge Freq", width=15)
        mergeFreqBut.place(x=20, y=225)