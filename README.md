متوجه شدم. در اینجا یک متن ویژه برای صفحه اصلی مخزن شما در گیت‌هاب ارائه می‌دهم که شامل تمامی توضیحات مربوط به سه بخش مختلف پروژه شماست:

---

# Image to Emoji Conversion Project

This repository includes multiple methods for converting images into emoji representations, as well as a tool for checking and editing emoji libraries. It is optimized for Google Colab, making it easy to use and modify.

## Emoji Library Check & Edit

### Emoji Color Editor

This project provides a web page to check and edit emojis and their corresponding average colors. It allows users to interactively modify emoji colors and save the updated data as a CSV file.

**How It Works:**

1. **Emoji Data Loading**: The script loads emoji data, including unicode values and average colors, from a CSV file.
2. **Web Page Generation**: An HTML file is generated to display emojis, their colors, and corresponding RGB values.
3. **Interactive Editing**: Users can delete or edit emoji colors directly on the web page.
4. **Save Changes**: Users can save the updated emoji data as a new CSV file.

**Example Code:**

```python
# Function to load emoji data and create HTML file
emoji_data = []
with open('emojis.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        emoji_data.append((row['emoji_unicode'], tuple(map(int, row['average_color'].split()))))

# Create an HTML file to display emoji and their average colors
html_output = '''
<!DOCTYPE html>
<html lang="en">
...
</html>
'''

# Save the HTML file
with open('emoji_colors.html', 'w') as f:
    f.write(html_output)

print('HTML file created successfully!')
```

![Emojis Library Editor by Hashem Changizy](https://github.com/changizyv/image2emoji/blob/main/IMG/Screenshot%202025-01-03%20214602.png)

## Method 1 - 1x1px Image to Emoji Converter

### Image to Emoji Converter

This project provides a method to convert images into emojis. The goal is to create a colorful and fun representation of images using emojis.

**How It Works:**

1. **Emoji Data**: The script loads a set of emojis and their average colors from a CSV file.
2. **Image Processing**: It reads an input image and processes it pixel by pixel.
3. **Emoji Matching**: For each pixel, the script finds the nearest emoji based on color using a KDTree for efficient nearest neighbor search.
4. **HTML Output**: The result is saved as an HTML file displaying the image composed entirely of emojis.

**Example Code:**

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
```

## Method 2 - 3x3px Image to Emoji Converter

### Image to Emoji Converter

This project implements a method to convert images into emojis. The primary goal is to create a colorful and fun representation of images using emojis.

**How It Works:**

1. **Emoji Data Loading**: The script loads a set of emojis along with their average colors from a CSV file. Invalid emojis are handled gracefully.
2. **Image Processing**: The script reads an input image and processes it in 3x3 pixel blocks.
3. **Color Conversion**: Each 3x3 block's average color is calculated and converted from RGB to BGR format.
4. **Emoji Matching**: The script uses a KDTree to find the nearest emoji based on the average color of each block.
5. **HTML Output**: The result is saved as an HTML file displaying the image composed entirely of emojis.

**Example Code:**

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
```

---
### Contributing
We warmly invite developers, data scientists, and emoji enthusiasts to contribute to the ongoing development and enhancement of this open-source project. Your expertise and insights can help us make significant improvements and achieve our goals more efficiently.

Whether you have ideas for new features, optimizations, or improvements in the existing algorithms, we encourage you to join us. Feel free to fork the repository, submit pull requests, or open issues. Your collaboration is highly valued, and we look forward to working together to create an even better tool.

For any questions, suggestions, or feedback, please do not hesitate to reach out.

### Thank you for your interest and support
