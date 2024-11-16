from PIL import Image, ImageDraw

filepath = 'sprites/Land.png'
s = 32
img = Image.open(filepath)
size = img.size
draw = ImageDraw.Draw(img)
for x in range(int(size[0]/s)):
    for y in range(int(size[1]/s)):
        pos_x = x*s
        pos_y = y*s
        draw.line([(pos_x, pos_y), (pos_x+s, pos_y)], fill=(0,0,0), width=2)
        draw.line([(pos_x, pos_y), (pos_x, pos_y+s)], fill=(0,0,0), width=2)
img.save(f"{filepath}.grid.png")