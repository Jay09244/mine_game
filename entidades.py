#Entidades concretas do jogo (Jogador, Tiro, Robôs).

import pygame

from config import LARGURA, ALTURA, VERDE, VERMELHO, AMARELO
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


# TIRO DIRECIONAL
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


# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)
        self.image.fill(VERMELHO)

    def atualizar_posicao(self):
        raise NotImplementedError


# ROBO EXEMPLO — ZigueZague
class RoboZigueZague(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
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
    def _spawnar_inimigos(self):
        self.spawn_timer += 1
        
        # MUDANÇA 1: O intervalo entre os spawns agora varia aleatoriamente (entre 20 e 60 frames)
        if not hasattr(self, 'intervalo_spawn'):
            self.intervalo_spawn = random.randint(20, 60)

        if self.spawn_timer > self.intervalo_spawn:
            # MUDANÇA 2: Posições X e Y aleatórias no topo da tela
            x_aleatorio = random.randint(40, LARGURA - 40)
            y_aleatorio = random.randint(-80, -40)
            
            robo = RoboZigueZague(x_aleatorio, y_aleatorio)
            self.todos_sprites.add(robo)
            self.inimigos.add(robo)
            
            # MUDANÇA 3: Reseta o timer e sorteia o tempo do próximo spawn
            self.spawn_timer = 0
            self.intervalo_spawn = random.randint(20, 60)
