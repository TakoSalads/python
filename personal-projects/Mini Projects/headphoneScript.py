from pycaw.pycaw import AudioUtilities
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.utils import get_audio_device_by_name
import json
import os

# Helper function to get the default audio device
def get_default_audio_device():
    devices = AudioUtilities.GetSpeakers()
    return devices

# Helper function to set the default audio device
def set_default_audio_device(device_name):
    # Get all audio devices
    devices = AudioUtilities.GetAllDevices()
    for device in devices:
        if device.FriendlyName == device_name:
            device.Activate(CLSCTX_ALL, None)
            break

# Helper function to read the current device from a file
def read_current_device():
    if os.path.exists("current_device.json"):
        with open("current_device.json", "r") as file:
            return json.load(file)
    return None

# Helper function to write the current device to a file
def write_current_device(device_name):
    with open("current_device.json", "w") as file:
        json.dump(device_name, file)

# Device names
speaker_name = "Speakers (Realtek(R) Audio)"
headphone_name = "Headphones (WH-XB910N Stereo)"

# Read the current device from the file
current_device = read_current_device()

if current_device == speaker_name:
    new_device = headphone_name
else:
    new_device = speaker_name

# Set the new default audio device
set_default_audio_device(new_device)

# Save the new device to the file
write_current_device(new_device)

print(f"Toggled audio output to {new_device}")
