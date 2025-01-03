"""img 2 emoji - method 3*3px 

Optimized for Google Colab.
Output: HTML
By: Hashem Changizy
"""

import csv
import cv2
import numpy as np
from scipy.spatial import KDTree

# Function to convert RGB to BGR
def rgb_to_bgr(color):
    r, g, b = color
    return (b, g, r)

# Load emoji data from CSV file
emoji_data = []
invalid_emojis = set()

with open('emojis.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            color = tuple(map(int, row['average_color'].split()))
            if len(color) != 3:
                raise ValueError("Incorrect number of color components")
            unicode_value = row['emoji_unicode']
            if not unicode_value:
                raise ValueError("Empty unicode value")
            bgr_color = rgb_to_bgr(color)
            emoji_data.append((unicode_value, bgr_color))
        except ValueError as e:
            print(f"Error processing row {row}: {e}")

emoji_colors = [e[1] for e in emoji_data]
try:
    emoji_tree = KDTree(emoji_colors)
    print("Emoji data loaded successfully")
except ValueError as e:
    print(f"Error creating KDTree: {e}")

# Function to find the nearest emoji based on color
def find_nearest_emoji(color):
    _, idx = emoji_tree.query(color)
    return emoji_data[idx][0]

# Function to convert unicode to emoji character and handle invalid unicodes
def unicode_to_emoji(unicode_value):
    if unicode_value in invalid_emojis:
        return None
    try:
        return chr(int(unicode_value[2:], 16))
    except ValueError:
        invalid_emojis.add(unicode_value)
        return None

# Load the input image
input_image_path = '/content/input-image.jpg'
image = cv2.imread(input_image_path)
print("Input image loaded successfully")

# Create an empty HTML file with a table
html_output = '<html><body><table cellpadding="0" cellspacing="0">'
for row_index in range(0, image.shape[0], 3):
    html_output += '<tr>'
    for col_index in range(0, image.shape[1], 3):
        block = image[row_index:row_index+3, col_index:col_index+3]
        if block.size == 0:
            continue
        average_color = block.mean(axis=(0, 1)).astype(int)  # BGR format
        dominant_color = tuple(average_color)  # Convert to tuple
        emoji_unicode = find_nearest_emoji(dominant_color)
        emoji_char = unicode_to_emoji(emoji_unicode)
        if not emoji_char:
            # Try finding a new closest emoji if the current one is invalid
            for i in range(1, len(emoji_data)):
                emoji_unicode = find_nearest_emoji(dominant_color)
                emoji_char = unicode_to_emoji(emoji_unicode)
                if emoji_char:
                    break
        if emoji_char:
            html_output += f'<td>{emoji_char}</td>'
            print(f"Processed block at row {row_index//3}, col {col_index//3} - Dominant color: {dominant_color} - Nearest emoji: {emoji_unicode}")
        else:
            html_output += '<td>?</td>'  # Placeholder for unresolved emoji
            print(f"Processed block at row {row_index//3}, col {col_index//3} - Dominant color: {dominant_color} - No valid emoji found")
    html_output += '</tr>'
html_output += '</table></body></html>'
print("HTML file creation completed")

# Save the HTML file
with open('output.html', 'w') as f:
    f.write(html_output)

print('HTML file saved successfully!')