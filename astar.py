import heapq


# Classe que representa um estado no grid (coordenadas x, y).
class Estado:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Comparar estados durante a ordenação na fila de prioridade.
    def __lt__(self, other):
        return False

    # Mover o estado para um destino.
    def mover_para(self, destino):
        dx = destino.x - self.x
        dy = destino.y - self.y
        if dx != 0:
            self.x += dx // abs(dx)
        if dy != 0:
            self.y += dy // abs(dy)


# Função de busca A* para encontrar o caminho mais curto de um ponto de início para um ponto de objetivo no grid.
# Retorna uma lista de estados representando o caminho do início ao objetivo, ou None se nenhum caminho é encontrado.
def a_star(salao, inicio, objetivo):
    agenda = []  # Fila de prioridade para estados a serem explorados
    heapq.heappush(agenda, (0, inicio))
    estados_passados = set()
    caminho = {}

    while agenda:
        _, estado = heapq.heappop(agenda)  # Obtém o estado com o menor custo da fila

        if estado.x == objetivo.x and estado.y == objetivo.y:
            seguir_caminho = []
            while estado:
                seguir_caminho.append(estado)
                estado = caminho.get(estado)
            return list(reversed(seguir_caminho))  # Inverte a lista para obter o caminho correto

        # Gera estados adjacentes ao estado atual
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = estado.x + dx, estado.y + dy
            proximo_estado = Estado(x, y)

            # Verifica se o próximo estado é válido e ainda não foi explorado
            if salao.is_valid(x, y) and proximo_estado not in estados_passados:
                custo = salao.custo_total(proximo_estado, objetivo)
                heapq.heappush(agenda,
                               (custo, proximo_estado))
                estados_passados.add(proximo_estado)
                caminho[proximo_estado] = estado

    return None  # Retorna None se nenhum caminho for encontrado
