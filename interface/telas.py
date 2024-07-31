import pygame
from recursos.cores import PRETO, BRANCO, VERMELHO, AZUL, CINZA_ESCURO, minha_fonte
import sys

# Largura e altura da janela do pygame
largura_janela, altura_janela = 800, 600

# Cores
VERDE = (34,139,34)
VERMELHO = (178,34,34)


def imprimir_sem_saida(janela):
    # Crie uma fonte para exibir o texto
    fonte = pygame.font.Font(minha_fonte, 36)

    # Crie o texto
    texto = fonte.render("O dogo está sem saída", True, BRANCO)

    # Obtenha as coordenadas para centralizar o texto na janela
    x_texto = (largura_janela - texto.get_width()) // 2
    y_texto = (altura_janela - texto.get_height()) // 2

    # Loop principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        janela.fill(PRETO)

        # Desenhe o texto no centro da janela
        janela.blit(texto, (x_texto, y_texto))

        # Atualize a tela
        pygame.display.flip()

# Função para permitir ao usuário escolher entre os modos de jogo: manual ou automático
def escolher_modo():
    pygame.init()

    janela_obs = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption("Escolher Modo")
    fonte = pygame.font.Font(minha_fonte, 24)
    texto_opcao = fonte.render("Clique na opção:", True, CINZA_ESCURO)
    texto_manual = fonte.render("Modo Manual", True, BRANCO)
    texto_automatico = fonte.render("Modo Automático", True, BRANCO)

    largura_texto_manual, altura_texto_manual = texto_manual.get_size()
    largura_texto_automatico, altura_texto_automatico = texto_automatico.get_size()

    posicao_x_manual = (largura_janela - largura_texto_manual) // 2
    posicao_x_automatico = (largura_janela - largura_texto_automatico) // 2

    posicao_y_manual = (altura_janela - altura_texto_manual - altura_texto_automatico) // 2.1
    posicao_y_automatico = posicao_y_manual + altura_texto_manual + 30

    rodando = True
    modo = None

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicao_mouse = pygame.mouse.get_pos()
                if posicao_x_manual <= posicao_mouse[0] <= posicao_x_manual + largura_texto_manual and \
                        posicao_y_manual <= posicao_mouse[1] <= posicao_y_manual + altura_texto_manual:
                    modo = "manual"
                    rodando = False
                elif posicao_x_automatico <= posicao_mouse[0] <= posicao_x_automatico + largura_texto_automatico and \
                        posicao_y_automatico <= posicao_mouse[1] <= posicao_y_automatico + altura_texto_automatico:
                    modo = "automatico"
                    rodando = False

        janela_obs.fill(PRETO)
        janela_obs.blit(texto_opcao, (posicao_x_manual - 20, posicao_y_manual - 45))
        janela_obs.blit(texto_manual, (posicao_x_manual, posicao_y_manual))
        janela_obs.blit(texto_automatico, (posicao_x_automatico, posicao_y_automatico))
        pygame.display.flip()

    return modo


