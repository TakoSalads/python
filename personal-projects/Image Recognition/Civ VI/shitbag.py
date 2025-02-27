import mss
import cv2
import numpy as np
import time

# Not the actual coords
coords = {"top": 96, "left": 326, "width": 1342, "height": 870}

# Suggested buildings based on yield priority
BUILDING_SUGGESTIONS = {
    "Food": "Granary or Farm Improvements",
    "Production": "Workshop or Industrial Zone",
    "Culture": "Theater Square",
    "Science": "Campus",
}

# Load templates for each icon (assuming they are in the same directory)
templates = {
    "Food": cv2.imread("Assets/food_icon.png", cv2.IMREAD_GRAYSCALE),
    "Production": cv2.imread("Assets/production_icon.png", cv2.IMREAD_GRAYSCALE),
    "Culture": cv2.imread("Assets/culture_icon.png", cv2.IMREAD_GRAYSCALE),
    "Science": cv2.imread("Assets/science_icon.png", cv2.IMREAD_GRAYSCALE),
}

# Function to perform template matching and detect icons
def detect_icon(image, icon_name):
    template = templates.get(icon_name)
    if template is None:
        print(f"Template for {icon_name} not found.")
        return []

    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Minimum correlation threshold
    loc = np.where(result >= threshold)

    detectedLocations = list(zip(*loc[::-1]))

    return detectedLocations


# Function to apply Non-Maximum Suppression to filter overlapping detections
def non_maximum_suppression(detections, overlap_threshold=0.6):
    if len(detections) == 0:
        return []

    # Convert detections into an array of (x, y, width, height)
    boxes = np.array([(x, y, x + templates["Food"].shape[1], y + templates["Food"].shape[0]) for (x, y) in detections])

    # Calculate the area of each box
    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    areas = (x2 - x1) * (y2 - y1)

    # Sort the boxes by their bottom-right y-coordinate
    sorted_indices = np.argsort(areas)

    keep = []

    while len(sorted_indices) > 0:
        i = sorted_indices[-1]
        keep.append(i)

        # Compare the current box with the rest
        xx1 = np.maximum(x1[i], x1[sorted_indices[:-1]])
        yy1 = np.maximum(y1[i], y1[sorted_indices[:-1]])
        xx2 = np.minimum(x2[i], x2[sorted_indices[:-1]])
        yy2 = np.minimum(y2[i], y2[sorted_indices[:-1]])

        # Compute the area of the intersection
        w = np.maximum(0, xx2 - xx1)
        h = np.maximum(0, yy2 - yy1)
        intersection_area = w * h

        # Compute the ratio of intersection over union (IoU)
        union_area = areas[i] + areas[sorted_indices[:-1]] - intersection_area
        iou = intersection_area / union_area

        # Keep boxes that have IoU below the threshold
        remaining_indices = np.where(iou <= overlap_threshold)[0]
        sorted_indices = sorted_indices[remaining_indices]

    return [detections[i] for i in keep]


def preprocessImg(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
    return blur


# Grabbing photo of monitor
with mss.mss() as sct:
    print("Starting Civ VI speedrunner")
    try:
        while True:
            # Capture screen
            screenshot = sct.grab(coords)
            img = np.array(screenshot)

            # Preprocess image
            processImg = preprocessImg(img)

            # Check for each icon in the screen capture
            all_suggestions = []

            for icon_name in BUILDING_SUGGESTIONS:
                # Detect all instances of the icon
                detected_locations = detect_icon(processImg, icon_name)
                if detected_locations:
                    # Apply Non-Maximum Suppression to group overlapping icons
                    filtered_locations = non_maximum_suppression(detected_locations)

                    # Store filtered suggestions for later use
                    all_suggestions.append((icon_name, filtered_locations))

            # Draw rectangles around detected icons
            annotated_img = img.copy()  # Make a copy to draw on

            for icon_name, locations in all_suggestions:
                for pt in locations:
                    # Draw rectangle
                    cv2.rectangle(annotated_img, pt, (pt[0] + templates[icon_name].shape[1], pt[1] + templates[icon_name].shape[0]), (0, 255, 0), 2)

                    # Add text label
                    cv2.putText(
                        annotated_img, BUILDING_SUGGESTIONS[icon_name], (pt[0], pt[1] - 10),  # Position above the icon
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA
                    )

            # Show the annotated image
            cv2.imshow("Annotated Image", annotated_img)


            # Wait for 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Sleep to prevent maxing out CPU
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        cv2.destroyAllWindows()