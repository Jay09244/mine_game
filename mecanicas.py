import random
import pygame

from config import LARGURA, ALTURA
from entidades import (
    Jogador, Tiro, RoboZigueZague, RoboTanque, RoboAtirador
)

class Jogo:
    def __init__(self):
        self.todos_sprites = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()
        self.tiros_inimigos = pygame.sprite.Group() # Novo grupo de tiros

        self.jogador = None
        self.pontos = 0
        self.spawn_timer = 0
        self.intervalo_spawn = 40
        self.estado = "JOGANDO"

        self.reiniciar()

    def reiniciar(self):
        self.todos_sprites.empty()
        self.inimigos.empty()
        self.tiros.empty()
        self.tiros_inimigos.empty()

        self.jogador = Jogador(LARGURA // 2, ALTURA - 60)
        self.todos_sprites.add(self.jogador)

        self.pontos = 0
        self.spawn_timer = 0
        self.intervalo_spawn = 40
        self.estado = "JOGANDO"

    def atirar(self, pos_alvo):
        tiro = Tiro(self.jogador.rect.centerx, self.jogador.rect.centery, pos_alvo)
        self.todos_sprites.add(tiro)
        self.tiros.add(tiro)

    def _spawnar_inimigos(self):
        self.spawn_timer += 1
        if self.spawn_timer > self.intervalo_spawn:
            x_aleatorio = random.randint(40, LARGURA - 40)
            y_aleatorio = random.randint(-80, -40)

            # Sorteia qual tipo de robô será criado
            tipo_robo = random.choice(["zigue_zague", "tanque", "atirador"])

            if tipo_robo == "zigue_zague":
                robo = RoboZigueZague(x_aleatorio, y_aleatorio)
            elif tipo_robo == "tanque":
                robo = RoboTanque(x_aleatorio, y_aleatorio)
            else:
                robo = RoboAtirador(x_aleatorio, y_aleatorio)

            self.todos_sprites.add(robo)
            self.inimigos.add(robo)

            self.spawn_timer = 0
            self.intervalo_spawn = random.randint(20, 60)

    def _processar_ataques_inimigos(self):
            # Passa a posição atual do jogador para os robôs atiradores
            if self.jogador:
                pos_jogador = self.jogador.rect.center
                for inimigo in self.inimigos:
                    if isinstance(inimigo, RoboAtirador):
                        novo_tiro = inimigo.tentar_atirar(pos_jogador)
                        if novo_tiro:
                            self.todos_sprites.add(novo_tiro)
                            self.tiros_inimigos.add(novo_tiro)

    def _verificar_colisoes(self):
        # 1. Colisão: Tiro do Jogador x Inimigos
        colisoes = pygame.sprite.groupcollide(self.inimigos, self.tiros, False, True)
        for inimigo, lista_tiros in colisoes.items():
            inimigo.vida -= len(lista_tiros) # Subtrai a vida baseada nos tiros recebidos
            if inimigo.vida <= 0:
                inimigo.kill()
                self.pontos += 1

        # 2. Colisão: Robô x Jogador
        if pygame.sprite.spritecollide(self.jogador, self.inimigos, True):
            self.jogador.vida -= 1
            if self.jogador.vida <= 0:
                self.estado = "GAME_OVER"

        # 3. Colisão: Tiro Inimigo x Jogador
        if pygame.sprite.spritecollide(self.jogador, self.tiros_inimigos, True):
            self.jogador.vida -= 1
            if self.jogador.vida <= 0:
                self.estado = "GAME_OVER"

    def atualizar(self):
        self._spawnar_inimigos()
        self._processar_ataques_inimigos()
        self._verificar_colisoes()
        self.todos_sprites.update()
