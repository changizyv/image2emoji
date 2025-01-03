# Image to Emoji Converter

This project implements a method to convert images into emojis, optimized for Google Colab. The primary goal is to create a colorful and fun representation of images using emojis.

## How It Works

1. **Emoji Data Loading**: The script loads a set of emojis along with their average colors from a CSV file. Invalid emojis are handled gracefully.
2. **Image Processing**: The script reads an input image and processes it in 3x3 pixel blocks.
3. **Color Conversion**: Each 3x3 block's average color is calculated and converted from RGB to BGR format.
4. **Emoji Matching**: The script uses a KDTree to find the nearest emoji based on the average color of each block.
5. **HTML Output**: The result is saved as an HTML file displaying the image composed entirely of emojis.

## Example Code

Here’s a brief snippet of the core functionality:

```python
# Function to find the nearest emoji based on color
def find_nearest_emoji(color):
    _, idx = emoji_tree.query(color)
    return emoji_data[idx][0]

# Create an HTML file with the emoji representation
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
        else:
            html_output += '<td>?</td>'
    html_output += '</tr>'
html_output += '</table></body></html>'
