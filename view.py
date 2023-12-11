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
        global fileSize
        file = filedialog.askopenfilename(filetypes=[('Waveform Files', '*.wav'), ('All Files', '*')])
        if file:
            name.set("File Name: " + str(os.path.basename(file)))
            fileSize.set("File Size: " + str(round(int(os.path.getsize(file)) / (pow(10, 6)), 2)) + " MB")
            self.file = file

    # Function to play .wav file
    def playAudio(self):
        global file
        if file:
            winsound.PlaySound(str(file), winsound.SND_ASYNC)
        else:
            winsound.PlaySound('silence.wav', winsound.SND_ASYNC)

    # Function to stop .wav file
    def stopAudio(self):
        global file
        winsound.PlaySound('silence.wav', winsound.SND_ASYNC)

    # Function to access the opened .wav file
    def getAudio(self):
        global file
        return self.file

    def __init__(self):
        # Initializing the self window
        super(GUI, self).__init__()
        global name
        global fileSize

        self.file = 'silence.wav'
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

        # File Name
        name = StringVar()
        name.set("File Name:")
        fileName = Label(self, textvariable=name, bg='white', font=("Arial", 15), width=40, anchor=W)
        fileName.place(x=160, y=25)

        # File Size
        fileSize = StringVar()
        fileSize.set("File Size:")
        fileName = Label(self, textvariable=fileSize, bg='white', font=("Arial", 15), width=40, anchor=W)
        fileName.place(x=160, y=50)