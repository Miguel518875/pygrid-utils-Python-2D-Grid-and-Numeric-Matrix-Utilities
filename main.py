from typing import Any, List, Tuple, Dict, Union, Iterator

class Map:
    class _Cell:
        def __init__(self, mapa: 'Map', coordenada: Tuple[int, int], valor: Any):
            self.y, self.x = coordenada
            self.mapa = mapa
            self.valor = valor
            self.cord = coordenada

        @property
        def valor(self) -> Any:
            return self._valor

        @valor.setter
        def valor(self, novo_valor: Any) -> None:
            self.mapa.map[self.y][self.x] = novo_valor
            self._valor = novo_valor

        def edit(self, novo_valor: Any) -> None:
            self.valor = novo_valor

        @staticmethod
        def desformatar(mapa: List[List[Any]], coordenada: Tuple[int, int]) -> Tuple[int, int]:
            coluna, linha_visual = coordenada
            x = coluna - 1
            y = len(mapa) - linha_visual
            return (y, x)

        @staticmethod
        def formatar(mapa: List[List[Any]], coordenada: Tuple[int, int]) -> Tuple[int, int]:
            y, x = coordenada
            linha_visual = len(mapa) - y
            coluna = x + 1
            return (coluna, linha_visual)

    def __init__(self, mapa: Union[List[List[Any]], 'Map', Tuple[Tuple[Any, ...], ...]]) -> None:
        if isinstance(mapa, Map):
            mapa = mapa.map
        elif not isinstance(mapa, list):
            mapa = list(mapa)
        self.map: List[List[Any]] = mapa
        coords: Dict[Tuple[int, int], Map._Cell] = {}
        for i, line in enumerate(mapa):
            for j, cell in enumerate(line):
                coords[(i, j)] = Map._Cell(self, (i, j), cell)
        self.cords = coords

    def __iter__(self) -> Iterator[Any]:
        for line in self.map:
            for cell in line:
                yield cell

    def __getitem__(self, line: int) -> List[Any]:
        return self.map[line]

    def __str__(self) -> str:
        resultado = []
        for line in self.map:
            for cell in line:
                resultado.append('"{}"'.format(cell))
            resultado.append('\n')
        return ', '.join(resultado).replace(', \n, ', ',\n')[:-3]

    def __repr__(self) -> str:
        return str(self)

    def __call__(self, valor: Any) -> Any:
        coordenadas = []
        for i, line in enumerate(self.map):
            for j, cell in enumerate(line):
                if cell == valor:
                    coordenadas.append(Map._Cell.formatar(self.map, (i, j)))
        if len(coordenadas) == 1:
            return coordenadas[0]
        return tuple(coordenadas)

    def __eq__(self, other: Any) -> bool:
        other = Map(other)
        return self.freeze() == other.freeze()

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __gt__(self, other: Any) -> bool:
        other = Map(other)
        return self.freeze() > other.freeze()

    def __ge__(self, other: Any) -> bool:
        return self.__eq__(other) or self.__gt__(other)

    def __lt__(self, other: Any) -> bool:
        return not self.__gt__(other) and not self.__eq__(other)

    def __le__(self, other: Any) -> bool:
        return not self.__gt__(other)

    def show(self) -> None:
        for line in self.map:
            print(line)

    def to_dict(self) -> Dict[Tuple[int, int], Any]:
        dicionario = {}
        for i, line in enumerate(self.map):
            for j, cell in enumerate(line):
                dicionario[(j, i)] = cell
        return dicionario

    def read(self, coordenadas: Tuple[int, int]) -> Any:
        y, x = Map._Cell.desformatar(self.map, coordenadas)
        return self.map[y][x]

    def edit(self, coordenadas: Tuple[int, int], novo_valor: Any,
             mode: str = 'editar') -> Any:
        if mode == 'editar':
            self.cords[Map._Cell.desformatar(self.map, coordenadas)].edit(novo_valor)
        else:
            copy_cords = self.cords.copy()
            self.cords[Map._Cell.desformatar(self.map, coordenadas)].edit(novo_valor)
            copy2 = self.cords.copy()
            self.cords = copy_cords.copy()
            return copy2

    def arredores(self, coordenadas: Tuple[int, int],
                  vizinho: int = 0,
                  mode: str = 'valor') -> Any:
        deslocamentos = {
            1: (-1, -1), 2: (-1, 0), 3: (-1, 1),
            4: (0, -1),             6: (0, 1),
            7: (1, -1), 8: (1, 0), 9: (1, 1)
        }
        coordenadas = Map._Cell.desformatar(self.map, coordenadas)
        if vizinho:
            deslocamento = deslocamentos[vizinho]
            try:
                self.map[coordenadas[0]][coordenadas[1]]
            except IndexError:
                raise IndexError('Coordinate out of map bounds')
            coordenada = [coordenadas[0] + deslocamento[0],
                          coordenadas[1] + deslocamento[1]]
            if mode == 'valor':
                return self.map[coordenada[0]][coordenada[1]]
            return tuple(Map._Cell.formatar(self.map, coordenada))
        valores = []
        for i in range(1, 10):
            if i == 5:
                continue
            try:
                valores.append(self.arredores(Map._Cell.formatar(self.map, coordenadas), i, mode))
            except IndexError:
                continue
        return tuple(valores)

    def freeze(self) -> Tuple[Tuple[Any, ...], ...]:
        return tuple(tuple(cell for cell in line) for line in self.map)


# Example
a = Map([['o' for _ in range(10)] for _ in range(10)])
print(str(a))
