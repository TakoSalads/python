import mss
import numpy as np
import cv2

# Define the coordinates for the region to capture
coords = {"top": 736, "left": 157, "width": 217, "height": 200}

# Grabbing photo of the region
with mss.mss() as sct:
    print("Capturing the specified region...")
    screenshot = sct.grab(coords)  # Capture the region defined by coords
    img = np.array(screenshot)  # Convert screenshot to a numpy array

    # Save the captured image to a file
    cv2.imwrite("captured_region.png", img)  # Save as a PNG file

    print("Screenshot saved as 'captured_region.png'")