# Função para obter as dimensões do jogo do usuário usando uma interface gráfica
def obter_dimensoes_jogo():
    pygame.init()

    janela = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption("Escolha as Dimensões do Jogo")
    entrada_largura = ""
    entrada_altura = ""
    fonte = pygame.font.Font(minha_fonte, 24)
    cor_texto = pygame.Color(BRANCO)

    while True:
        janela.fill(pygame.Color(PRETO))
        texto_largura = fonte.render("Digite a dimensão da sala LxL de 6 - 20: " + entrada_largura, True, cor_texto)
        texto_rect = texto_largura.get_rect(center=(largura_janela // 2, altura_janela // 2))
        janela.blit(texto_largura, texto_rect)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    try:
                        largura = int(entrada_largura)
                        altura = int(entrada_altura)
                        return largura, altura
                    except ValueError:
                        entrada_largura = ""
                        entrada_altura = ""
                elif evento.key == pygame.K_BACKSPACE:
                    entrada_largura = entrada_largura[:-1]
                else:
                    entrada_largura += evento.unicode
                entrada_largura = entrada_largura[:3]

                if evento.key == pygame.K_BACKSPACE:
                    entrada_altura = entrada_altura[:-1]
                else:
                    entrada_altura += evento.unicode
                entrada_altura = entrada_altura[:3]
        pygame.display.flip()


# Função para escolher se o usuário deseja configurar as dimensões do jogo manualmente
def escolher_modo_dimensao():
    pygame.init()
    janela = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption("Escolha as Dimensões do Jogo")
    fonte = pygame.font.Font(minha_fonte, 24)
    cor_texto = pygame.Color(BRANCO)
    texto_pergunta = fonte.render("Você quer escolher as dimensões do jogo? ", True, cor_texto)

    texto_rect = texto_pergunta.get_rect(center=(largura_janela // 2, altura_janela // 2 - 50))

    botao_sim = pygame.Rect(largura_janela // 2 - 100, altura_janela // 2, 80, 40)
    botao_nao = pygame.Rect(largura_janela // 2 + 20, altura_janela // 2, 80, 40)

    while True:
        janela.fill(pygame.Color(PRETO))
        janela.blit(texto_pergunta, texto_rect)

        pygame.draw.rect(janela, VERDE, botao_sim)
        pygame.draw.rect(janela, VERMELHO, botao_nao)

        texto_sim = fonte.render("Sim", True, cor_texto)
        texto_nao = fonte.render("Não", True, cor_texto)
        janela.blit(texto_sim, (botao_sim.x + 20, botao_sim.y + 10))
        janela.blit(texto_nao, (botao_nao.x + 20, botao_nao.y + 10))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_sim.collidepoint(evento.pos):
                    return True
                elif botao_nao.collidepoint(evento.pos):
                    return False

        pygame.display.flip()


# Função para escolher o modo de configuração dos obstáculos: manual ou automático
def escolher_modo_obstaculo():
    pygame.init()

    janela = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption("Escolher Modo")
    fonte = pygame.font.Font(minha_fonte, 24)
    texto_opcao = fonte.render("Clique na opção:", True, CINZA_ESCURO)
    texto_manual = fonte.render("Escolher obstáculos", True, BRANCO)
    texto_automatico = fonte.render("Gerar obstáculos", True, BRANCO)

    largura_texto_manual, altura_texto_manual = texto_manual.get_size()
    largura_texto_automatico, altura_texto_automatico = texto_automatico.get_size()

    posicao_x_manual = (largura_janela - largura_texto_manual) // 2
    posicao_x_automatico = (largura_janela - largura_texto_automatico) // 2

    posicao_y_manual = (altura_janela - altura_texto_manual - altura_texto_automatico) // 2.1
    posicao_y_automatico = posicao_y_manual + altura_texto_manual + 30

    rodando = True
    modo = None

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicao_mouse = pygame.mouse.get_pos()
                if posicao_x_manual <= posicao_mouse[0] <= posicao_x_manual + largura_texto_manual and \
                        posicao_y_manual <= posicao_mouse[1] <= posicao_y_manual + altura_texto_manual:
                    modo = "manual"
                    rodando = False
                elif posicao_x_automatico <= posicao_mouse[0] <= posicao_x_automatico + largura_texto_automatico and \
                        posicao_y_automatico <= posicao_mouse[1] <= posicao_y_automatico + altura_texto_automatico:
                    modo = "automatico"
                    rodando = False

        janela.fill(PRETO)
        janela.blit(texto_opcao, (posicao_x_manual + 35, posicao_y_manual - 50))
        janela.blit(texto_manual, (posicao_x_manual, posicao_y_manual))
        janela.blit(texto_automatico, (posicao_x_automatico, posicao_y_automatico))
        pygame.display.flip()

    return modo


# Função para criar uma sala com obstáculos em posições específicas
def criar_sala(largura, altura):
    sala = [[False for _ in range(largura)] for _ in range(altura)]
    return sala


# Função para escolher as posições dos obstáculos manualmente
def escolher_posicao_obstaculo(janela, largura_salao, altura_salao):
    obstaculos = [[False for _ in range(largura_salao)] for _ in range(altura_salao)]
    sala = criar_sala(800, 600)
    lista_obstaculos = []
    tamanho_celula_obs = 50
    pygame.display.set_caption("Definir Obstáculos")

    # Renderiza a mensagem inicial na tela
    fonte_tutorial = pygame.font.Font(minha_fonte, 20)
    texto_tutorial1 = fonte_tutorial.render("Para escolher a posição do obstáculo, clique na célula referente.", True,
                                            BRANCO)
    texto_tutorial2 = fonte_tutorial.render("Após escolher, clique em ENTER para salvar.", True, BRANCO)
    texto_tutorial3 = fonte_tutorial.render("Clique em ESPAÇO para pular este tutorial.", True, CINZA_ESCURO)

    largura_texto1, altura_texto1 = texto_tutorial1.get_size()
    largura_texto2, altura_texto2 = texto_tutorial2.get_size()
    largura_texto3, altura_texto3 = texto_tutorial3.get_size()

    largura_tela, altura_tela = janela.get_size()
    x_texto1 = (largura_tela - largura_texto1) // 2
    y_texto1 = (altura_tela - altura_texto1 - altura_texto2 - altura_texto3) // 2

    x_texto2 = (largura_tela - largura_texto2) // 2
    y_texto2 = y_texto1 + altura_texto1

    x_texto3 = (largura_tela - largura_texto3) // 2
    y_texto3 = y_texto2 + altura_texto2 + 50

    janela.fill(PRETO)
    janela.blit(texto_tutorial1, (x_texto1, y_texto1))
    janela.blit(texto_tutorial2, (x_texto2, y_texto2))
    janela.blit(texto_tutorial3, (x_texto3, y_texto3))
    pygame.display.flip()

    esperando_instrucoes = True
    while esperando_instrucoes:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                esperando_instrucoes = False

    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                posicao_mouse = pygame.mouse.get_pos()
                x = posicao_mouse[0] // tamanho_celula_obs
                y = posicao_mouse[1] // tamanho_celula_obs
                sala[y][x] = not sala[y][x]
                if sala[y][x]:
                    lista_obstaculos.append((x, y))
                else:
                    lista_obstaculos.remove((x, y))
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                rodando = False

        janela.fill(PRETO)

        for y in range(altura_salao):
            for x in range(largura_salao):
                cor = PRETO if sala[y][x] else AZUL
                if cor == AZUL:
                    pygame.draw.rect(janela, cor,
                                     (x * tamanho_celula_obs, y * tamanho_celula_obs, tamanho_celula_obs,
                                      tamanho_celula_obs), 1)
                else:
                    pygame.draw.rect(janela, cor,
                                     (x * tamanho_celula_obs, y * tamanho_celula_obs, tamanho_celula_obs,
                                      tamanho_celula_obs), 0)

        pygame.display.flip()

    for x, y in lista_obstaculos:
        if (x, y) in [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]:
            # Se o obstáculo cair em uma das posições específicas, mova-o duas casas abaixo
            y = (y + 2) % altura_salao
        obstaculos[y][x] = True

    return obstaculos


# Função para configurar a largura e altura do salão de acordo com a escolha do usuário
def configurar_largura_altura():
    escolher_dimensoes = escolher_modo_dimensao()
    if escolher_dimensoes:
        l, a = obter_dimensoes_jogo()
        return l, a
    else:
        l, a = 10, 10
        return l, a

