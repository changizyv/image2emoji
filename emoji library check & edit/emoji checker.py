"""emoji checker generator- 
create html file for check and edit  Dominant color emojis library csv
Optimized for Google Colab.
By: Hashem Changizy
"""

import csv

# Load emoji data from CSV file
emoji_data = []
with open('emojis.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        emoji_data.append((row['emoji_unicode'], tuple(map(int, row['average_color'].split()))))

# Create an HTML file to display emoji and their average colors
html_output = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emoji Color Editor</title>
</head>

<body>

    <style>
        button{
            background: #2196F3;
            color: #fff;
            padding: 11px;
            border-radius: 10px;
            border: none;
            font-size: 20px;
            margin: 10px;
        }

        input{
            height: 46px;
            border-radius: 15px;
            border: none;
            background: #008828;
            text-align: center;
            color: #fff;
            font-size: 20px;
        }

        .red{
            background: #b90000;
        }

        table{margin: auto;}

       .sidebar {
        position: -webkit-sticky; 
        position: sticky;
        top: 0;
        left: 0;
        padding: 10px; 
        z-index: 1000; 
        }

    </style>
 
    <table id="emojiTable" border="1" cellpadding="10" cellspacing="0">
        <thead>
            <tr>
                <th>Emoji</th>
                <th>Color</th>
                <th>RGB Color</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <!-- Rows will be dynamically added here -->
'''

for emoji_unicode, color in emoji_data:
    emoji_char = chr(int(emoji_unicode[2:], 16))  # Convert unicode to emoji character
    color_rgb = f'{color[2]} {color[1]} {color[0]}'  # Convert BGR to RGB
    html_output += f'''
    <tr>
        <td style="font-size: 2em;">{emoji_char}</td>
        <td><div style="background-color: rgb({color[2]}, {color[1]}, {color[0]}); width: 50px; height: 50px;"></div></td>
        <td><input type="text" value="{color_rgb}"></td>
        <td>
            <button onclick="deleteRow(this)">Delete</button>
            <button onclick="editRow(this)">Edit</button>
        </td>
    </tr>
    '''

html_output += '''
        </tbody>
    </table>
    <button onclick="saveCSV()">Save as CSV</button>

    <script>
        function deleteRow(button) {
            const row = button.parentElement.parentElement;
            row.parentElement.removeChild(row);
        }

        function editRow(button) {
            const row = button.parentElement.parentElement;
            const input = row.cells[2].querySelector('input');
            const newColor = prompt('Enter new RGB color (B G R):', input.value);
            if (newColor) {
                input.value = newColor;
                const [r, g, b] = newColor.split(' ').map(Number);
                row.cells[1].querySelector('div').style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
            }
        }

        function saveCSV() {
            const rows = [['Emoji', 'Color', 'Unicode']];
            const tableRows = document.querySelectorAll('#emojiTable tbody tr');
            tableRows.forEach(row => {
                const emoji = row.cells[0].textContent.trim();
                const color = row.cells[2].querySelector('input').value.trim();
                const unicode = emoji.codePointAt(0).toString(16).toUpperCase();
                rows.push([emoji, color, `U+${unicode}`]);
            });

            let csvContent = 'data:text/csv;charset=utf-8,';
            rows.forEach(rowArray => {
                const row = rowArray.join(',');
                csvContent += row + '\\r\\n';
            });

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement('a');
            link.setAttribute('href', encodedUri);
            link.setAttribute('download', 'emoji_colors.csv');
            document.body.appendChild(link); // Required for FF
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>
'''

# Save the HTML file
with open('emoji_colors.html', 'w') as f:
    f.write(html_output)

print('HTML file created successfully!')
