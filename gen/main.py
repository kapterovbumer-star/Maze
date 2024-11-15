from Generator import *
import json

gen = Generator(maze_data='maze.json', maze_settings='sprites/Grass.json', px=1, py=1, padding=0)
renderResponse = gen.render(filename="output/maze-6.png", theme="dirt")

