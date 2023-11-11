import random
import pygame
from astar import a_star
from cores import PRETO, VERMELHO, AZUL, BRANCO, minha_fonte
from telas import escolher_modo_obstaculo, escolher_posicao_obstaculo, imprimir_sem_saida


def configurar_obstaculos(janela, largura_salao, altura_salao):
    quantidade_obstaculos = 3
    modo_obstaculo = escolher_modo_obstaculo()
    if modo_obstaculo == 'automatico':
        obs = definir_obstaculos_aleatorios(largura_salao, altura_salao, quantidade_obstaculos)
    else:
        obs = escolher_posicao_obstaculo(janela, largura_salao, altura_salao)

    return obs


# Função para definir obstáculos aleatórios no grid do salão.
# Retorna as posicoes dos obstáculos.
def definir_obstaculos_aleatorios(largura, altura, quantidade_obstaculos):
    x_fim, y_fim = largura - 1, altura - 1
    obstaculos = [[False for _ in range(largura)] for _ in range(altura)]
    for _ in range(quantidade_obstaculos):
        x = random.randint(0, largura - 1)
        y = random.randint(0, altura - 1)
        if (x, y) in [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2), (1, 1),
                      (x_fim, y_fim), (x_fim - 1, y_fim), (x_fim - 2, y_fim),
                      (x_fim, y_fim - 1), (x_fim, y_fim - 2), (x_fim - 1, y_fim - 1)]:
            y = (y + 3) % altura
        obstaculos[y][x] = True

    return obstaculos


# Função para encontrar e desenhar o caminho do início ao fim usando o algoritmo A*.
def encontrar_caminho(salao, inicio, objetivo, janela, tamanho_celula, icone_cachorro, icone_osso, obstaculos,
                      VERMELHO_CLARO):
    caminho = a_star(salao, inicio, objetivo)
    if not caminho:
        imprimir_sem_saida(janela)
    if caminho:
        desenhar_caminho(janela, caminho, tamanho_celula)
    pintar_obstaculos_adjacentes(salao, obstaculos, VERMELHO_CLARO, janela, tamanho_celula)
    janela.blit(icone_cachorro, (inicio.x * tamanho_celula[0] + 5, inicio.y * tamanho_celula[1] + 5))
    janela.blit(icone_osso, (objetivo.x * tamanho_celula[0] + 5, objetivo.y * tamanho_celula[1] + 5))


# Função para calcular se há um obstáculo adjacente à posição dada.
# Retorna True se houver um obstáculo adjacente à posição do cachorro, senão False.
def calcular_distancia_obstaculo(cachorro_x, cachorro_y, obstaculos):
    for y in range(len(obstaculos)):
        for x in range(len(obstaculos[0])):
            if obstaculos[y][x]:
                distancia_x = abs(cachorro_x - x)
                distancia_y = abs(cachorro_y - y)
                if distancia_x <= 1 and distancia_y <= 1:
                    return True
    return False


# Função para mostrar uma mensagem na tela.
def mostrar_mensagem(mensagem, cor, posicao, janela):
    fonte = pygame.font.Font(None, 36)  # Define a fonte e o tamanho do texto
    texto = fonte.render(mensagem, True, cor)  # Renderiza o texto com a cor especificada
    retangulo = texto.get_rect(center=posicao)  # Obtém o retângulo que contém o texto
    janela.blit(texto, retangulo.topleft)  # Desenha o texto na tela


# Função para pintar as zonas adjacentes a um obstaculo em uma cor diferente dele.
def pintar_obstaculos_adjacentes(salao, obstaculos, cor, janela, tamanho_celula):
    for y in range(salao.altura):
        for x in range(salao.largura):
            if obstaculos[y][x]:
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),
                               (-1, -1), (0, -1), (-1, +1), (+1, -1), (+1, +1)]:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < salao.largura and 0 <= new_y < salao.altura and not obstaculos[new_y][new_x]:
                        pygame.draw.rect(janela, cor,
                                         (new_x * tamanho_celula[0], new_y * tamanho_celula[1], tamanho_celula[0],
                                          tamanho_celula[1]), 0)


# Função para desenhar as células do grid.
def desenhar_salao(janela, salao, tamanho_celula):
    for y in range(salao.largura):
        for x in range(salao.altura):
            cor = PRETO if salao.valido(x, y) else VERMELHO
            pygame.draw.rect(janela, cor,
                             (x * tamanho_celula[0], y * tamanho_celula[1], tamanho_celula[0], tamanho_celula[1]), 0)


# Função para desenhar obstáculos no grid.
def desenhar_obstaculos(janela, salao, tamanho_celula):
    for y in range(salao.largura):
        for x in range(salao.altura):
            if salao.obstaculos[y][x]:
                pygame.draw.rect(janela, VERMELHO,
                                 (x * tamanho_celula[0], y * tamanho_celula[1], tamanho_celula[0], tamanho_celula[1]),
                                 0)


# Função para desenhar a legenda no grid.
def desenhar_legenda(largura_salao, altura_salao, janela, tamanho_celula, cor):
    for y in range(largura_salao):
        for x in range(altura_salao):
            if x == 0 or y == 0:
                if y >= x:
                    texto = f"{y}"
                if x >= y:
                    texto = f"{x}"
                desenhar_texto(janela, texto, (x * tamanho_celula[0] + 10, y * tamanho_celula[1] + 10), cor)


# Função para desenhar o caminho que o dogo faz no grid.
def desenhar_caminho(janela, caminho, tamanho_celula):
    for estado in caminho:
        pygame.draw.rect(janela, AZUL,
                         (estado.x * tamanho_celula[0], estado.y * tamanho_celula[1], tamanho_celula[0],
                          tamanho_celula[1]), 0)


# Função para escrever os textos da legenda.
def desenhar_texto(janela, texto, posicao, cor=BRANCO, tamanho=20):
    fonte = pygame.font.Font(minha_fonte, tamanho)
    superficie_texto = fonte.render(texto, True, cor)
    janela.blit(superficie_texto, posicao)