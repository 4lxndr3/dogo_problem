class Estado:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.custo = 0

    def __lt__(self, other):
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

    # Inverte a lista para obter o caminho do estado inicial ao objetivo
    return list(reversed(caminho_final))


# Definição da classe FilaPrioridade para gerenciar uma fila de prioridade simples
class FilaPrioridade:
    def __init__(self):
        self.elementos = []

    # Verifica se a fila de prioridade está vazia
    def vazia(self):
        return not self.elementos

    # Adiciona um item à fila de prioridade com uma determinada prioridade
    def adicionar(self, prioridade, item):
        self.elementos.append((prioridade, item))

    # Obtém o item com a maior prioridade da fila de prioridade
    def obter(self):
        # Ordena os elementos com base na prioridade e retorna o primeiro elemento (o de maior prioridade)
        self.elementos.sort(key=lambda x: x[0])
        return self.elementos.pop(0) if self.elementos else None

    # Esvazia a lista de elementos
    def delete(self):
        self.elementos = []


# Funçã que é pra encontrar o caminho no salão
def a_star(salao, inicio, objetivo):
    # Inicializa a fila de prioridade com o estado inicial
    agenda = FilaPrioridade()
    agenda.adicionar(0, inicio)

    estados_passados = set()
    custo_acumulado = {inicio: 0}
    caminho = {}

    while not agenda.vazia():
        # Obtém o próximo estado da fila de prioridade
        proximo_item = agenda.obter()

        # Verifica se a fila está vazia
        if not proximo_item:
            break

        _, estado = proximo_item

        # Verifica se o estado atual é o objetivo após a expansão dos vizinhos
        if estado.x == objetivo.x and estado.y == objetivo.y:
            seguir_caminho = reconstruir_caminho(caminho, estado)
            # Esvazia a fila após encontrar o caminho
            agenda.delete()
            return seguir_caminho

        # Explora os vizinhos do estado atual
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = estado.x + dx, estado.y + dy
            proximo_estado = Estado(x, y)

            # Verifica se o próximo estado é válido e ainda não foi visitado
            if salao.valido(x, y) and proximo_estado not in estados_passados:
                # Calcula o novo custo acumulado
                novo_custo = custo_acumulado[estado] + salao.custo_total(estado, proximo_estado)

                # Verifica se o novo custo é menor do que o custo acumulado atual
                if proximo_estado not in custo_acumulado or novo_custo < custo_acumulado[proximo_estado]:
                    # Atualiza o custo acumulado e a prioridade na fila de prioridade
                    custo_acumulado[proximo_estado] = novo_custo
                    prioridade = novo_custo + salao.heuristica(proximo_estado, objetivo)
                    agenda.adicionar(prioridade, proximo_estado)

                    # Adiciona o próximo estado aos estados visitados e atualiza o caminho
                    estados_passados.add(proximo_estado)
                    caminho[proximo_estado] = estado
    # Esvazia a fila antes de retornar None se não foi possível encontrar um caminho
    agenda.delete()
    return None
