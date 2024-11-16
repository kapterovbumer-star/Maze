from Generator import *
from MazeGenerator import *
from PdfBuilder import *
import json

def create_2d_array(width, height, default_value):
    """Create a 2D array of given dimensions with a default value."""
    return [[default_value for _ in range(width)] for _ in range(height)]

def paste_array(target, smaller_array, x, y):
    """Paste the smaller array into the target array at the given top-left coordinate (x, y)."""
    for i in range(len(smaller_array)):  # Rows in smaller array
        for j in range(len(smaller_array[i])):  # Columns in smaller array
            target_y = y + i
            target_x = x + j
            # Ensure within bounds of target array
            if 0 <= target_y < len(target) and 0 <= target_x < len(target[0]):
                target[target_y][target_x] = smaller_array[i][j]

ratio = 1.3
width = 20
height = int(width*ratio)


gateway = [
    [["wall", 0], ["floor", 0], ["wall", 2]],
    [["wall", 0], ["floor", 0], ["wall", 2]],
    [["wall", 0], ["floor", 0], ["wall", 2]],
]


mg = MazeGenerator(width=width, height=height, difficulty=5)
mg.generate()
maze_data = mg.export()
gen = Generator(grid=False, maze_data=maze_data, maze_settings='sprites/Grass.json')
tilemap = gen.convertToTileMap(maze_data)


final_width = width*3+6
final_height = height*3

water_array = create_2d_array(final_height, final_width, ["none", 0])

paste_array(water_array, tilemap, 0, 3)
paste_array(water_array, gateway, 0, 0)
paste_array(water_array, gateway, final_height-3, final_width-3)

gen.renderTileMap(water_array, filename=f"output/paste.png", theme="water")

with open(f"output/paste.json", "w") as file:
    file.write(json.dumps(water_array).replace("NaN","null"))