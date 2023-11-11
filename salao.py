
class Salao:
    def __init__(self, largura, altura, obstaculos):
        self.largura = largura
        self.altura = altura
        self.obstaculos = obstaculos

    def valido(self, x, y):
        return 0 <= x < self.largura and 0 <= y < self.altura and not self.obstaculos[y][x]

    def custo_total(self, estado, objetivo):
        custo_base = abs(objetivo.x - estado.x) + abs(objetivo.y - estado.y)
        custo_adjacente_obstaculo = 20

        adjacentes_obstaculo = [
            (estado.x + 1, estado.y),
            (estado.x - 1, estado.y),
            (estado.x, estado.y + 1),
            (estado.x, estado.y - 1),
            (estado.x - 1, estado.y - 1),
            (estado.x - 1, estado.y + 1),
            (estado.x + 1, estado.y - 1),
            (estado.x + 1, estado.y + 1)
        ]

        for x, y in adjacentes_obstaculo:
            if 0 <= x < self.largura and 0 <= y < self.altura and self.obstaculos[y][x]:
                custo_base += custo_adjacente_obstaculo

        return custo_base

    def heuristica(self, estado, objetivo):
        dx = abs(estado.x - objetivo.x)
        dy = abs(estado.y - objetivo.y)
        return dx + dy + 0.9 * min(dx, dy)

