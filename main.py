import pygame
from astar import Estado
from cores import VERMELHO_CLARO
from telas import *
from salao import Salao
from funcoes import *

largura, altura = 800, 600
pygame.init()

# Configura as dimensões do salao
largura_salao, altura_salao = configurar_largura_altura()
tamanho_celula = largura // largura_salao, altura // altura_salao
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Ninas's Adventure")

# Configuração dos obstáculos do salão
obstaculos = configurar_obstaculos(janela,largura_salao,altura_salao)

# Instancia as clases
salao = Salao(largura_salao, altura_salao, obstaculos)
inicio = Estado(0, 0)
objetivo = Estado(largura_salao - 1, altura_salao - 1)


# Carrega e redimensiona as imagens do cachorro e do osso para o tamanho das células do salão.
icone_cachorro = pygame.image.load("dog_icon.png.png")
icone_osso = pygame.image.load("osso.png.png")
icone_cachorro = pygame.transform.scale(icone_cachorro, (tamanho_celula[0] - 10, tamanho_celula[1] - 10))
icone_osso = pygame.transform.scale(icone_osso, (tamanho_celula[0] - 10, tamanho_celula[1] - 10))


# Função para o modo automático do jogo onde o dogo faz o caminho sozinho.
def modo_automatico():
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Desenha o salão, obstáculos, caminho encontrado, cachorro, osso e a legenda.
        desenhar_salao(janela, salao, tamanho_celula)
        desenhar_obstaculos(janela, salao, tamanho_celula)
        encontrar_caminho(salao, inicio, objetivo, janela, tamanho_celula, icone_cachorro, icone_osso, obstaculos,
                          VERMELHO_CLARO)
        desenhar_legenda(salao.largura, salao.altura, janela, tamanho_celula,BRANCO)
        pygame.display.flip()
    pygame.quit()


# Função para o modo manual do jogo onde o usuário gera as posicoes.
def modo_manual():
    pygame.init()
    cachorro = Estado(0, 0)
    objetivo = Estado(largura_salao - 1, altura_salao - 1)
    mensagem_game_over = False
    mensagem_good_job = False
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                # Movimenta o cachorro nas direções correspondentes às teclas de seta.
                if evento.key == pygame.K_UP:
                    cachorro.mover_para(Estado(cachorro.x, cachorro.y - 1))
                elif evento.key == pygame.K_DOWN:
                    cachorro.mover_para(Estado(cachorro.x, cachorro.y + 1))
                elif evento.key == pygame.K_LEFT:
                    cachorro.mover_para(Estado(cachorro.x - 1, cachorro.y))
                elif evento.key == pygame.K_RIGHT:
                    cachorro.mover_para(Estado(cachorro.x + 1, cachorro.y))

                # Verifica as condições para o fim do jogo e exibe as mensagens correspondentes.
                if not mensagem_game_over and not mensagem_good_job:
                    if salao.is_valid(cachorro.x, cachorro.y) and not salao.obstaculos[cachorro.y][cachorro.x]:
                        if not calcular_distancia_obstaculo(cachorro.x, cachorro.y, salao.obstaculos):
                            cachorro.mover_para(cachorro)
                        else:
                            mensagem_game_over = True
                    else:
                        mensagem_game_over = True

                if not mensagem_game_over and not mensagem_good_job and cachorro.x == objetivo.x and cachorro.y == objetivo.y:
                    mensagem_good_job = True

                if evento.key == pygame.K_ESCAPE:
                    rodando = False

        janela.fill(PRETO)
        desenhar_salao(janela, salao, tamanho_celula)
        desenhar_obstaculos(janela, salao, tamanho_celula)
        pintar_obstaculos_adjacentes(salao, salao.obstaculos, VERMELHO_CLARO, janela, tamanho_celula)

        desenhar_legenda(salao.largura, salao.altura, janela, tamanho_celula,BRANCO)
        # Desenha o cachorro e o osso
        janela.blit(icone_cachorro, (cachorro.x * tamanho_celula[0] + 5, cachorro.y * tamanho_celula[1] + 5))
        janela.blit(icone_osso, (objetivo.x * tamanho_celula[0] + 5, objetivo.y * tamanho_celula[1] + 5))

        # Gera as mensagens caso o usuário ganhe ou perca
        if mensagem_game_over:
            mostrar_mensagem("Game Over", VERMELHO, (largura // 2, altura // 2), janela)
            mostrar_mensagem("Aperte Esc para sair", AZUL, (largura // 2, altura // 1.5), janela)
        elif mensagem_good_job:
            mostrar_mensagem("Good Job!", BRANCO, (largura // 2, altura // 2), janela)
            mostrar_mensagem("Aperte Esc para sair", AZUL, (largura // 2, altura // 1.5), janela)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    escolha = escolher_modo()
    if escolha == "manual":
        modo_manual()
    elif escolha == "automatico":
        modo_automatico()
