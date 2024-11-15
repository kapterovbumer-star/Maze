Map example:
{"start":{"x":0,"y":0},"end":{"x":11,"y":11},"v":[[1,1,1,1,1,1,1,1,1,1,1,1],[0,0,1,1,1,1,1,0,0,0,1,0],[0,0,1,1,1,1,0,1,1,1,0,1],[0,0,0,0,0,0,0,0,1,0,1,0],[0,1,1,1,1,0,1,1,0,1,1,0],[1,0,0,1,0,0,0,0,1,1,0,0],[0,0,1,1,0,0,0,1,0,0,1,0],[0,1,0,1,1,1,1,1,1,1,0,0],[0,1,1,0,0,1,0,1,1,1,1,0],[0,0,0,1,0,1,0,1,0,0,0,1],[0,1,1,0,1,1,1,1,0,0,1,0],[0,0,0,1,1,0,0,0,1,0,0,0]],"h":[[1,0,0,0,0,0,0,0,1,1,0,0],[1,0,0,0,0,0,0,1,0,1,0,1],[1,1,1,0,1,0,1,1,0,0,1,0],[1,1,0,1,0,1,1,0,0,1,0,0],[1,0,1,0,0,1,1,0,1,0,0,1],[1,0,1,0,1,1,1,1,0,1,0,1],[1,1,1,0,0,1,0,1,0,1,0,1],[1,0,0,1,0,1,0,0,0,0,0,1],[1,1,1,0,1,0,0,0,0,1,0,1],[1,0,1,0,1,0,1,0,1,1,1,0],[1,0,0,1,0,0,1,1,0,1,1,1],[1,0,1,0,0,0,1,0,0,0,1,0]]}


How to read the map:
The map represents a maze.
The start & end positions are specify by the `start` & `end` properties.

The maze itself is encoded as a list of walls: 0 = no wall, 1 = wall
The vertical walls (walls between columns) are encoded line by line in property `v`. They should be rendered as 2 tiles side by side (one for each side of the wall)
The horizontal walls (walls between rows) are encoded line by line in property `h`. They should be rendered as 2 tiles on top of each others (one for each side of the wall)

The class constructor takes in the spritesheet filename, and the sheet's width & height measured in sprites.
The spritesheet is made up of square sprites placed side by side.
The actual pixel width & height of each sprite must be calculated as `pixel_width(sprite_filename)/width`, `pixel_height(sprite_filename)/height`.

It should render the maze in a png and save it.