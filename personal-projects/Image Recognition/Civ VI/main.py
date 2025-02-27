import mss
import cv2
import numpy as np
import time
import pytesseract
from pytesseract import image_to_string

foodThreshold = 3
prodThreshold = 2

GRID_ROWS = 5 
GRID_COLS = 5

#not the actual coords
coords = {"top": 96, "left": 326, "width": 1342, "height": 870}

# Suggested buildings based on yield priority
BUILDING_SUGGESTIONS = {
    "Food": "Granary or Farm Improvements",
    "Production": "Workshop or Industrial Zone",
    "Culture": "Theater Square",
    "Science": "Campus",
}

# OCR Configuration
TESSERACT_CONFIG = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789FoodProductionCultureScience'

# Load templates for each icon (assuming they are in the same directory)
templates = {
    "Food": cv2.imread("Assets/food_icon.png", cv2.IMREAD_GRAYSCALE),
    "Production": cv2.imread("Assets/production_icon.png", cv2.IMREAD_GRAYSCALE),
    "Culture": cv2.imread("Assets/culture_icon.png", cv2.IMREAD_GRAYSCALE),
    "Science": cv2.imread("Assets/science_icon.png", cv2.IMREAD_GRAYSCALE),
}

def preprocessImg(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contrast = cv2.convertScaleAbs(gray, alpha=2.0, beta=0)  # Increase contrast
    binary = cv2.adaptiveThreshold(contrast, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return binary


def divideIntoTiles(image, rows, cols):
    tile_height = image.shape[0] // rows
    tile_width = image.shape[1] // cols
    tiles = []
    for row in range(rows):
        for col in range(cols):
            x = col * tile_width
            y = row * tile_height
            tile = image[y:y + tile_height, x:x + tile_width]
            tiles.append((tile, (row, col)))
    return tiles


# Function to perform template matching and detect icons
def detect_icon(image, icon_name):
    template = templates.get(icon_name)
    if template is None:
        print(f"Template for {icon_name} not found.")
        return []
    
    # Resize template to fit within tile size
    tile_height, tile_width = image.shape
    template_height, template_width = template.shape
    if template_height > tile_height or template_width > tile_width:
        # Resize template to fit the tile
        template = cv2.resize(template, (tile_width, tile_height))
        print(f"Resized template for {icon_name} to fit tile size.")

    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Minimum correlation threshold
    loc = np.where(result >= threshold)

    if len(loc[0]) > 0:
        return [icon_name]  # Found the icon
    return []  # Icon not found


def evaluateTile(tile):
    text = pytesseract.image_to_string(tile, config=TESSERACT_CONFIG)
    print(f"OCR Text: {text.strip()}")

    if len(text.strip()) < 3:
        print("Error: OCR text is too short or empty. No suggestions.")
        return []

    suggestions = []
    for keyword, building in BUILDING_SUGGESTIONS.items():
        if keyword in text:
            suggestions.append(building)

    if len(suggestions) == 0:
        print("No relevent suggestions")

    time.sleep(2)
    return suggestions


def drawRecommendations(image, tiles, rows, cols, suggestions):
    tile_width = image.shape[1] // cols
    tile_height = image.shape[0] // rows 
    for (tile, (row, col)), suggestion in zip(tiles, suggestions):
        if suggestion:
            x = col * tile_width
            y = row * tile_height
            cv2.rectangle(image, (x, y), (x + tile_width, y + tile_height), (0, 255, 0), 2)
            cv2.putText(
                image, ", ".join(suggestion), (x + 5, y + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
            )

    return image


#grabbing photo of monitor
with mss.mss() as sct:
    print("Starting Civ VI speedrunner")
    try:
        while True:
            #capture screen
            screenshot = sct.grab(coords)
            img = np.array(screenshot)

            processImg = preprocessImg(img)
            tiles = divideIntoTiles(processImg, GRID_ROWS, GRID_COLS)

            # Check for icons and evaluate text in each tile
            suggestions = []
            for tile, pos in tiles:
                # First, check if an icon is detected
                icon_suggestions = []
                for icon_name in BUILDING_SUGGESTIONS:
                    icon_suggestions += detect_icon(tile, icon_name)

                # If no icons are found, evaluate OCR text
                if not icon_suggestions:
                    icon_suggestions = evaluateTile(tile)

                suggestions.append(icon_suggestions)
            
            annotated_img = drawRecommendations(img, tiles, GRID_ROWS, GRID_COLS, suggestions)
            
            annotated_img = cv2.resize(annotated_img, (1024, 768))
            cv2.imshow("Annotated Image", annotated_img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            #should help pc not die
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        cv2.destroyAllWindows()