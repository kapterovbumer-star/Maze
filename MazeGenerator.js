class MazeGenerator {
  constructor(options = {}) {
    this.width = options.width || 25;
    this.height = options.height || 25;
    this.start = Array.isArray(options.start) ? options.start : [0, 0];
    this.end = Array.isArray(options.end) ? options.end : [this.width - 1, this.height - 1];
    const diff = options.difficulty == null ? 10 : options.difficulty;
    this.difficulty = Math.max(1, Math.min(10, diff));
    this.walls = { h: [], v: [] };
  }

  // Build initial wall grid
  _initWalls() {
    // horizontal walls: width columns, height+1 rows
    this.walls.h = Array.from({ length: this.width }, () => Array(this.height + 1).fill(true));
    // vertical walls: width+1 columns, height rows
    this.walls.v = Array.from({ length: this.width + 1 }, () => Array(this.height).fill(true));
  }

  // Check unvisited neighbours from (x,y)
  _walkableNeighbors(x, y) {
    const dirs = [];
    if (x + 1 < this.width && !this.visited[x + 1][y]) dirs.push({ x: 1, y: 0 });
    if (x - 1 >= 0 && !this.visited[x - 1][y]) dirs.push({ x: -1, y: 0 });
    if (y + 1 < this.height && !this.visited[x][y + 1]) dirs.push({ x: 0, y: 1 });
    if (y - 1 >= 0 && !this.visited[x][y - 1]) dirs.push({ x: 0, y: -1 });
    return dirs;
  }

  // Backtracking step
  _hunt() {
    if (this.corners.length === 0) return false;
    const start = Math.round(((10 - this.difficulty) / 10) * (this.corners.length - 1));
    for (let i = Math.max(0, start); i < this.corners.length; i++) {
      const [cx, cy] = this.corners[i];
      if (this._walkableNeighbors(cx, cy).length > 0) {
        this.genPos = { x: cx, y: cy };
        return true;
      }
      this.corners.splice(i, 1);
      i--;
    }
    return this.corners.length > 0 ? this._hunt() : false;
  }

  _removeWall(from, to) {
    if (to.x === from.x + 1) this.walls.v[from.x + 1][from.y] = false;
    if (to.x === from.x - 1) this.walls.v[from.x][from.y] = false;
    if (to.y === from.y + 1) this.walls.h[from.x][from.y + 1] = false;
    if (to.y === from.y - 1) this.walls.h[from.x][from.y] = false;
  }

  // Recursive walk until all cells are visited
  _randomWalk() {
    while (true) {
      const available = this._walkableNeighbors(this.genPos.x, this.genPos.y);
      if (available.length === 0) {
        if (!this._hunt()) return;
        continue;
      }
      const move = available[Math.floor(Math.random() * available.length)];
      if (move.x !== this.lastDir.x || move.y !== this.lastDir.y) {
        this.corners.push([this.genPos.x, this.genPos.y]);
      }
      const prev = { x: this.genPos.x, y: this.genPos.y };
      this.lastDir = { x: move.x, y: move.y };
      this.genPos.x += move.x;
      this.genPos.y += move.y;
      this.visited[this.genPos.x][this.genPos.y] = true;
      this._removeWall(prev, this.genPos);
    }
  }

  generate() {
    this._initWalls();
    this.visited = Array.from({ length: this.width }, () => Array(this.height).fill(false));
    this.corners = [];
    this.genPos = { x: this.start[0], y: this.start[1] };
    this.lastDir = { x: 0, y: 0 };
    this.visited[this.genPos.x][this.genPos.y] = true;
    this._randomWalk();
    return this.export();
  }

  export() {
    const h = this.walls.h.map(col => col.map(v => (v ? 1 : 0)));
    const v = this.walls.v.map(col => col.map(v => (v ? 1 : 0)));
    return {
      start: { x: this.start[0], y: this.start[1] },
      end: { x: this.end[0], y: this.end[1] },
      h,
      v,
    };
  }
}

module.exports = MazeGenerator;


var maze = new MazeGenerator();
console.log(maze.generate());