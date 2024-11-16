from Generator import *
from MazeGenerator import *
import json


mg = MazeGenerator(width=10, height=10, difficulty=8)
mg.generate()
maze_data = mg.export()
print('h length:', len(maze_data['h']), 'subarrays length:', len(maze_data['h'][0]))
print('v length:', len(maze_data['v']), 'subarrays length:', len(maze_data['v'][0]))
print(json.dumps(maze_data))

gen = Generator(grid=False, maze_data=maze_data, maze_settings='sprites/Grass.json')
renderResponse = gen.render(filename="output/maze-gen.png", theme="water")
