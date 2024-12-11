import mss
import numpy as np
import cv2
import pyautogui

# Define the region for capturing the screen (game window region)
game_window_region = (0, 100, 1660, 1080)  # Adjust this based on the game window coordinates


# Function to check if the mouse is hovering over a specific monkey
def detect_hovered_monkey(frame, monkey_images):
    hovered_monkey = None
    # Convert the frame to grayscale before performing template matching
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    for monkey_name, monkey_image in monkey_images.items():
        # Convert monkey image to grayscale for template matching
        monkey_gray = cv2.cvtColor(monkey_image, cv2.COLOR_BGR2GRAY)
        
        # Ensure both the frame and monkey images are single-channel (grayscale) and 8-bit
        monkey_gray = np.uint8(monkey_gray)
        frame_gray = np.uint8(frame_gray)
        
        # Match the template of the monkey on the frame
        result = cv2.matchTemplate(frame_gray, monkey_gray, cv2.TM_CCOEFF_NORMED)
        
        # Threshold to detect the template
        threshold = 0.8  # You can adjust this based on accuracy
        locations = np.where(result >= threshold)
        
        for pt in zip(*locations[::-1]):
            # Draw a rectangle around the matched area
            cv2.rectangle(frame, pt, (pt[0] + monkey_image.shape[1], pt[1] + monkey_image.shape[0]), (0, 255, 0), 2)
            print(f"Hovered over {monkey_name}")
            hovered_monkey = monkey_name  # Set the hovered monkey
    return frame, hovered_monkey


# Load template images for each monkey (These images must be captured from the game)
dart_monkey_img = cv2.imread('monkeys/dart_monkey.png')
ice_monkey_img = cv2.imread('monkeys/ice_monkey.png')
cannon_monkey_img = cv2.imread('monkeys/cannon_monkey.png')

# Store the images in a dictionary
monkey_images = {
    'dart': dart_monkey_img,
    'ice': ice_monkey_img,
    'cannon': cannon_monkey_img
}


def generate_heatmap(frame, grid_rows, grid_cols, monkey_type):
    height, width = frame.shape[:2]
    cell_width = width // grid_cols
    cell_height = height // grid_rows
    
    heatmap = np.zeros((grid_rows, grid_cols))
    
    # Example logic for heatmap generation based on tower type
    if monkey_type == "dart":
        # Heatmap will highlight the best areas for Dart Monkeys (e.g., near straight paths)
        track_color = (177, 195, 170)  # Track color approximation
        
        for row in range(grid_rows):
            for col in range(grid_cols):
                x_start = col * cell_width
                y_start = row * cell_height
                cell = frame[y_start:y_start + cell_height, x_start:x_start + cell_width]
                
                # Count track pixels in this cell
                track_pixels = np.sum(np.all(np.abs(cell - track_color) < 30, axis=-1))
                heatmap[row, col] = track_pixels
    
    elif monkey_type == "ice":
        # Heatmap for Ice Monkey: highlight larger areas for freezing bloons
        # For example, areas where multiple paths converge
        for row in range(grid_rows):
            for col in range(grid_cols):
                x_start = col * cell_width
                y_start = row * cell_height
                cell = frame[y_start:y_start + cell_height, x_start:x_start + cell_width]
                
                ice_area_pixels = np.sum(np.all(cell == [255, 255, 255], axis=-1))  # Example: white areas for ice
                heatmap[row, col] = ice_area_pixels
    
    elif monkey_type == "cannon":
        # Heatmap for Cannon Monkey: Areas with large space for splash damage
        for row in range(grid_rows):
            for col in range(grid_cols):
                x_start = col * cell_width
                y_start = row * cell_height
                cell = frame[y_start:y_start + cell_height, x_start:x_start + cell_width]
                
                cannon_area_pixels = np.sum(np.all(cell == [0, 0, 255], axis=-1))  # Example: red areas for splash damage
                heatmap[row, col] = cannon_area_pixels

    # Normalize heatmap to be between 0 and 255
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    
    return heatmap

# Calculate and overlay heatmap
with mss.mss() as sct:
    while True:
        screenshot = sct.grab(game_window_region)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        
        # Detect hovered monkey and generate appropriate heatmap
        frame, hovered_monkey = detect_hovered_monkey(frame, monkey_images)
        
        if hovered_monkey:
            # Generate the heatmap based on the hovered monkey
            heatmap = generate_heatmap(frame, 18, 18, hovered_monkey)
            
            # Resize heatmap to match the frame size
            heatmap_resized = cv2.resize(heatmap, (frame.shape[1], frame.shape[0]))
            
            # Convert heatmap to color
            heatmap_colored = cv2.applyColorMap(heatmap_resized.astype(np.uint8), cv2.COLORMAP_JET)
            
            # Ensure frame is uint8 and add the heatmap overlay
            overlay = cv2.addWeighted(frame, 0.7, heatmap_colored, 0.3, 0)
            
            # Display overlay
            cv2.imshow("Live Game with Heatmap", overlay)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
