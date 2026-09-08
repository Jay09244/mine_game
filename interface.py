import pygame

from config import (
    LARGURA, ALTURA, BRANCO, VERMELHO_CLARO, CINZA_BOTAO, CINZA_BOTAO_HOVER,
)

fonte_titulo = pygame.font.SysFont(None, 64)
fonte_botao = pygame.font.SysFont(None, 36)
fonte_hud = pygame.font.SysFont(None, 30)

btn_iniciar_rect = pygame.Rect(LARGURA // 2 - 120, ALTURA // 2 + 10, 240, 50)
btn_reiniciar_rect = pygame.Rect(LARGURA // 2 - 120, ALTURA // 2 - 10, 240, 50)
btn_sair_rect = pygame.Rect(LARGURA // 2 - 120, ALTURA // 2 + 60, 240, 50)


def desenhar_tela_inicio(tela):
    txt_titulo = fonte_titulo.render("SKY RAIDER", True, BRANCO)
    rect_titulo = txt_titulo.get_rect(center=(LARGURA // 2, ALTURA // 3))
    tela.blit(txt_titulo, rect_titulo)

    pos_mouse = pygame.mouse.get_pos()
    cor_btn = CINZA_BOTAO_HOVER if btn_iniciar_rect.collidepoint(pos_mouse) else CINZA_BOTAO

    pygame.draw.rect(tela, cor_btn, btn_iniciar_rect, border_radius=8)
    txt_iniciar = fonte_botao.render("Iniciar Jogo", True, BRANCO)
    tela.blit(txt_iniciar, txt_iniciar.get_rect(center=btn_iniciar_rect.center))


def desenhar_hud(tela, jogador, pontos):
    status_escudo = " [ESCUDO]" if jogador.tem_escudo else ""
    texto = fonte_hud.render(f"Vida: {jogador.vida}{status_escudo}  |  Pontos: {pontos}", True, BRANCO)
    tela.blit(texto, (10, 10))


def desenhar_tela_game_over(tela):
    txt_game_over = fonte_titulo.render("GAME OVER", True, VERMELHO_CLARO)
    rect_go = txt_game_over.get_rect(center=(LARGURA // 2, ALTURA // 3))
    tela.blit(txt_game_over, rect_go)

    pos_mouse = pygame.mouse.get_pos()
    cor_btn_reiniciar = CINZA_BOTAO_HOVER if btn_reiniciar_rect.collidepoint(pos_mouse) else CINZA_BOTAO
    cor_btn_sair = CINZA_BOTAO_HOVER if btn_sair_rect.collidepoint(pos_mouse) else CINZA_BOTAO

    pygame.draw.rect(tela, cor_btn_reiniciar, btn_reiniciar_rect, border_radius=8)
    txt_reiniciar = fonte_botao.render("Nova Partida", True, BRANCO)
    tela.blit(txt_reiniciar, txt_reiniciar.get_rect(center=btn_reiniciar_rect.center))

    pygame.draw.rect(tela, cor_btn_sair, btn_sair_rect, border_radius=8)
    txt_sair = fonte_botao.render("Sair", True, BRANCO)
    tela.blit(txt_sair, txt_sair.get_rect(center=btn_sair_rect.center))
