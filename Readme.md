# Image to Emoji Converter

This project provides a method to convert images into emojis, optimized for Google Colab. The goal is to create a colorful and fun representation of images using emojis.

## How It Works

1. **Emoji Data**: The script loads a set of emojis and their average colors from a CSV file.
2. **Image Processing**: It reads an input image and processes it pixel by pixel.
3. **Emoji Matching**: For each pixel, the script finds the nearest emoji based on color using a KDTree for efficient nearest neighbor search.
4. **HTML Output**: The result is saved as an HTML file displaying the image composed entirely of emojis.

## Example

Here’s a small snippet of the code:

```python
# Function to find the nearest emoji based on color
def find_nearest_emoji(color):
    _, idx = emoji_tree.query(color)
    return emoji_data[idx][0]

# Create an HTML file with the emoji representation
html_output = '<html><body style="background:#000"><table cellpadding="0" cellspacing="0" style="">'
for row_index, row in enumerate(image):
    html_output += '<tr>'
    for col_index, pixel in enumerate(row):
        dominant_color = tuple(pixel)  # BGR format
        emoji_unicode = find_nearest_emoji(dominant_color)
        emoji_char = chr(int(emoji_unicode[2:], 16))  # Convert unicode to emoji character
        html_output += f'<td>{emoji_char}</td>'
    html_output += '</tr>'
html_output += '</table></body></html>'
