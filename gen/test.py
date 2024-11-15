from Generator import *
import json

def getJSON(filename):
    with open(filename, 'r') as file:
        return json.load(file)


maze_data = getJSON('maze.json')

gen = Generator()
cell = gen.getCell(maze_data, 0, 2)
cellMap = gen.getCellMap(cell)

renderResponse = gen.renderTileMap(filename="output/maze-5.png", tilemap=cellMap)

print(renderResponse)
