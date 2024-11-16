from PIL import Image, ImageDraw, ImageFont

filepath = 'sprites/Roads.png'
s = 16  # Size of each grid cell
img = Image.open(filepath)
size = img.size
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()  # Load default font

num_columns = int(size[0] / s)
num_rows = int(size[1] / s)

# Draw grid lines
for x in range(num_columns):
    for y in range(num_rows):
        pos_x = x * s
        pos_y = y * s

        # Draw vertical and horizontal lines
        draw.line([(pos_x, pos_y), (pos_x + s, pos_y)], fill=(0, 0, 0), width=2)
        draw.line([(pos_x, pos_y), (pos_x, pos_y + s)], fill=(0, 0, 0), width=2)

# Add column numbers at the top
for x in range(num_columns):
    pos_x = x * s
    text = str(x)
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = pos_x + (s - text_width) / 2
    text_y = 5  # Slight offset from the top
    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)

# Add row numbers on the left
for y in range(num_rows):
    pos_y = y * s
    text = str(y)
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = 5  # Slight offset from the left
    text_y = pos_y + (s - text_height) / 2
    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)

img.save(f"{filepath}.grid.png")
