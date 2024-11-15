from PIL import Image, ImageDraw
import json
import os

class Generator:
    def __init__(self, maze_data, maze_settings, px=0, py=0, padding=0):
        self.px = px
        self.py = py
        self.padding = padding
        
        self.settingsDir = os.path.dirname(maze_settings)

        self.maze_data = self.getJSON(maze_data)
        self.maze_settings = self.getJSON(maze_settings)

        self.width = self.maze_settings["width"]
        self.height = self.maze_settings["height"]

        # Tile coordinates for the walls & floor
        """
            ⌜─⌝
        """

        self.tile_types = {
            'corner': (16, 15),
            'corner_out': (13, 18),
            'wall': (17, 15),
            'plain_wall': (5, 16),
            'floor': (17, 16),
            'none': (0, 0),
        }


    def getJSON(self, filename):
        with open(filename, 'r') as file:
            return json.load(file)
        
    def render(self, filename="output/maze.png", theme="default"):
        tilemap = self.convertToTileMap(self.maze_data)
        self.renderTileMap(tilemap, filename, theme)
        return tilemap
        with open(f"{filename}.json", "w") as file:
            file.write(json.dumps(tilemap, indent=4).replace("NaN","null"))

        self.renderTileMap(tilemap, filename)



    def convertToTileMap(self, maze_data):
        num_rows = len(maze_data['v'])
        num_cols = len(maze_data['v'][0])
        grid_width = num_cols * 3
        grid_height = num_rows * 3
        tilemap = [[['none', 0] for _ in range(grid_width)] for _ in range(grid_height)]
        for x in range(num_cols):
            for y in range(num_rows):
                cell = self.getCell(maze_data, x, y)
                cellMap = self.getCellMap(cell)

                # Overwrite the corners
                top_left = self.getCell(maze_data, x-1, y-1)
                top_right = self.getCell(maze_data, x+1, y-1)
                bottom_left = self.getCell(maze_data, x-1, y+1)
                bottom_right = self.getCell(maze_data, x+1, y+1)

                left = self.getCell(maze_data, x-1, y)
                right = self.getCell(maze_data, x+1, y)
                top = self.getCell(maze_data, x, y-1)
                bottom = self.getCell(maze_data, x, y+1)

                TOP = 0
                RIGHT = 1
                BOTTOM = 2
                LEFT = 3
                # [top, right, bottom, left]

                # top left
                if not cell[LEFT] and not cell[TOP]:
                    cellMap[0][0] = ['corner_out', 0]

                # top right
                if not cell[RIGHT] and not cell[TOP]:
                    cellMap[2][0] = ['corner_out', 3]

                # bottom left
                if not cell[LEFT] and not cell[BOTTOM]:
                    cellMap[0][2] = ['corner_out', 1]

                # bottom right
                if not cell[RIGHT] and not cell[BOTTOM]:
                    cellMap[2][2] = ['corner_out', 2]

                for _x in range(3):
                    for _y in range(3):
                        xx = x*3 + _x
                        yy = y*3 + _y
                        tilemap[xx][yy] = cellMap[_x][_y]

        return tilemap

    # Return a boolean with wall positions around that cell
    def getCell(self, maze_data, x, y):
        num_rows = len(maze_data['v'])
        num_cols = len(maze_data['v'][0])
        if x < 0 or x >= num_rows or y < 0 or y >= num_cols:
            return [True, True, True, True]
        
        sideWalls = maze_data['v'] # side walls [x, y]
        topWalls = maze_data['h'] # top walls [x, y]
        top = topWalls[x][y]
        right = sideWalls[x+1][y] if x<num_cols-1 and x >=0 else 1
        bottom = topWalls[x][y+1] if y<num_rows-1 and y >=0 else 1
        left = sideWalls[x][y] if x > 0 else 1
        return [top, right, bottom, left]

    
    # Convert a cell wall array into a 3x3 tiled group
    def getCellMap(self, cell):
        default_tile = ['floor', 0] # tile, rotation
        [top, right, bottom, left] = cell
        output = [[default_tile,default_tile,default_tile],[default_tile,default_tile,default_tile],[default_tile,default_tile,default_tile]]
        """
            T
        L       R
            B
        """
        if top and left:
            output[0][0] = ['corner', 0]
        elif top and not left:
            output[0][0] = ['wall', 0]
        elif not top and left:
            output[0][0] = ['wall', 1]
        
        if top and right:
            output[2][0] = ['corner', 3]
        elif top and not right:
            output[2][0] = ['wall', 0]
        elif not top and right:
            output[2][0] = ['wall', 3]
        
        if bottom and right:
            output[2][2] = ['corner', 2]
        elif bottom and not right:
            output[2][2] = ['wall', 2]
        elif not bottom and right:
            output[2][2] = ['wall', 3]

        if bottom and left:
            output[0][2] = ['corner', 1]
        elif bottom and not left:
            output[0][2] = ['wall', 2]
        elif not bottom and left:
            output[0][2] = ['wall', 1]

        if top:
            output[1][0] = ['wall', 0]
        if left:
            output[0][1] = ['wall', 1]
        if bottom:
            output[1][2] = ['wall', 2]
        if right:
            output[2][1] = ['wall', 3]
        if top and left and bottom and right:
            output[1][1] = ['plain_wall', 3]
        return output # [x][y]
    

    def renderTileMap(self, tilemap, filename="output/maze.png", theme="default"):
        from PIL import Image

        tile_types = self.maze_settings["themes"][theme]
        spritesheet_filename = self.maze_settings["spritesheet"]
        sprite_filename = f"{self.settingsDir}/{spritesheet_filename}"

        # Load the sprite sheet
        sprite_sheet = Image.open(sprite_filename)
        sheet_width, sheet_height = sprite_sheet.size

        # Compute the size of each sprite
        sprite_width = sheet_width // self.width
        sprite_height = sheet_height // self.height

        # Prepare the sprites dictionary
        sprites = {}
        for tile_type, (tile_x, tile_y) in tile_types.items():
            sprites[tile_type] = sprite_sheet.crop((
                tile_x * sprite_width + self.px,
                tile_y * sprite_height + self.py,
                (tile_x + 1) * sprite_width - self.px,
                (tile_y + 1) * sprite_height - self.py
            ))
        actual_sprite_width = sprite_width - (self.px*2)
        actual_sprite_height = sprite_height - (self.py*2)

        grid_width = len(tilemap)
        grid_height = len(tilemap[0])

        maze_width = grid_width * actual_sprite_width
        maze_height = grid_height * actual_sprite_height

        # Create the maze image
        maze_image = Image.new('RGBA', (maze_width, maze_height))

        draw = ImageDraw.Draw(maze_image)
        # Render the maze
        for x in range(grid_width):
            for y in range(grid_height):
                tile_type = tilemap[x][y][0]
                tile_rotation = tilemap[x][y][1]*90

                pos_x = x * actual_sprite_width 
                pos_y = y * actual_sprite_height

                if tile_type in sprites:
                    rotated_tile = sprites[tile_type].rotate(tile_rotation, expand=True)
                    maze_image.paste(rotated_tile, (pos_x, pos_y))
                else:
                    # If tile type is not recognized, default to floor
                    maze_image.paste(sprites['floor'], (pos_x, pos_y))
                #if y % 3 == 0:
                #    draw.line([(pos_x, pos_y), (pos_x+actual_sprite_width*3, pos_y)], fill=(0,0,0), width=2)
                #if x % 3 == 0:
                #    draw.line([(pos_x, pos_y), (pos_x, pos_y+actual_sprite_height*3)], fill=(0,0,0), width=2)

        # Save the maze image
        maze_image.save(filename)

