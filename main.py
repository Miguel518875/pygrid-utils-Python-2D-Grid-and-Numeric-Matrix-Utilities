from __future__ import annotations
from typing import Any, Iterator, Literal

class Map():
    class _Cell():
        def __init__(self, map_obj: Map, coordinate: tuple[int, int], value: object):
            self.y, self.x = coordinate
            self.map_obj = map_obj
            self.value = value
            self.coord = coordinate
        
        @property
        def value(self) -> object:
            return self._value
        
        @value.setter
        def value(self, new_value: object) -> None:
            self.map_obj.map[self.y][self.x] = new_value  # pyright: ignore[reportAttributeAccessIssue]
            self._value = new_value
        
        def edit(self, new_value: object) -> None:
            self.value = new_value
            
        @staticmethod
        def unformat(map_data: list[list[Any]], coordinate: tuple[int, int]) -> tuple[int, int]:
            col, visual_row = coordinate
            x = col - 1
            y = len(map_data) - visual_row
            return (y, x)

        @staticmethod
        def format(map_data: list[list[Any]], coordinate: tuple[int, int]) -> tuple[int, int]:
            y, x = coordinate
            visual_row = len(map_data) - y
            col = x + 1
            return (col, visual_row)

    
    def __init__(self, map_data: list[list[Any]] | Map | tuple[tuple[Any, ...], ...]) -> None:
        if not isinstance(map_data, list):
            map_data = list(map_data)
        self.map = map_data
        coords = dict()
        for i, line in enumerate(map_data):
            for j, cell in enumerate(line):
                coords[(i, j)] = Map._Cell(self, (i, j), cell)
        self.cells = coords
        self.cells: dict[tuple[int, int], Map._Cell]
        
    def __iter__(self) -> Iterator[Any]:
        for line in self.map:
            for cell in line:
                yield cell
                
    def __getitem__(self, line: int) -> list[Any]:
        return self.map[line]
    
    def __str__(self) -> str:
        result = []
        for line in self.map:
            for cell in line:
                result.append(f'"{cell}"')
            result.append('\n')
        return ', '.join(result).replace(', \n, ', ',\n')[:-3]
    
    def __repr__(self) -> str:
        return str(self)
    
    def __call__(self, value) -> object:
        coordinates = []
        for i, line in enumerate(self.map):
            for j, cell in enumerate(line):
                if cell == value:
                    coordinates.append(Map._Cell.format(self.map, (i, j)))
        if len(coordinates) == 1:
            return coordinates[0]
        return tuple(coordinates)
        
    def __eq__(self, other) -> bool:
        other = Map(other)
        return self.freeze() == other.freeze()
    
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    
    def __gt__(self, other) -> bool:
        other = Map(other)
        return self.freeze() > other.freeze()
    
    def __ge__(self, other) -> bool:
        return self.__eq__(other) or self.__gt__(other)
    
    def __lt__(self, other) -> bool:
        return not self.__gt__(other) and not self.__eq__(other)
    
    def __le__(self, other) -> bool:
        return not self.__gt__(other)
    
    def show(self) -> None:
        for line in self.map:
            print(line)
            
    def to_dict(self) -> dict[tuple[int, int], object]:
        dictionary = dict()
        for i, line in enumerate(self.map):
            for j, cell in enumerate(line):
                dictionary[(j, i)] = cell
        return dictionary
                
    def read(self, coordinate: tuple[int, int]) -> object:
        y, x = Map._Cell.unformat(self.map, coordinate)
        return self.map[y][x]
    
    def edit(self, coordinate: tuple[int, int], new_value: object, mode: Literal['edit', 'return edited']='edit') -> object:
        if mode == 'edit':
            self.cells[(Map._Cell.unformat(self.map, coordinate))].edit(new_value)
        else:
            copy = self.cells.copy()
            self.cells[(Map._Cell.unformat(self.map, coordinate))].edit(new_value)
            copy2 = self.cells.copy()
            self.cells = copy.copy()
            return copy2
        
    def neighbors(self, coordinate: tuple[int, int], neighbor: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]=0, mode: Literal['value', 'coordinate']='value') -> object:
        offsets = {
            1: (-1, -1), 2: (-1, 0), 3: (-1, 1),
            4: (0, -1),             6: (0, 1),
            7: (1, -1), 8: (1, 0), 9: (1, 1)
        }
        coordinate = Map._Cell.unformat(self.map, coordinate)
        if neighbor:
            offset = offsets[neighbor]
            try:
                self.map[coordinate[0]][coordinate[1]]
            except IndexError:
                raise IndexError('Coordinate out of map')
            if mode == 'value':
                coord = []
                coord.append(coordinate[0] + offset[0])
                coord.append(coordinate[1] + offset[1])
                return self.map[coord[0]][coord[1]]
            else:
                coord = []
                coord.append(coordinate[0] + offset[0])
                coord.append(coordinate[1] + offset[1])
                return tuple(Map._Cell.format(self.map, coord))
        else:
            results = []
            for i in range(1, 10):
                if i == 5: continue
                try:
                    results.append(self.neighbors(Map._Cell.format(self.map, coordinate), i, mode))
                except IndexError:
                    continue
            return tuple(results)

    def freeze(self) -> tuple[tuple[object, ...], ...]:
        return tuple(tuple(cell for cell in line) for line in self.map)

# Example usage
a = Map([['o' for _ in range(10)] for _ in range(10)])
print(str(a))
