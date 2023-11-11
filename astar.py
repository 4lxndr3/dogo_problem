import heapq


class Estado:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.custo = 0

    def __lt__(self, other):
        # Corrigido para ordenar com base no custo
        return self.custo < other.custo

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Método para mover o dogo no modo manual
    # calculo é feito para mover apenas uma celula do salao na direção desejada
    def mover_para(self, destino):
        dx = destino.x - self.x
        dy = destino.y - self.y
        if dx != 0:
            self.x += dx // abs(dx)
        if dy != 0:
            self.y += dy // abs(dy)


# Função para reconstruir o caminho a partir do estado objetivo
def reconstruir_caminho(caminho, objetivo):
    estado = objetivo
    caminho_final = [estado]
    while estado in caminho and caminho[estado] is not None:
        estado = caminho[estado]
        caminho_final.append(estado)

    return list(reversed(caminho_final))


# Algoritmo A* para encontrar o caminho no salão
def a_star(salao, inicio, objetivo):
    # Inicializa a heap (fila de prioridade) com o estado inicial
    agenda = []
    heapq.heappush(agenda, (0, inicio))

    # Conjunto para rastrear estados já visitados
    estados_passados = set()
    custo_acumulado = {inicio: 0}
    caminho = {}

    while agenda:
        # Extrai o estado com a menor prioridade (menor custo acumulado) da heap
        _, estado = heapq.heappop(agenda)

        # Verifica se o estado atual é o objetivo após a expansão dos vizinhos
        if estado.x == objetivo.x and estado.y == objetivo.y:
            seguir_caminho = reconstruir_caminho(caminho, estado)
            # Esvazia a heap após atingir o objetivo
            heapq.heappop(agenda)
            return seguir_caminho

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = estado.x + dx, estado.y + dy
            proximo_estado = Estado(x, y)

            # Verifica se o próximo estado é válido e ainda não foi visitado
            if salao.valido(x, y) and proximo_estado not in estados_passados:
                # Calcula o novo custo acumulado
                novo_custo = custo_acumulado[estado] + salao.custo_total(estado, proximo_estado)

                # Verifica se o novo custo é menor do que o custo acumulado atual
                if proximo_estado not in custo_acumulado or novo_custo < custo_acumulado[proximo_estado]:
                    # Atualiza o custo acumulado e a prioridade na heap
                    custo_acumulado[proximo_estado] = novo_custo
                    prioridade = novo_custo + salao.heuristica(proximo_estado, objetivo)
                    heapq.heappush(agenda, (prioridade, proximo_estado))

                    # Adiciona o próximo estado aos estados visitados e atualiza o caminho
                    estados_passados.add(proximo_estado)
                    caminho[proximo_estado] = estado

    return None
