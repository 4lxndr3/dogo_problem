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
    # calculo é feito para mover apenas uma célula do salão na direção desejada
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
        self._heapify_acima(len(self.elementos) - 1)

    def _heapify_acima(self, indice):
        while indice > 0:
            indice_pai = (indice - 1) // 2
            if self.elementos[indice][0] < self.elementos[indice_pai][0]:
                self.elementos[indice], self.elementos[indice_pai] = self.elementos[indice_pai], self.elementos[indice]
                indice = indice_pai
            else:
                break

    def _heapify_abaixo(self, indice):
        tamanho = len(self.elementos)
        while True:
            indice_esquerda = 2 * indice + 1
            indice_direita = 2 * indice + 2
            menor = indice
            if indice_esquerda < tamanho and self.elementos[indice_esquerda][0] < self.elementos[menor][0]:
                menor = indice_esquerda
            if indice_direita < tamanho and self.elementos[indice_direita][0] < self.elementos[menor][0]:
                menor = indice_direita
            if menor != indice:
                self.elementos[indice], self.elementos[menor] = self.elementos[menor], self.elementos[indice]
                indice = menor
            else:
                break

    # Obtém o item com a maior prioridade da fila de prioridade
    def obter(self):
        # Implementação do selection sort
        n = len(self.elementos)
        for i in range(n):
            menor_indice = i
            for j in range(i + 1, n):
                if self.elementos[j][0] < self.elementos[menor_indice][0]:
                    menor_indice = j

            # Swap os elementos
            self.elementos[i], self.elementos[menor_indice] = self.elementos[menor_indice], self.elementos[i]

        return self.elementos.pop(0) if self.elementos else None

    def aumentar_chave(self, indice, novo_valor):
        if 0 <= indice < len(self.elementos):
            self.elementos[indice] = novo_valor
            self._heapify_acima(indice)

    def remover_chave(self, indice):
        if 0 <= indice < len(self.elementos):
            self.aumentar_chave(indice, (float('inf'), self.elementos[indice][1]))
            self.obter()


# Função que é pra encontrar o caminho no salão
def a_star(salao, inicio, objetivo):
    agenda = FilaPrioridade()
    agenda.adicionar(0, inicio)

    estados_passados = set()
    custo_acumulado = {inicio: 0}
    caminho = {}
    
    while not agenda.vazia():
        proximo_item = agenda.obter()
        if not proximo_item:
            break

        _, estado = proximo_item

        if estado.x == objetivo.x and estado.y == objetivo.y:
            return reconstruir_caminho(caminho, estado)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = estado.x + dx, estado.y + dy
            proximo_estado = Estado(x, y)

            if salao.valido(x, y) and proximo_estado not in estados_passados:
                novo_custo = custo_acumulado[estado] + salao.custo_total(estado, proximo_estado)
                if proximo_estado not in custo_acumulado or novo_custo < custo_acumulado[proximo_estado]:
                    custo_acumulado[proximo_estado] = novo_custo
                    prioridade = novo_custo + salao.heuristica(proximo_estado, objetivo)
                    agenda.adicionar(prioridade, proximo_estado)
                    estados_passados.add(proximo_estado)
                    caminho[proximo_estado] = estado

    return None  # Retorna None se não houver caminho