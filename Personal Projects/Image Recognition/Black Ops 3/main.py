import mss
import cv2
import numpy as np
import time
import pytesseract

#tesseract path location (if your pc corrupted FUCK YOU!)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\sassy\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\pytesseract.exe'

killCount = 0
lastDetectionTime = 0
cd = 0.5

#not the actual coords
monitor = {"top": 200, "left": 500, "width": 150, "height": 50}


def preprocessImg(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # Apply binary thresholding
    return thresh


#grabbing photo of monitor
with mss.mss() as sct:
    print("Starting kill tracker!")
    try:
        while True:
            #capture screen
            img = np.array(sct.grab(monitor))

            processedImg(img) = preprocessImg(img)

            # Perform OCR to extract text - Also known as "WTF does this mean"
            custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=+0123456789'
            text = pytesseract.image_to_string(processedImg, config=custom_config)

            #scan for "+50" or "+10" or "+100"
            currentTime = time.time()
            if "+50" in text or "+10" in text or "+100" or "+60" in text:
                #should I scan?
                if currentTime - lastDetectionTime > cd:
                    #yes!
                    killCount += 1
                    lastDetectionTime = currentTime
                    print("Kill detected!")
            #should help pc not die
            time.sleep(0.1)

    except KeyboardInterrupt:
        print(f"Exiting program - Final Kill Count: {killCount}")




