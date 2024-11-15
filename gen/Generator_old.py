from PIL import Image
import json

class Generator:
    def __init__(self, width=24, height=30, sprite_filename="sprites/megaman.png"):
        self.width = width
        self.height = height
        self.sprite_filename = sprite_filename
        # Tile coordinates for the walls & floor
        """
            ⌜─⌝
            | |
            ⌞_⌟
        """
        self.config = [
            (4, 5),  # top-left corner
            (5, 5),  # horizontal wall
            (6, 5),  # top-right corner

            (4, 6),  # vertical wall (left)
            (5, 6),  # floor tile
            (6, 6),  # vertical wall (right)

            (4, 7),  # bottom-left corner
            (5, 7),  # horizontal wall
            (6, 7),  # bottom-right corner

            (0, 5), # Plain wall
        ]
        # Map tile types to positions in self.config
        self.tile_types = {
            'top_left': (4, 5),
            'top_wall': (5, 5),
            'top_right': (6, 5),

            'left_wall': (4, 6),
            'floor': (5, 6),
            'right_wall': (6, 6),

            'bottom_left': (4, 7),
            'bottom_wall': (5, 7),
            'bottom_right': (6, 7),

            'wall': (0, 5),  # Default wall tile
        }
    
    def loadSquare(self, x, y, wall):
        self.tile_types = {
            'top_left': (x+0, y+0),
            'top_wall': (x+1, y+0),
            'top_right': (x+2, y+0),

            'left_wall': (x+0, y+1),
            'floor': (x+1, y+1),
            'right_wall': (x+2, y+1),

            'bottom_left': (x+0, y+2),
            'bottom_wall': (x+1, y+2),
            'bottom_right': (x+2, y+2),

            'wall': wall,  # Default wall tile
        }
    
    def renderCell(self, cell):
        mapping = {

        }

    def setSpriteConfig(self, config):
        self.config = config

    def render(self, map_data, filename="output/maze.png"):
        tilemap = self.convertToTileMap(map_data)

        with open(f"{filename}.json", "w") as file:
            file.write(json.dumps(tilemap, indent=4).replace("NaN","null"))

        self.renderTileMap(tilemap, filename)



    def convertToTileMap(self, map_data):
        num_rows = len(map_data['v'])
        num_cols = len(map_data['v'][0])
    
    def convertToTileMap_old(self, map_data):
        num_rows = len(map_data['v'])
        num_cols = len(map_data['v'][0])
        
        # Create a larger grid to accommodate walls between cells
        grid_width = num_cols * 2 + 1
        grid_height = num_rows * 2 + 1

        # Initialize the tilemap with walls
        tilemap = [['wall' for _ in range(grid_width)] for _ in range(grid_height)]

        # Map the maze data into the tilemap
        for y in range(num_rows):
            for x in range(num_cols):
                grid_x = x * 2 + 1
                grid_y = y * 2 + 1
                tilemap[grid_y][grid_x] = 'floor'

                # Check for passage to the right
                if x < num_cols - 1:
                    if map_data['v'][y][x] == 0:
                        tilemap[grid_y][grid_x + 1] = 'floor'

                # Check for passage below
                if y < num_rows - 1:
                    if map_data['h'][y][x] == 0:
                        tilemap[grid_y + 1][grid_x] = 'floor'

        # Determine wall tiles based on surrounding tiles
        for y in range(grid_height):
            for x in range(grid_width):
                if tilemap[y][x] != 'floor':
                    # Determine walls around the current tile
                    walls = {
                        'up': y > 0 and tilemap[y - 1][x] != 'floor',
                        'down': y < grid_height - 1 and tilemap[y + 1][x] != 'floor',
                        'left': x > 0 and tilemap[y][x - 1] != 'floor',
                        'right': x < grid_width - 1 and tilemap[y][x + 1] != 'floor'
                    }
                    if walls['up'] and not walls['right'] and not walls['down'] and walls['left']:
                        tilemap[y][x] = 'top_left'
                    elif walls['up'] and not walls['right'] and not walls['down'] and not walls['left']:
                        tilemap[y][x] = 'top_wall'
                    elif walls['up'] and walls['right'] and not walls['down'] and not walls['left']:
                        tilemap[y][x] = 'top_right'

                    elif not walls['up'] and not walls['right'] and not walls['down'] and walls['left']:
                        tilemap[y][x] = 'left_wall'
                    elif not walls['up'] and not walls['right'] and not walls['down'] and not walls['left']:
                        tilemap[y][x] = 'floor'
                    elif not walls['up'] and walls['right'] and not walls['down'] and not walls['left']:
                        tilemap[y][x] = 'right_wall'

                    elif not walls['up'] and not walls['right'] and walls['down'] and walls['left']:
                        tilemap[y][x] = 'bottom_left'
                    elif not walls['up'] and not walls['right'] and walls['down'] and not walls['left']:
                        tilemap[y][x] = 'bottom_wall'
                    elif not walls['up'] and walls['right'] and walls['down'] and not walls['left']:
                        tilemap[y][x] = 'bottom_right'

                    elif not walls['up'] and not walls['right'] and not walls['down'] and not walls['left']:
                        tilemap[y][x] = 'wall'

        return tilemap

    def renderTileMap(self, tilemap, filename="output/maze.png"):
        from PIL import Image

        # Load the sprite sheet
        sprite_sheet = Image.open(self.sprite_filename)
        sheet_width, sheet_height = sprite_sheet.size

        # Compute the size of each sprite
        sprite_width = sheet_width // self.width
        sprite_height = sheet_height // self.height

        # Prepare the sprites dictionary
        sprites = {}
        for tile_type, (tile_x, tile_y) in self.tile_types.items():
            sprites[tile_type] = sprite_sheet.crop((
                tile_x * sprite_width,
                tile_y * sprite_height,
                (tile_x + 1) * sprite_width,
                (tile_y + 1) * sprite_height
            ))

        grid_height = len(tilemap)
        grid_width = len(tilemap[0])

        maze_width = grid_width * sprite_width
        maze_height = grid_height * sprite_height

        # Create the maze image
        maze_image = Image.new('RGBA', (maze_width, maze_height))

        # Render the maze
        for y in range(grid_height):
            for x in range(grid_width):
                tile_type = tilemap[y][x]
                pos_x = x * sprite_width
                pos_y = y * sprite_height

                if tile_type in sprites:
                    maze_image.paste(sprites[tile_type], (pos_x, pos_y))
                else:
                    # If tile type is not recognized, default to floor
                    maze_image.paste(sprites['floor'], (pos_x, pos_y))

        # Save the maze image
        maze_image.save(filename)
