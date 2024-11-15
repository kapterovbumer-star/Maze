from Generator import *
import json

gen = Generator(grid=False, maze_data='maze.json', maze_settings='sprites/Grass.json')
renderResponse = gen.render(filename="output/maze-test.png", theme="dirt")

