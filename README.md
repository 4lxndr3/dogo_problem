# Nina's Adventure

Nina's Adventure é um jogo interativo que utiliza o algoritmo de busca heurística A* 
para encontrar o caminho mais curto entre um ponto inicial (dogo) e um objetivo (osso), 
evitando obstáculos em um grid. O jogo possui uma interface gráfica criada com a biblioteca Pygame.

# Índice 

1. Visão Geral
2. Características
3. Instalação
4. Uso
5. Autores

# Visão Geral

O algoritmo A* é um dos mais populares para busca de caminhos devido à sua eficiência e capacidade de encontrar o caminho mais curto em um grafo ou grid. 
No jogo, você pode optar por dois modos: "Manual", onde você controla o dogo, e "Automático", onde o algoritmo encontra o caminho para você.

# Características

- Algoritmo A*: Implementação do algoritmo de busca A* para encontrar o caminho mais curto.
- Interface Gráfica: Desenvolvida com Pygame, com suporte para interação via teclado e mouse.
- Modos de Jogo:
  - Manual: Controle o dogo com as setas do teclado.
  - Automático: O algoritmo A* encontra o caminho até o osso.
- Personalização: Escolha manualmente as posições dos obstáculos ou gere-os automaticamente.
- Feedback Visual: Mensagens de status e feedback durante o jogo (ex: "Game Over", "Good Job!").

# Instalação

1. Python: Certifique-se de ter o Python instalado. Você pode baixá-lo em python.org.
2. Instalação do Pygame:
   - Use o pip instalar a biblioteca Pygame:
   
```bash
  pip install pygame
```
3. Executando o jogo:
   - No terminal (Linux/macOS) ou no prompt de comando (Windows), navegue até o diretório onde está o main.py e execute:
```bash
  python main.py
```

# Uso

1. Configuração Inicial:
   - Ao iniciar, uma janela perguntará se você deseja definir as dimensões do grid.
   - Pressione SIM ou NÃO.

2. Definição de Dimensões(se aplicável):
   - Insira o número de linhas e colunas desejadas e pressione Enter
3. Escolha de Obstáculos:
   - Clique em "Escolher obstáculos" para definir manualmente ou "Gerar obstáculos" para que o programa os gere aleatoriamente.
4. Definição de Obstáculos (se aplicável):
   - Siga o tutorial interativo para posicionar os obstáculos. Clique nas células para colocar ou remover obstáculos. Pressione Enter para salvar.
5. Seleção do Modo de Jogo:
   - Clique em "Modo Manual" ou "Modo Automático".
6. Modo Manual:
   - Use as setas do teclado para guiar o dogo até o osso, evitando obstáculos.

## Autores
- [Alexandre Gabriel Gadelha de Lima](https://github.com/4lxndr3)
- [Martinho Prata Dos Santos](https://github.com/Pratamartin)
- [Samuel Monteiro Gomes](https://github.com/samggg)

