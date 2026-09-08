import pygame

from config import LARGURA, ALTURA, FPS, CINZA_ESCURO, PRETO
from mecanicas import Jogo
from interface import (
    desenhar_hud, desenhar_tela_game_over, desenhar_tela_inicio,
    btn_reiniciar_rect, btn_sair_rect, btn_iniciar_rect
)

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Sky Raider")

clock = pygame.time.Clock()


def main():
    jogo = Jogo()
    rodando = True

    while rodando:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            if jogo.estado == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if btn_iniciar_rect.collidepoint(event.pos):
                        jogo.iniciar_partida()

            elif jogo.estado == "JOGANDO":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    jogo.atirar(event.pos)

            elif jogo.estado == "GAME_OVER":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if btn_reiniciar_rect.collidepoint(event.pos):
                        jogo.iniciar_partida()
                    elif btn_sair_rect.collidepoint(event.pos):
                        rodando = False

        if jogo.estado == "MENU":
            TELA.fill(PRETO)
            desenhar_tela_inicio(TELA)

        elif jogo.estado == "JOGANDO":
            jogo.atualizar()
            TELA.fill(CINZA_ESCURO)
            jogo.todos_sprites.draw(TELA)
            desenhar_hud(TELA, jogo.jogador, jogo.pontos)

        elif jogo.estado == "GAME_OVER":
            TELA.fill(PRETO)
            desenhar_tela_game_over(TELA)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
