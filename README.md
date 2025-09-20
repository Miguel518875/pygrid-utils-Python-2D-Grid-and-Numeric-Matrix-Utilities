# Pygrid utils - Python 2D Grid and Numeric Matrix Utils

Python library for working with **2D grids** and **numeric matrices**.  
Provides easy-to-use classes for generic grids (`Grid`) and numeric grids (`NumericGrid`) with methods for reading, editing, iterating, and working with adjacent cells. Ideal for building grid-based games, simulations, or puzzles like Minesweeper.

---

## Features

- Create 2D string-based grids (`Grid`)
- Create 2D numeric grids (`NumericGrid`)
- Read and edit cells using 1-indexed coordinates
- Find all occurrences of a value in the grid
- Query adjacent cells (like a numpad layout)
- Iterate over grid or matrix values
- Perform arithmetic operations on numeric grids
- Freeze a grid into an immutable tuple
- Convert a grid to a dictionary of coordinates → value

---

## Installation

You can clone the repository and use it locally:

```bash
git clone https://github.com/Miguel518875/pygrid-utils.git
cd pygrid-utils
Then import in Python:

python
Copiar código
from pygrid_utils import Grid, NumericGrid
(Note: not yet published to PyPI.)

Usage Examples
Grid Example
python
Copiar código
from pygrid_utils import Grid

grid = Grid([
    ["", "", ""],
    ["", "X", ""],
    ["", "", ""]
])

print(grid.read((2, 2)))  # Output: X
grid.edit((1, 1), "O")
print(grid.find_all("X")) # Output: ((2, 2),)
NumericGrid Example
```
### Example code:
```python
from pygrid_utils import NumericGrid

matrix = NumericGrid([
    [1, 1, 1],
    [1, 9, 1],
    [1, 1, 1]
])

matrix.increment_neighbors((2, 2), amount=1)
print(matrix.matrix)
# Output: numbers around the 9 incremented by 1
```
License:
MIT License

Author:
Created by [Miguel518875](https://github.com/Miguel518875)
