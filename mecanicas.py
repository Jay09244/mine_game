# Mecânicas/regras do jogo.
# (spawn de robôs, colisões, reinício)

import random

import pygame

from config import LARGURA, ALTURA
from entidades import Jogador, RoboZigueZague, Tiro


class Jogo:

    def __init__(self):
        self.todos_sprites = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()

        self.jogador = None
        self.pontos = 0
        self.spawn_timer = 0
        self.estado = "JOGANDO"  # "JOGANDO" ou "GAME_OVER"

        self.reiniciar()

    def reiniciar(self):
        self.todos_sprites.empty()
        self.inimigos.empty()
        self.tiros.empty()

        self.jogador = Jogador(LARGURA // 2, ALTURA - 60)
        self.todos_sprites.add(self.jogador)

        self.pontos = 0
        self.spawn_timer = 0
        self.estado = "JOGANDO"

    def atirar(self, pos_alvo):
        tiro = Tiro(self.jogador.rect.centerx, self.jogador.rect.centery, pos_alvo)
        self.todos_sprites.add(tiro)
        self.tiros.add(tiro)

    def _spawnar_inimigos(self):
        self.spawn_timer += 1
        if self.spawn_timer > 40:
            robo = RoboZigueZague(random.randint(40, LARGURA - 40), -40)
            self.todos_sprites.add(robo)
            self.inimigos.add(robo)
            self.spawn_timer = 0

    def _verificar_colisoes(self):
        # colisão tiro x robô
        colisao = pygame.sprite.groupcollide(self.inimigos, self.tiros, True, True)
        self.pontos += len(colisao)

        # colisão robô x jogador
        if pygame.sprite.spritecollide(self.jogador, self.inimigos, True):
            self.jogador.vida -= 1
            if self.jogador.vida <= 0:
                self.estado = "GAME_OVER"

    def atualizar(self):
        self._spawnar_inimigos()
        self._verificar_colisoes()
        self.todos_sprites.update()
