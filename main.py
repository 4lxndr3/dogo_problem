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
    caminho = encontrar_caminho(salao, inicio, objetivo, janela, tamanho_celula, icone_cachorro, icone_osso, obstaculos, VERMELHO_CLARO)
    caminho_iter = iter(caminho)  # Cria um iterador sobre o caminho
    cachorro = next(caminho_iter)
    passo_atual = 0;
    
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Desenha a imagem de fundo
        janela.blit(imagem_fundo, (0, 0))

        # Desenha o salão, obstáculos, caminho encontrado, cachorro, osso e a legenda
        desenhar_salao(janela, salao, tamanho_celula, imagem_fundo)
        desenhar_obstaculos(janela, salao, tamanho_celula)
        pintar_obstaculos_adjacentes(salao, obstaculos, VERMELHO, janela, tamanho_celula)
        
        try:
            cachorro = next(caminho_iter)
            passo_atual += 1
        except StopIteration:
            mostrar_mensagem("Good Job!", BRANCO, (largura // 2, altura // 2), janela)
            mostrar_mensagem("Aperte Esc para sair", AZUL, (largura // 2, altura // 1.5), janela)
            pygame.display.flip()
            pygame.time.wait(2000)  # Aguarda um pouco para mostrar a mensagem
            rodando = False
            continue
            
        desenhar_caminho_parcial(janela, caminho, tamanho_celula, passo_atual, AZUL)
        
        janela.blit(icone_cachorro, (cachorro.x * tamanho_celula[0] + 10, cachorro.y * tamanho_celula[1] + 10))
        janela.blit(icone_osso, (objetivo.x * tamanho_celula[0] + 10, objetivo.y * tamanho_celula[1] + 10))
        desenhar_legenda(largura_salao, altura_salao, janela, tamanho_celula, BRANCO)
       
        pygame.display.flip()
        pygame.time.wait(100)
        

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
                    cachorro.mover_para(Estado(cachorro.x, cachorro.y - 1))
                elif evento.key == pygame.K_DOWN:
                    cachorro.mover_para(Estado(cachorro.x, cachorro.y + 1))
                elif evento.key == pygame.K_LEFT:
                    cachorro.mover_para(Estado(cachorro.x - 1, cachorro.y))
                elif evento.key == pygame.K_RIGHT:
                    cachorro.mover_para(Estado(cachorro.x + 1, cachorro.y))

                # Feedback visual ao mover o cachorro
                pygame.draw.circle(janela, AZUL, (cachorro.x * tamanho_celula[0] + tamanho_celula[0] // 2, cachorro.y * tamanho_celula[1] + tamanho_celula[1] // 2), 5)

                # Verifica as condições para o fim do jogo e exibe as mensagens correspondentes
                if not mensagem_game_over and not mensagem_good_job:
                    if salao.valido(cachorro.x, cachorro.y) and not salao.obstaculos[cachorro.y][cachorro.x]:
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

        # Limpa a tela e desenha a imagem de fundo, salão, obstáculos, legenda, cachorro e osso
        janela.blit(imagem_fundo, (0, 0))
        desenhar_salao(janela, salao, tamanho_celula, imagem_fundo)
        desenhar_obstaculos(janela, salao, tamanho_celula)
        pintar_obstaculos_adjacentes(salao, salao.obstaculos, VERMELHO, janela, tamanho_celula)
        desenhar_legenda(largura_salao, altura_salao, janela, tamanho_celula, BRANCO)
        janela.blit(icone_cachorro, (cachorro.x * tamanho_celula[0] + 10, cachorro.y * tamanho_celula[1] + 10))
        janela.blit(icone_osso, (objetivo.x * tamanho_celula[0] + 10, objetivo.y * tamanho_celula[1] + 10))

        # Exibe mensagens de vitória ou derrota
        if mensagem_game_over:
            mostrar_mensagem("Game Over", VERMELHO, (largura // 2, altura // 2), janela)
            mostrar_mensagem("Aperte Esc para sair", AZUL, (largura // 2, altura // 1.5), janela)
        elif mensagem_good_job:
            mostrar_mensagem("Good Job!", BRANCO, (largura // 2, altura // 2), janela)
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