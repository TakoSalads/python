import tkinter as tk
import pyaudio

# Initialize PyAudio
p = pyaudio.PyAudio()

# Create Tkinter window
root = tk.Tk()
root.title("Mute Button")

# Define mute button
mute_button = tk.Button(root, text="Mute", command=mute_audio)
mute_button.pack()

def mute_audio():
    # Toggle microphone mute state using PyAudio
    if p.get_input_latency() > 0:
        p.set_input_mute(True)
        mute_button.config(text="Unmute")
    else:
        p.set_input_mute(False)
        mute_button.config(text="Mute")

# Start Tkinter event loop
root.mainloop()