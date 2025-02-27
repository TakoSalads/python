import mss
import cv2
import numpy as np
import time
import pytesseract

#tesseract path location (if your pc corrupted FUCK YOU!)
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

killCount = 0
lastDetectionTime = 0
cd = 0.5

#not the actual coords
coords = {"top": 736, "left": 157, "width": 217, "height": 200}


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
            #monitor = sct.monitors[2]
            screenshot = sct.grab(coords)
            img = np.array(screenshot)

            processedImg = preprocessImg(img)

            # Perform OCR to extract text - Also known as "WTF does this mean"
            custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=+0123456789'
            text = pytesseract.image_to_string(processedImg, config=custom_config)

            #scan for "+50" or "+10" or "+100"
            currentTime = time.time()
            if any(value in text for value in ["+50", "+100", "+60"]):
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




