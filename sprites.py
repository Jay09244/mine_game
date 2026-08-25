# Sprite base do jogo.
# (imagem, rect, movimento)


import pygame


class Entidade(pygame.sprite.Sprite):
    #Classe base para qualquer objeto do jogo que se move na tela.

    def __init__(self, x, y, velocidade):
        super().__init__()
        self.velocidade = velocidade
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=(x, y))

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
