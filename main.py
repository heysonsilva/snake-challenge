import pygame
import sys
import random

pygame.init()

# DIMENSÕES DA TELA
tamanho_tela = (800, 800)
tela = pygame.display.set_mode(tamanho_tela)

# ATRIBUINDO O TÍTULO DO JOGO
pygame.display.set_caption("Snake Challenge 🐍")

# CORES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# FONTES
font = pygame.font.SysFont('arial', 35)

# FPS DO JOGO
clock = pygame.time.Clock()

# POSIÇÃO INICIAL DA COBRA
def inicializar_jogo():
    global cobra_posicao, cobra, direcao, mudar_direcao, fruit_pos, fruit_spawn, pontuacao, tempo_ultimo_movimento
    cobra_posicao = [100, 50]
    cobra = [[100, 50], [90, 50], [80, 50]]  # TAMANHO INICIAL DA COBRA
    direcao = 'RIGHT'
    mudar_direcao = direcao
    fruit_pos = [random.randrange(1, (tamanho_tela[0] // 10)) * 10,
                 random.randrange(1, (tamanho_tela[1] // 10)) * 10]
    fruit_spawn = True
    pontuacao = 0
    tempo_ultimo_movimento = 0  # Variável para controlar o tempo de movimento da fruta

inicializar_jogo()

# FUNÇÃO PARA DESENHAR O JOGO
def draw_game():
    tela.fill(WHITE)  # LIMPA A TELA COM A COR BRANCA

    # DESENHANDO A COBRA
    for pos in cobra:
        pygame.draw.rect(tela, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    # DESENHANDO A FRUTA
    pygame.draw.rect(tela, RED, pygame.Rect(fruit_pos[0], fruit_pos[1], 10, 10))

    # EXIBINDO A PONTUAÇÃO
    exibir_pontuacao = font.render(f"Pontuação: {pontuacao}", True, BLACK)
    tela.blit(exibir_pontuacao, [0, 0])

    # ATUALIZANDO A TELA
    pygame.display.flip()

# FUNÇÃO PARA MOVER A FRUTA APÓS A PONTUAÇÃO 10
def mover_fruta():
    global fruit_pos
    fruit_pos = [random.randrange(1, (tamanho_tela[0] // 10)) * 10,
                 random.randrange(1, (tamanho_tela[1] // 10)) * 10]

# FUNÇÃO PARA CONTROLAR O MOVIMENTO DA COBRA
def mover_cobra(mudar_direcao):
    global cobra_posicao, pontuacao

    if mudar_direcao == 'UP':
        cobra_posicao[1] -= 10
    if mudar_direcao == 'DOWN':
        cobra_posicao[1] += 10
    if mudar_direcao == 'LEFT':
        cobra_posicao[0] -= 10
    if mudar_direcao == 'RIGHT':
        cobra_posicao[0] += 10

    # ATUALIZA O CORPO DA COBRA
    cobra.insert(0, list(cobra_posicao))

    # SE A COBRA COMEU A FRUTA
    if cobra_posicao == fruit_pos:
        pontuacao += 1  # AUMENTA A PONTUAÇÃO
        return True  # COBRA COMEU A FRUTA, CRESCE
    else:
        cobra.pop()  # REMOVE A ÚLTIMA PARTE DA COBRA (NÃO CRESCE)
        return False

# FUNÇÃO PARA VERIFICAR COLISÕES
def verificar_colisao():
    # COLISÃO COM AS BORDAS
    if cobra_posicao[0] < 0 or cobra_posicao[0] >= tamanho_tela[0] or cobra_posicao[1] < 0 or cobra_posicao[1] >= tamanho_tela[1]:
        return True

    # COLISÃO COM O PRÓPRIO CORPO
    for parte in cobra[1:]:
        if cobra_posicao == parte:
            return True

    return False

# FUNÇÃO PARA EXIBIR A PONTUAÇÃO FINAL E PERGUNTAR SE DESEJA JOGAR NOVAMENTE
def fim_de_jogo():
    tela.fill(WHITE)
    mensagem_fim = font.render(f" Pontuação: {pontuacao}", True, BLACK)
    mensagem_novamente = font.render("Jogar Novamente: ESPAÇO // ESC: sair", True, BLACK)
    tela.blit(mensagem_fim, [tamanho_tela[0] // 4, tamanho_tela[1] // 3])
    tela.blit(mensagem_novamente, [tamanho_tela[0] // 20, tamanho_tela[1] // 2])
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # JOGAR NOVAMENTE
                    inicializar_jogo()
                    return
                if event.key == pygame.K_ESCAPE:  # SAIR
                    pygame.quit()
                    sys.exit()

# LOOP PRINCIPAL DO JOGO
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # CONTROLE DE DIREÇÃO
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direcao != 'DOWN':
                mudar_direcao = 'UP'
            if event.key == pygame.K_DOWN and direcao != 'UP':
                mudar_direcao = 'DOWN'
            if event.key == pygame.K_LEFT and direcao != 'RIGHT':
                mudar_direcao = 'LEFT'
            if event.key == pygame.K_RIGHT and direcao != 'LEFT':
                mudar_direcao = 'RIGHT'

    direcao = mudar_direcao  # ATUALIZA A DIREÇÃO COM BASE NO INPUT DO USUÁRIO

    # MOVER A COBRA
    if mover_cobra(direcao):
        fruit_pos = [random.randrange(1, (tamanho_tela[0] // 10)) * 10,
                     random.randrange(1, (tamanho_tela[1] // 10)) * 10]  # GERA UMA NOVA FRUTA

    # VERIFICAR SE HOUVE COLISÃO
    if verificar_colisao():
        fim_de_jogo()

    # MOVER A FRUTA AUTOMATICAMENTE APÓS A PONTUAÇÃO 10
    if pontuacao >= 10:
        tempo_atual = pygame.time.get_ticks()  # OBTÉM O TEMPO ATUAL DO JOGO
        if tempo_atual - tempo_ultimo_movimento > 3000:  # MOVE A CADA 1 SEGUNDO
            mover_fruta()
            tempo_ultimo_movimento = tempo_atual  # ATUALIZA O TEMPO DO ÚLTIMO MOVIMENTO

    # DESENHAR O JOGO
    draw_game()
    

    # CONTROLAR A TAXA DE ATUALIZAÇÃO DO JOGO
    clock.tick(15)
