#Entidades concretas do jogo (Jogador, Tiro, Robôs).

import pygame

from config import LARGURA, ALTURA, VERDE, VERMELHO, AMARELO, AZUL_CLARO, LARANJA, ROXO
from sprites import Entidade
import random


# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.image.fill(VERDE)
        self.vida = 5

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.mover(0, -self.velocidade)
        if keys[pygame.K_s]:
            self.mover(0, self.velocidade)
        if keys[pygame.K_a]:
            self.mover(-self.velocidade, 0)
        if keys[pygame.K_d]:
            self.mover(self.velocidade, 0)

        # limites de tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - 40))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 40))


# TIRO DIRECIONAL DO PLAYER
class Tiro(Entidade):
    def __init__(self, x, y, alvo_pos):
        super().__init__(x, y, 12)
        self.image = pygame.Surface((10, 10))
        self.image.fill(AMARELO)
        self.pos = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=(x, y))

        direcao = pygame.math.Vector2(alvo_pos) - self.pos
        if direcao.length() > 0:
            self.direcao = direcao.normalize()
        else:
            self.direcao = pygame.math.Vector2(0, -1)

    def update(self):
        self.pos += self.direcao * self.velocidade
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if (self.rect.right < 0 or self.rect.left > LARGURA or
                self.rect.bottom < 0 or self.rect.top > ALTURA):
            self.kill()

class TiroInimigo(Entidade):
    def __init__(self, x, y, alvo_pos):
        super().__init__(x, y, velocidade=5)
        self.image = pygame.Surface((8, 8))
        self.image.fill(AZUL_CLARO)
        self.pos = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=(x, y))

        # Calcula o vetor de direção até o jogador
        direcao = pygame.math.Vector2(alvo_pos) - self.pos
        if direcao.length() > 0:
            self.direcao = direcao.normalize()
        else:
            self.direcao = pygame.math.Vector2(0, 1)

    def update(self):
        self.pos += self.direcao * self.velocidade
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if (self.rect.right < 0 or self.rect.left > LARGURA or
                self.rect.bottom < 0 or self.rect.top > ALTURA):
            self.kill()


# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y, velocidade, vida=1):
        super().__init__(x, y, velocidade)
        self.vida = vida
        self.image.fill(VERMELHO)

    def atualizar_posicao(self):
        raise NotImplementedError


# 1. ROBO ZIGUEZAGUE (Cor: Vermelho, 1 tiro)
class RoboZigueZague(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3, vida=1)
        self.direcao = 1

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * 3

        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()


# 2. ROBO TANQUE (Cor: Roxo, 3 tiros)
class RoboTanque(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=1, vida=3)  # Mais lento, porém mais vida
        self.image.fill(ROXO)

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA:
            self.kill()


# 3. ROBO ATIRADOR (Cor: Laranja, atira no jogador)
class RoboAtirador(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=2, vida=1)
        self.image.fill(LARANJA)
        self.timer_tiro = 0

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA:
            self.kill()

    def tentar_atirar(self, jogador_pos):
        self.timer_tiro += 1
        if self.timer_tiro >= 90:
            self.timer_tiro = 0
            return TiroInimigo(self.rect.centerx, self.rect.bottom, jogador_pos)
        return None
