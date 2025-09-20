from __future__ import annotations
from math import sqrt
from typing import Literal, Iterator, Any, Union, Tuple, List, Dict

class Grid:
    """
    A generic 2D grid container. Supports iteration, reading, editing, and adjacency queries.
    """
    def __new__(cls, grid_data: Union[List[List[str]], Grid]) -> object:
        return object.__new__(cls)
        
    def __init__(self, grid_data: Union[List[List[str]], Grid]) -> None:
        if isinstance(grid_data, Grid):
            grid_data = grid_data.grid
        self.grid: List[List[str]] = grid_data

    def __call__(self, coordinates: Tuple[int, int]) -> str:
        return self.read(coordinates)

    def __iter__(self) -> Iterator[str]:
        for row in self.grid:
            for cell in row:
                yield cell

    def __getitem__(self, row: int) -> List[str]:
        return self.grid[row]

    def __repr__(self) -> str:
        return str(self.grid)

    def __str__(self) -> str:
        return '"' + '", "'.join(cell for row in self.grid for cell in row) + '"'

    def __hash__(self) -> int:
        return hash(self.freeze())

    def __eq__(self, other: Union[Grid, List[List[str]]]) -> bool:
        other = Grid(other)  # pyright: ignore[reportAssignmentType] # allow comparison to raw list
        return self.freeze() == other.freeze() # pyright: ignore[reportAttributeAccessIssue]

    def __ne__(self, other: Grid) -> bool:
        return not self.__eq__(other)

    # 🔹 Helper: normalize 1-indexed coordinates for internal access
    def _normalize_coords(self, coords: Tuple[int, int]) -> Tuple[int, int]:
        x, y = coords
        if x < 1 or y < 1:
            raise IndexError("Coordinates must be positive integers starting from 1.")
        return -x, -y

    def edit(self, coords: Tuple[int, int], new_value: str, mode: Literal['edit', 'return edited'] = 'edit') -> Union[None, List[List[str]]]:
        x, y = self._normalize_coords(coords)
        if mode == 'edit':
            self.grid[y][x] = new_value
        else:
            grid_copy = self.grid.copy()
            grid_copy[y][x] = new_value
            return grid_copy

    def read(self, coords: Tuple[int, int]) -> str:
        x, y = self._normalize_coords(coords)
        return self.grid[y][x]

    def find_all(self, value: str) -> Tuple[Tuple[int, int], ...]:
        """
        Returns all coordinates (1-indexed) where `value` appears.
        """
        matches = []
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == value:
                    matches.append((j + 1, i + 1))
        return tuple(matches)

    def adjacents(self, coords: Tuple[int, int], location: int = 0, mode: Literal['coordinates', 'value'] = 'value') -> Union[Tuple[int, int], str, Tuple[Union[Tuple[int,int], str], ...]]:
        """
        Returns adjacent cells of a coordinate. Location is from numpad (1-9, skip 5).
        """
        deltas = {
            1: (-1, 1), 2: (0, 1), 3: (1, 1),
            4: (-1, 0), 6: (1, 0),
            7: (-1, -1), 8: (0, -1), 9: (1, -1)
        }

        x, y = self._normalize_coords(coords)
        if location:
            dx, dy = deltas[location]
            nx, ny = x + dx, y + dy
            return (-nx, -ny) if mode == 'coordinates' else self.grid[ny][nx]
        else:
            return tuple(self.adjacents(coords, i, mode) for i in range(1, 10) if i != 5) # pyright: ignore[reportReturnType]

    def to_dict(self) -> Dict[Tuple[int, int], str]:
        return {(j, i): cell for i, row in enumerate(self.grid) for j, cell in enumerate(row)}

    def freeze(self) -> Tuple[Tuple[str, ...], ...]:
        return tuple(tuple(row) for row in self.grid)

    @classmethod
    def from_list(cls, grid_data: List[List[str]]) -> Grid:
        return cls(grid_data)


class NumericGrid(Grid):
    """
    A numeric 2D grid with arithmetic operations.
    """
    def __init__(self, matrix: List[List[float]]) -> None:
        super().__init__([[str(c) for c in row] for row in matrix])
        self.matrix: List[List[float]] = matrix

    def __iter__(self) -> Iterator[float]:
        for row in self.matrix:
            for cell in row:
                yield cell

    def __getitem__(self, row: int) -> List[float]:
        return self.matrix[row]

    def read(self, coords: Tuple[int, int]) -> float:
        return float(super().read(coords))

    def sum_coords(self, *coords: Tuple[int, int]) -> float:
        return sum(self.read(self._normalize_coords(c)) for c in coords)

    def sum_diagonal(self) -> float:
        size = len(self.matrix)
        return sum(self.read((i, i)) for i in range(size))

    def max_value(self) -> float:
        return max(max(row) for row in self.matrix)

    def min_value(self) -> float:
        return min(min(row) for row in self.matrix)

    def increment_neighbors(self, coords: Tuple[int, int], amount: float = 1) -> None:
        for nx, ny in self.adjacents(coords, mode='coordinates'):  # pyright: ignore[reportGeneralTypeIssues, reportAssignmentType]
            self.matrix[ny][nx] += amount # type: ignore
