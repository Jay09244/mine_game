#Interface visual fora do jogo: HUD (vida/pontos) e a tela de Game Over

import pygame

from config import (
    LARGURA, ALTURA, BRANCO, VERMELHO_CLARO, CINZA_BOTAO, CINZA_BOTAO_HOVER,
)

fonte_titulo = pygame.font.SysFont(None, 64)
fonte_botao = pygame.font.SysFont(None, 36)
fonte_hud = pygame.font.SysFont(None, 30)

btn_reiniciar_rect = pygame.Rect(LARGURA // 2 - 120, ALTURA // 2 - 10, 240, 50)
btn_sair_rect = pygame.Rect(LARGURA // 2 - 120, ALTURA // 2 + 60, 240, 50)


def desenhar_hud(tela, jogador, pontos):
    texto = fonte_hud.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, BRANCO)
    tela.blit(texto, (10, 10))


def desenhar_tela_game_over(tela):
    # Título
    txt_game_over = fonte_titulo.render("GAME OVER", True, VERMELHO_CLARO)
    rect_go = txt_game_over.get_rect(center=(LARGURA // 2, ALTURA // 3))
    tela.blit(txt_game_over, rect_go)

    # Hover nos botões
    pos_mouse = pygame.mouse.get_pos()
    cor_btn_reiniciar = CINZA_BOTAO_HOVER if btn_reiniciar_rect.collidepoint(pos_mouse) else CINZA_BOTAO
    cor_btn_sair = CINZA_BOTAO_HOVER if btn_sair_rect.collidepoint(pos_mouse) else CINZA_BOTAO

    # Botão "Nova Partida"
    pygame.draw.rect(tela, cor_btn_reiniciar, btn_reiniciar_rect, border_radius=8)
    txt_reiniciar = fonte_botao.render("Nova Partida", True, BRANCO)
    tela.blit(txt_reiniciar, txt_reiniciar.get_rect(center=btn_reiniciar_rect.center))

    # Botão "Sair"
    pygame.draw.rect(tela, cor_btn_sair, btn_sair_rect, border_radius=8)
    txt_sair = fonte_botao.render("Sair", True, BRANCO)
    tela.blit(txt_sair, txt_sair.get_rect(center=btn_sair_rect.center))
