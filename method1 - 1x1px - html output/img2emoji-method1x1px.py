"""img 2 emoji - method 3*3px 

Optimized for Google Colab.
Output: HTML
By: Hashem Changizy
"""

# progressing 1*1 picxels to 1 emojie
import csv
import cv2
import numpy as np
from scipy.spatial import KDTree

# Load emoji data from CSV file
emoji_data = []
with open('emojis.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        emoji_data.append((row['emoji_unicode'], tuple(map(int, row['average_color'].split()))))

emoji_colors = [e[1] for e in emoji_data]
emoji_tree = KDTree(emoji_colors)
print("Emoji data loaded successfully")

# Function to find the nearest emoji based on color
def find_nearest_emoji(color):
    _, idx = emoji_tree.query(color)
    return emoji_data[idx][0]

# Load the input image
input_image_path = '/content/input-image.jpg'
image = cv2.imread(input_image_path)
print("Input image loaded successfully")

# Create an empty HTML file with a table
html_output = '<html><body style="background:#000"><table cellpadding="0" cellspacing="0" style="">'
for row_index, row in enumerate(image):
    html_output += '<tr>'
    for col_index, pixel in enumerate(row):
        dominant_color = tuple(pixel)  # BGR format
        emoji_unicode = find_nearest_emoji(dominant_color)
        emoji_char = chr(int(emoji_unicode[2:], 16))  # Convert unicode to emoji character
        html_output += f'<td>{emoji_char}</td>'
        print(f"Processed pixel at row {row_index}, col {col_index} - Dominant color: {dominant_color} - Nearest emoji: {emoji_unicode}")
    html_output += '</tr>'
html_output += '</table></body></html>'
print("HTML file creation completed")

# Save the HTML file
with open('output.html', 'w') as f:
    f.write(html_output)

print('HTML file saved successfully!')