
import pygame

from config import (
    LARGURA,
    ALTURA,
    FPS,
    CINZA_ESCURO,
    PRETO
)

from mecanicas import Jogo

pygame.init()

TELA = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption(
    "Sky Raider"
)

clock = pygame.time.Clock()

from interface import (
    fundo_menu,
    desenhar_hud,
    desenhar_tela_game_over,
    desenhar_tela_inicio,
    desenhar_tela_instrucoes,
    desenhar_tela_creditos,
    btn_reiniciar_rect,
    btn_sair_rect,
    btn_iniciar_rect,
    btn_instrucoes_rect,
    btn_creditos_rect,
    btn_sair_menu_rect,
    btn_voltar_rect
)


def main():

    jogo = Jogo()

    rodando = True

    tela_atual = "MENU"

    musica_morte_tocando = False

    imagem_teju_morto = pygame.image.load(
        "assets/img/teju_morto.png"
    ).convert_alpha()

    imagem_teju_morto = pygame.transform.scale(
        imagem_teju_morto,
        (200, 130)
    )

    botao_voltar_teju = pygame.Rect(
        LARGURA // 2 - 120,
        ALTURA // 2 + 100,
        240,
        50
    )

    try:
        pygame.mixer.music.load("assets/sons/Hero_immortal.mp3")
        pygame.mixer.music.play(-1)

    except pygame.error:
        pass

    while rodando:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            if tela_atual == "MENU":

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:

                        if btn_iniciar_rect.collidepoint(event.pos):

                            jogo.iniciar_partida()
                            musica_morte_tocando = False
                            tela_atual = "JOGANDO"

                        elif btn_instrucoes_rect.collidepoint(event.pos):

                            tela_atual = "INSTRUCOES"

                        elif btn_creditos_rect.collidepoint(event.pos):

                            tela_atual = "CREDITOS"

                        elif btn_sair_menu_rect.collidepoint(event.pos):

                            rodando = False

            elif tela_atual == "INSTRUCOES":

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:

                        if btn_voltar_rect.collidepoint(event.pos):

                            tela_atual = "MENU"

            elif tela_atual == "CREDITOS":

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:

                        if btn_voltar_rect.collidepoint(event.pos):

                            tela_atual = "MENU"

            elif tela_atual == "JOGANDO":

                if jogo.teju_morto:

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if event.button == 1:

                            if botao_voltar_teju.collidepoint(event.pos):

                                if jogo.canal_som_teju is not None:
                                    jogo.canal_som_teju.stop()
                                    jogo.canal_som_teju = None

                                jogo.teju_morto = False

                                try:
                                    pygame.mixer.music.stop()
                                    pygame.mixer.music.load(
                                        "assets/sons/Having_energy.mp3"
                                    )
                                    pygame.mixer.music.play(-1)
                                except pygame.error as e:
                                    print(
                                        f"Não foi possível reproduzir a música: {e}"
                                    )

                else:

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if event.button == 1:

                            jogo.atirar(event.pos)

            elif tela_atual == "GAME_OVER":

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:

                        if btn_reiniciar_rect.collidepoint(event.pos):

                            jogo.iniciar_partida()
                            musica_morte_tocando = False
                            tela_atual = "JOGANDO"

                        elif btn_sair_rect.collidepoint(event.pos):

                            rodando = False

        if tela_atual == "MENU":

            desenhar_tela_inicio(TELA)

        elif tela_atual == "INSTRUCOES":

            desenhar_tela_instrucoes(TELA)

        elif tela_atual == "CREDITOS":

            desenhar_tela_creditos(TELA)

        elif tela_atual == "JOGANDO":

            if not jogo.teju_morto:
                jogo.atualizar()

            TELA.blit(fundo_menu, (0, 0))

            jogo.todos_sprites.draw(TELA)

            desenhar_hud(
                TELA,
                jogo.jogador,
                jogo.pontos
            )

            if jogo.teju_morto:

                camada = pygame.Surface(
                    (LARGURA, ALTURA),
                    pygame.SRCALPHA
                )

                camada.fill((0, 0, 0, 190))
                TELA.blit(camada, (0, 0))

                caixa = pygame.Rect(
                    LARGURA // 2 - 250,
                    ALTURA // 2 - 180,
                    500,
                    360
                )

                pygame.draw.rect(
                    TELA,
                    (25, 25, 35),
                    caixa,
                    border_radius=20
                )

                pygame.draw.rect(
                    TELA,
                    (220, 40, 40),
                    caixa,
                    width=4,
                    border_radius=20
                )

                fonte_titulo = pygame.font.Font(None, 48)
                fonte_texto = pygame.font.Font(None, 27)
                fonte_botao = pygame.font.Font(None, 29)

                titulo = fonte_titulo.render(
                    "O TEJU MORREU!",
                    True,
                    (255, 70, 70)
                )

                TELA.blit(
                    titulo,
                    titulo.get_rect(
                        center=(LARGURA // 2, ALTURA // 2 - 140)
                    )
                )

                TELA.blit(
                    imagem_teju_morto,
                    imagem_teju_morto.get_rect(
                        center=(LARGURA // 2, ALTURA // 2 - 45)
                    )
                )

                mensagem = fonte_texto.render(
                    "Voce realmente fez isso?",
                    True,
                    (255, 255, 255)
                )

                mensagem2 = fonte_texto.render(
                    "O Teju nao vai esquecer essa traicao!",
                    True,
                    (210, 210, 220)
                )

                TELA.blit(
                    mensagem,
                    mensagem.get_rect(
                        center=(LARGURA // 2, ALTURA // 2 + 35)
                    )
                )

                TELA.blit(
                    mensagem2,
                    mensagem2.get_rect(
                        center=(LARGURA // 2, ALTURA // 2 + 65)
                    )
                )

                pygame.draw.rect(
                    TELA,
                    (40, 150, 90),
                    botao_voltar_teju,
                    border_radius=12
                )

                pygame.draw.rect(
                    TELA,
                    (100, 230, 150),
                    botao_voltar_teju,
                    width=2,
                    border_radius=12
                )

                texto_botao = fonte_botao.render(
                    "VOLTAR AO JOGO",
                    True,
                    (255, 255, 255)
                )

                TELA.blit(
                    texto_botao,
                    texto_botao.get_rect(
                        center=botao_voltar_teju.center
                    )
                )

            if jogo.estado == "GAME_OVER":

                tela_atual = "GAME_OVER"

                if not musica_morte_tocando:

                    try:
                        pygame.mixer.music.load(
                            "assets/sons/som_derrota.mp3"
                        )
                        pygame.mixer.music.play()
                    except pygame.error:
                        pass

                    musica_morte_tocando = True

        elif tela_atual == "GAME_OVER":

            desenhar_tela_game_over(TELA)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
