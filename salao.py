class Salao:
    def __init__(self, largura, altura, obstaculos):
        self.largura = largura
        self.altura = altura
        self.obstaculos = obstaculos

    # Método para verificar se uma posição (x, y) é válida (dentro dos limites do salão e não é um obstáculo).
    def is_valid(self, x, y):
        return 0 <= x < self.largura and 0 <= y < self.altura and not self.obstaculos[y][x]

    # Método para calcular o custo total de um estado em relação ao objetivo.
    def custo_total(self, estado, objetivo):
        custo_base = abs(objetivo.x - estado.x) + abs(objetivo.y - estado.y)
        custo_adjacente_obstaculo = 10  # Custo adicional para estados adjacentes aos obstáculos

        # Lista de coordenadas dos estados adjacentes ao estado do obstaculo
        adjacentes_obstaculo = [(estado.x + 1, estado.y),
                                (estado.x - 1, estado.y),
                                (estado.x, estado.y + 1),
                                (estado.x, estado.y - 1),
                                (estado.x - 1, estado.y - 1),
                                (estado.x - 1, estado.y + 1),
                                (estado.x + 1, estado.y - 1),
                                (estado.x + 1, estado.y + 1)]

        # Verifica se os estados adjacentes estão dentro dos limites do salão e são obstáculos
        for x, y in adjacentes_obstaculo:
            if 0 <= x < self.largura and 0 <= y < self.altura and self.obstaculos[y][x]:
                custo_base += custo_adjacente_obstaculo  # Adiciona o custo adicional para adjacente a um obstáculo

        return custo_base

