from view import GUI
from model import Model
import os

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Add event handlers
        self.view.openAudio.configure(command=self.openAudio)
        self.view.playAudio.configure(command=self.playAudio)
        self.view.stopAudio.configure(command=self.stopAudio)

    # ... other methods ...

    def openAudio(self):
        global file
        file = self.view.openAudio()
        if file:
            mono_file = self.model.convert_file(file)
            mono_file = self.model.clean_file()

            # Display file information in the view
            length, max_frequency = self.model.length_and_max_freq(mono_file)
            self.view.name.set(f"File Name: {os.path.basename(file)}")
            self.view.fileSize.set(f"File Size: {round(int(os.path.getsize(file)) / (pow(10, 6)), 2)} MB")
            # Add other information as needed

    def playAudio(self):
        global file
        file = self.view.getAudio()
        if file:
            # Use the view to play the audio
            self.view.playAudio(file)
        else:
            # Use the view to play a default audio (silence.wav)
            self.view.playAudio('silence.wav')

    def stopAudio(self):
        global file
        # Use the view to stop the audio
        self.view.stopAudio()

if __name__ == "__main__":
    # Initialize the model and view
    model = Model(None)
    view = GUI()

    # Initialize the controller with the model and view
    controller = Controller(model, view)

    # Start the Tkinter main loop
    view.mainloop()
