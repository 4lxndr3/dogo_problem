import random
from algoritmo.astar import a_star
from recursos.cores import PRETO, VERMELHO, AZUL, BRANCO, minha_fonte
from interface.telas import escolher_modo_obstaculo, escolher_posicao_obstaculo, imprimir_sem_saida
import pygame

def configurar_obstaculos(janela, largura_salao, altura_salao):
    quantidade_obstaculos = calcular_quantidade_obstaculos(largura_salao, altura_salao)
    
    modo_obstaculo = escolher_modo_obstaculo()
    if modo_obstaculo == 'automatico':
        obs = definir_obstaculos_aleatorios(largura_salao, altura_salao, quantidade_obstaculos)
    else:
        obs = escolher_posicao_obstaculo(janela, largura_salao, altura_salao)

    return obs

def calcular_quantidade_obstaculos(largura, altura):
    area = largura * altura
    # Definindo a proporção de obstáculos em relação à área do salão
    proporcao = 0.05  # 10% da área
    quantidade_obstaculos = max(1, int(area * proporcao))
    return quantidade_obstaculos



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
def encontrar_caminho(salao, inicio, objetivo, janela, tamanho_celula, icone_cachorro, icone_osso, obstaculos, VERMELHO_CLARO):
    caminho = a_star(salao, inicio, objetivo)
    if not caminho:
        imprimir_sem_saida(janela)
    else:
        desenhar_caminho(janela, caminho, tamanho_celula)
    pintar_obstaculos_adjacentes(salao, obstaculos, VERMELHO_CLARO, janela, tamanho_celula)
    janela.blit(icone_cachorro, (inicio.x * tamanho_celula[0] + 5, inicio.y * tamanho_celula[1] + 5))
    janela.blit(icone_osso, (objetivo.x * tamanho_celula[0] + 5, objetivo.y * tamanho_celula[1] + 5))
    return caminho

def desenhar_caminho_parcial(janela, caminho, tamanho_celula, passo_atual, VERMELHO_CLARO):
    for estado in caminho[:passo_atual]:
        pygame.draw.rect(janela,  VERMELHO_CLARO, (estado.x * tamanho_celula[0], estado.y * tamanho_celula[1], tamanho_celula[0], tamanho_celula[1]))

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
def mostrar_mensagem(texto, cor, posicao, janela):
    fonte = pygame.font.SysFont(None, 48)
    mensagem = fonte.render(texto, True, cor)
    rect = mensagem.get_rect(center=posicao)
    janela.blit(mensagem, rect)



# Função para pintar as zonas adjacentes a um obstaculo em uma cor diferente dele.
def pintar_obstaculos_adjacentes(salao, obstaculos, cor, janela, tamanho_celula):
    for y in range(salao.altura):
        for x in range(salao.largura):
            if obstaculos[y][x]:
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),
                               (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < salao.largura and 0 <= new_y < salao.altura and not obstaculos[new_y][new_x]:
                        pygame.draw.rect(janela, cor,
                                         (new_x * tamanho_celula[0], new_y * tamanho_celula[1], tamanho_celula[0],
                                          tamanho_celula[1]), 0)

# Função para desenhar as células do grid.
def desenhar_salao(janela, salao, tamanho_celula, imagem_fundo):
    janela.blit(imagem_fundo, (0, 0))
    # Desenha as bordas do salão
    for y in range(salao.altura):
        for x in range(salao.largura):
            pygame.draw.rect(janela, PRETO, (x * tamanho_celula[0], y * tamanho_celula[1], tamanho_celula[0], tamanho_celula[1]), 1)




# Função para desenhar obstáculos no grid.
def desenhar_obstaculos(janela, salao, tamanho_celula):
    for y in range(salao.largura):
        for x in range(salao.altura):
            if salao.obstaculos[y][x]:
                pygame.draw.rect(janela, PRETO,
                                 (x * tamanho_celula[0] + 2,  y * tamanho_celula[1] + 2,
                                  tamanho_celula[0] - 4, tamanho_celula[1] - 4), border_radius=5)

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
