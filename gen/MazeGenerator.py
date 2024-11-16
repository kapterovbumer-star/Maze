import random
import json

class MazeGenerator:
    def __init__(self, width: int, height: int, difficulty: int):
        self.width = width
        self.height = height
        self.difficulty = difficulty
        self.walls = {
            'v': [],  # Vertical walls
            'h': []   # Horizontal walls
        }
        self.visited = []
        self.corners = []
        self.genPos = {'x': 0, 'y': 0}
        self.lastDir = {'x': 0, 'y': 0}
        self.startpoint = None
        self.endpoint = None

    def generate(self):
        self.generateGrid()
        self.visited = [[False for _ in range(self.height)] for _ in range(self.width)]
        # Starting position
        self.genPos = {'x': 0, 'y': 0}
        self.visited[0][0] = True
        self.lastDir = {'x': 0, 'y': 0}
        self.corners = []
        # Start the random walk
        self.randomWalk()
        # Set start and end points
        self.startpoint = {'x': 0, 'y': 0}
        self.endpoint = {'x': self.width - 1, 'y': self.height - 1}

    def generateGrid(self):
        # Initialize walls
        # Vertical walls: (width + 1) columns, each with height cells
        self.walls['v'] = [
            [{'state': True} for _ in range(self.height)]
            for _ in range(self.width + 1)
        ]
        # Horizontal walls: width columns, each with (height + 1) cells
        self.walls['h'] = [
            [{'state': True} for _ in range(self.height + 1)]
            for _ in range(self.width)
        ]

    def randomWalk(self):
        while True:
            available = self.isCaseWalkable(self.genPos['x'], self.genPos['y'])
            if not available:
                if not self.hunt():
                    break
            else:
                move = random.choice(available)
                if move['x'] != self.lastDir['x'] or move['y'] != self.lastDir['y']:
                    # We just turned.
                    # Register this corner
                    self.corners.append((self.genPos['x'], self.genPos['y']))
                # Save the last direction taken
                self.lastDir = {'x': move['x'], 'y': move['y']}
                # Deactivate the wall between current and new position
                self.deactivateWallBetween(
                    self.genPos['x'], self.genPos['y'], move['x'], move['y']
                )
                # Move to new position
                self.genPos['x'] += move['x']
                self.genPos['y'] += move['y']
                self.visited[self.genPos['x']][self.genPos['y']] = True

    def hunt(self):
        if not self.corners:
            return False
        # Adjust starting index based on difficulty
        start = round(
            ((10 - self.difficulty) / 10) * (len(self.corners) - 1)
        )
        if start < 0:
            start = 0
        for index in range(start, len(self.corners)):
            x, y = self.corners[index]
            available = self.isCaseWalkable(x, y)
            if available:
                self.genPos = {'x': x, 'y': y}
                self.lastDir = {'x': 0, 'y': 0}
                # Remove used corners to prevent revisiting
                self.corners.pop(index)
                return True
            else:
                # Remove from corners as it's no longer useful
                self.corners.pop(index)
                return self.hunt()
        return False

    def isCaseWalkable(self, x, y):
        available = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, right, up, down
        random.shuffle(directions)  # Randomize direction order
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.visited[nx][ny]:
                    available.append({'x': dx, 'y': dy})
        return available if available else None

    def deactivateWallBetween(self, x, y, dx, dy):
        if dx == 1:
            # Moving right, deactivate vertical wall to the right of (x, y)
            self.walls['v'][x + 1][y]['state'] = False
        elif dx == -1:
            # Moving left, deactivate vertical wall at (x, y)
            self.walls['v'][x][y]['state'] = False
        elif dy == 1:
            # Moving down, deactivate horizontal wall below (x, y)
            self.walls['h'][x][y + 1]['state'] = False
        elif dy == -1:
            # Moving up, deactivate horizontal wall at (x, y)
            self.walls['h'][x][y]['state'] = False

    def export(self):
        buffer = {
            'start': self.startpoint,
            'end': self.endpoint
        }
        # Export vertical walls
        buffer['v'] = [
            [1 if cell['state'] else 0 for cell in col]
            for col in self.walls['v']
        ]
        # Export horizontal walls
        buffer['h'] = [
            [1 if cell['state'] else 0 for cell in row]
            for row in self.walls['h']
        ]
        return buffer
