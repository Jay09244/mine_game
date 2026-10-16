import pygame
import os

from config import (
    LARGURA, ALTURA, VERDE, VERMELHO, AMARELO, ROXO, LARANJA,
    AZUL_CLARO, ROSA, CIANO, DOURADO, AZUL_ESC
)
from sprites import Entidade


PASTA_ASSETS = os.path.join(os.path.dirname(__file__), "assets")


def carregar_sprite(nome, tamanho=(140, 140)):
    caminho = os.path.join(PASTA_ASSETS, nome)
    imagem = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(imagem, tamanho)


class PowerUp(Entidade):
    def __init__(self, x, y, tipo):
        super().__init__(x, y, velocidade=2)
        self.tipo = tipo
        self.image = pygame.Surface((16, 16))

        if tipo == "vida":
            self.image.fill(ROSA)
        elif tipo == "tiro_triplo":
            self.image.fill(CIANO)
        elif tipo == "tiro_rapido":
            self.image.fill(DOURADO)
        elif tipo == "escudo":
            self.image.fill(AZUL_ESC)

        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA:
            self.kill()


class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.image = carregar_sprite("jogador.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.vida = 5
        self.tem_escudo = False
        self.tempo_tiro_triplo = 0
        self.tempo_tiro_rapido = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.mover(-self.velocidade, 0)
        if keys[pygame.K_d]:
            self.mover(self.velocidade, 0)

        if self.tempo_tiro_triplo > 0:
            self.tempo_tiro_triplo -= 1
        if self.tempo_tiro_rapido > 0:
            self.tempo_tiro_rapido -= 1

        self.rect.x = max(0, min(self.rect.x, LARGURA - 40))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 40))

    def levar_dano(self):
        if self.tem_escudo:
            self.tem_escudo = False
            return False
        self.vida -= 1
        return self.vida <= 0


class Teju(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = carregar_sprite("teju.png", (110, 70))
        self.rect = self.image.get_rect(
            midbottom=(LARGURA // 2 + 100, ALTURA - 20)
        )
        self.vida = 1


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

        if (
            self.rect.right < 0 or self.rect.left > LARGURA or
            self.rect.bottom < 0 or self.rect.top > ALTURA
        ):
            self.kill()


class TiroInimigo(Entidade):
    def __init__(self, x, y, alvo_pos):
        super().__init__(x, y, velocidade=5)
        self.image = pygame.Surface((8, 8))
        self.image.fill(AZUL_CLARO)
        self.pos = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=(x, y))

        direcao = pygame.math.Vector2(alvo_pos) - self.pos
        if direcao.length() > 0:
            self.direcao = direcao.normalize()
        else:
            self.direcao = pygame.math.Vector2(0, 1)

    def update(self):
        self.pos += self.direcao * self.velocidade
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if (
            self.rect.right < 0 or self.rect.left > LARGURA or
            self.rect.bottom < 0 or self.rect.top > ALTURA
        ):
            self.kill()


class Robo(Entidade):
    def __init__(self, x, y, velocidade, vida=1):
        super().__init__(x, y, velocidade)
        self.vida = vida
        self.image = carregar_sprite("nave.png")
        self.rect = self.image.get_rect(center=(x, y))

    def atualizar_posicao(self):
        raise NotImplementedError


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


class RoboTanque(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=1, vida=3)

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA:
            self.kill()


class RoboAtirador(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=2, vida=1)
        self.timer_tiro = 0

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA:
            self.kill()

    def tentar_atirar(self, jogador_pos):
        self.timer_tiro += 1
        if self.timer_tiro >= 90:
            self.timer_tiro = 0
            return TiroInimigo(
                self.rect.centerx,
                self.rect.bottom,
                jogador_pos
            )
        return None
