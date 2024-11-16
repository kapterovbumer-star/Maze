from Generator import *
import json

gen = Generator(grid=False, maze_data='maze-medium.json', maze_settings='sprites/Grass.json')
renderResponse = gen.render(filename="output/maze-7.png", theme="water")

