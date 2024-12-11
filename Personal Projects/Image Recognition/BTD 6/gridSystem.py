import cv2
import numpy as np
import matplotlib.pyplot as plt


#Load the image provided by the user
from PIL import Image

# File path to the uploaded image
file_path = "maps/monkeymedow.PNG"

# Open the image to analyze its dimensions
map_image = Image.open(file_path)
map_image_dimensions = map_image.size

map_image_dimensions


# Crop the image to exclude UI elements

# Define the cropping box for the playable area:
# Left, Top, Right, Bottom (excluding the right panel and bottom-right buttons)
crop_box = (0, 100, 1660, 1080)  # Exclude right 470px and bottom-right buttons

# Crop the image
playable_area = map_image.crop(crop_box)

# Save dimensions of the cropped playable area for grid generation
playable_area_dimensions = playable_area.size

# Show cropped playable area dimensions
playable_area_dimensions

# Convert the cropped playable area to a numpy array
playable_area_array = np.array(playable_area)

# Define the grid dimensions (rows and columns)
grid_rows = 18
grid_cols = 18

# Calculate cell width and height
cell_width = playable_area_dimensions[0] // grid_cols
cell_height = playable_area_dimensions[1] // grid_rows

# Create a copy of the playable area for grid overlay
gridded_map = playable_area_array.copy()

# Draw grid lines
for row in range(0, playable_area_dimensions[1], cell_height):
    cv2.line(gridded_map, (0, row), (playable_area_dimensions[0], row), (255, 0, 0), 1)  # Horizontal lines

for col in range(0, playable_area_dimensions[0], cell_width):
    cv2.line(gridded_map, (col, 0), (col, playable_area_dimensions[1]), (255, 0, 0), 1)  # Vertical lines

# Display the result
plt.figure(figsize=(12, 8))
plt.imshow(cv2.cvtColor(gridded_map, cv2.COLOR_BGR2RGB))
plt.title("Gridded Playable Area")
plt.axis("off")
plt.show()