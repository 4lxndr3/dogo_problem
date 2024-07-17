import pygame
from algoritmo.astar import Estado
from recursos.cores import VERMELHO_CLARO, PRETO, VERMELHO, AZUL, BRANCO
from interface.telas import escolher_modo, configurar_largura_altura
from algoritmo.salao import Salao
from interface.funcoes import *

# Inicialização do Pygame
pygame.init()

# Configuração da janela do jogo
largura, altura = 800, 600
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Nina's Adventure")

# Carregar a nova imagem de fundo
imagem_fundo = pygame.image.load('fundo.png')
# Redimensionar a imagem de fundo para o tamanho da janela
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))

# Configuração do tamanho do salão
largura_salao, altura_salao = configurar_largura_altura()
tamanho_celula = largura // largura_salao, altura // altura_salao

# Configuração dos obstáculos do salão
obstaculos = configurar_obstaculos(janela, largura_salao, altura_salao)

# Instanciação das classes principais
salao = Salao(largura_salao, altura_salao, obstaculos)
inicio = Estado(0, 0)
objetivo = Estado(largura_salao - 1, altura_salao - 1)

# Carregamento e redimensionamento das imagens do cachorro e do osso
icone_cachorro = pygame.image.load("recursos/dog_icon.png.png")
icone_osso = pygame.image.load("recursos/osso.png.png")
icone_cachorro = pygame.transform.scale(icone_cachorro, (tamanho_celula[0] - 20, tamanho_celula[1] - 20))
icone_osso = pygame.transform.scale(icone_osso, (tamanho_celula[0] - 20, tamanho_celula[1] - 20))


# Modo automático do jogo onde o cachorro faz o caminho sozinho
def modo_automatico():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Desenha o salão, obstáculos, caminho encontrado, cachorro, osso e a legenda
        desenhar_salao(janela, salao, tamanho_celula, imagem_fundo)
        desenhar_obstaculos(janela, salao, tamanho_celula)
        encontrar_caminho(salao, inicio, objetivo, janela, tamanho_celula, icone_cachorro, icone_osso, obstaculos, VERMELHO_CLARO)
        desenhar_legenda(largura_salao, altura_salao, janela, tamanho_celula, BRANCO)
        janela.blit(icone_cachorro, (inicio.x * tamanho_celula[0] + 10, inicio.y * tamanho_celula[1] + 10))
        janela.blit(icone_osso, (objetivo.x * tamanho_celula[0] + 10, objetivo.y * tamanho_celula[1] + 10))

        pygame.display.flip()

    pygame.quit()


# Modo manual do jogo onde o usuário controla o cachorro
def modo_manual():
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
                # Movimenta o cachorro nas direções correspondentes às teclas de seta
                if evento.key == pygame.K_UP:
                    proximo_estado = Estado(cachorro.x, cachorro.y - 1)
                elif evento.key == pygame.K_DOWN:
                    proximo_estado = Estado(cachorro.x, cachorro.y + 1)
                elif evento.key == pygame.K_LEFT:
                    proximo_estado = Estado(cachorro.x - 1, cachorro.y)
                elif evento.key == pygame.K_RIGHT:
                    proximo_estado = Estado(cachorro.x + 1, cachorro.y)

                # Verifica se o próximo estado é válido e não é um obstáculo
                if salao.valido(proximo_estado.x, proximo_estado.y) and not salao.obstaculos[proximo_estado.y][proximo_estado.x]:
                    cachorro.mover_para(proximo_estado)
                else:
                    mensagem_game_over = True

                # Verifica se o cachorro alcançou o objetivo
                if cachorro.x == objetivo.x and cachorro.y == objetivo.y:
                    mensagem_good_job = True

                if evento.key == pygame.K_ESCAPE:
                    rodando = False

        # Limpa a tela e desenha a imagem de fundo, salão, obstáculos, legenda, cachorro e osso
        janela.blit(imagem_fundo, (0, 0))
        desenhar_salao(janela, salao, tamanho_celula, imagem_fundo)
        desenhar_obstaculos(janela, salao, tamanho_celula)
        desenhar_legenda(largura_salao, altura_salao, janela, tamanho_celula, BRANCO)
        janela.blit(icone_cachorro, (cachorro.x * tamanho_celula[0] + 10, cachorro.y * tamanho_celula[1] + 10))
        janela.blit(icone_osso, (objetivo.x * tamanho_celula[0] + 10, objetivo.y * tamanho_celula[1] + 10))

        # Exibe mensagens de vitória
        if mensagem_good_job:
            mostrar_mensagem("Good Job!", BRANCO, (largura // 2, altura // 2), janela)
            mostrar_mensagem("Aperte Esc para sair", AZUL, (largura // 2, altura // 1.5), janela)

        # Exibe mensagem de game over se houver colisão com obstáculo
        if mensagem_game_over:
            mostrar_mensagem("Game Over", VERMELHO, (largura // 2, altura // 2), janela)
            mostrar_mensagem("Aperte Esc para sair", AZUL, (largura // 2, altura // 1.5), janela)

        pygame.display.flip()

        # Aguarda um curto período para criar um efeito de transição suave
        pygame.time.wait(100)

    pygame.quit()



if __name__ == "__main__":
    # Escolha do modo de jogo (manual ou automático)
    escolha = escolher_modo()
    if escolha == "manual":
        modo_manual()
    elif escolha == "automatico":
        modo_automatico()
