# Maze Generator Algorithm

This project implements the "Loutre-Hunter" maze generator. The main idea is to perform a randomized depth-first search and backtrack using a list of previously visited turning points called `corners`. Difficulty tunes how far back in that list the algorithm looks when backtracking.

Algorithm overview:

1. **Grid initialization**
   - Build vertical and horizontal wall arrays so every cell is surrounded by walls.
   - A `visited[x][y]` matrix keeps track of explored cells.
   - `corners` holds coordinates where a direction change happened.

2. **Random Walk**
   - From the current position, collect all unvisited neighbouring cells (up, down, left, right).
   - If no unvisited neighbour is found, start `hunt`.
   - Otherwise choose one neighbour at random, remove the wall between the cells and mark the new cell as visited.
   - If movement direction changed, push the previous cell on the `corners` stack.
   - Continue the walk recursively.

3. **Hunt**
   - Select a cell from `corners` according to `difficulty` (1 uses recent corners, 10 uses the earliest ones).
   - If that cell still has unvisited neighbours, resume the random walk from there.
   - Otherwise remove it from `corners` and repeat the search.
   - The process stops when every cell has been visited.

The algorithm always creates a perfect maze with a single unique path between any two cells. Difficulty adjusts how often the walk backtracks to older turning points, which affects corridor length and maze complexity.
