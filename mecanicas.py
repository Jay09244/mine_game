import random
import pygame

from config import LARGURA, ALTURA
from entidades import (
    Jogador, Tiro, RoboZigueZague, RoboTanque, RoboAtirador, PowerUp
)


class Jogo:
    def __init__(self):
        self.todos_sprites = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()
        self.tiros_inimigos = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.jogador = None
        self.pontos = 0
        self.spawn_timer = 0
        self.intervalo_spawn = 40
        self.cadencia_tiro_timer = 0
        self.estado = "MENU"

    def iniciar_partida(self):
        self.reiniciar()
        self.estado = "JOGANDO"

    def reiniciar(self):
        self.todos_sprites.empty()
        self.inimigos.empty()
        self.tiros.empty()
        self.tiros_inimigos.empty()
        self.powerups.empty()

        self.jogador = Jogador(LARGURA // 2, ALTURA - 60)
        self.todos_sprites.add(self.jogador)

        self.pontos = 0
        self.spawn_timer = 0
        self.intervalo_spawn = 40
        self.cadencia_tiro_timer = 0

    def atirar(self, pos_alvo):
        delay_necessario = 5 if self.jogador.tempo_tiro_rapido > 0 else 15
        if self.cadencia_tiro_timer < delay_necessario:
            return

        self.cadencia_tiro_timer = 0

        if self.jogador.tempo_tiro_triplo > 0:
            offsets = [-20, 0, 20]
            for offset in offsets:
                alvo_offset = (pos_alvo[0] + offset, pos_alvo[1])
                tiro = Tiro(self.jogador.rect.centerx, self.jogador.rect.centery, alvo_offset)
                self.todos_sprites.add(tiro)
                self.tiros.add(tiro)
        else:
            tiro = Tiro(self.jogador.rect.centerx, self.jogador.rect.centery, pos_alvo)
            self.todos_sprites.add(tiro)
            self.tiros.add(tiro)

    def _tentar_dropar_powerup(self, inimigo):
        chances = random.random()

        if isinstance(inimigo, RoboZigueZague):
            if chances < 0.25:
                p = PowerUp(inimigo.rect.centerx, inimigo.rect.centery, "vida")
                self.todos_sprites.add(p)
                self.powerups.add(p)

        elif isinstance(inimigo, RoboAtirador):
            if chances < 0.20:
                p = PowerUp(inimigo.rect.centerx, inimigo.rect.centery, "tiro_triplo")
                self.todos_sprites.add(p)
                self.powerups.add(p)
            elif chances < 0.40:
                p = PowerUp(inimigo.rect.centerx, inimigo.rect.centery, "tiro_rapido")
                self.todos_sprites.add(p)
                self.powerups.add(p)

        elif isinstance(inimigo, RoboTanque):
            if chances < 0.30:
                p = PowerUp(inimigo.rect.centerx, inimigo.rect.centery, "escudo")
                self.todos_sprites.add(p)
                self.powerups.add(p)

    def _spawnar_inimigos(self):
        self.spawn_timer += 1
        if self.spawn_timer > self.intervalo_spawn:
            x_aleatorio = random.randint(40, LARGURA - 40)
            y_aleatorio = random.randint(-80, -40)

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
        if self.jogador:
            pos_jogador = self.jogador.rect.center
            for inimigo in self.inimigos:
                if isinstance(inimigo, RoboAtirador):
                    novo_tiro = inimigo.tentar_atirar(pos_jogador)
                    if novo_tiro:
                        self.todos_sprites.add(novo_tiro)
                        self.tiros_inimigos.add(novo_tiro)

    def _verificar_colisoes(self):
        colisoes = pygame.sprite.groupcollide(self.inimigos, self.tiros, False, True)
        for inimigo, lista_tiros in colisoes.items():
            inimigo.vida -= len(lista_tiros)
            if inimigo.vida <= 0:
                self._tentar_dropar_powerup(inimigo)
                inimigo.kill()
                self.pontos += 1

        if pygame.sprite.spritecollide(self.jogador, self.inimigos, True):
            if self.jogador.levar_dano():
                self.estado = "GAME_OVER"

        if pygame.sprite.spritecollide(self.jogador, self.tiros_inimigos, True):
            if self.jogador.levar_dano():
                self.estado = "GAME_OVER"

        powerups_coletados = pygame.sprite.spritecollide(self.jogador, self.powerups, True)
        for p in powerups_coletados:
            if p.tipo == "vida":
                self.jogador.vida += 1
            elif p.tipo == "tiro_triplo":
                self.jogador.tempo_tiro_triplo = 300
            elif p.tipo == "tiro_rapido":
                self.jogador.tempo_tiro_rapido = 300
            elif p.tipo == "escudo":
                self.jogador.tem_escudo = True

    def atualizar(self):
        self.cadencia_tiro_timer += 1
        self._spawnar_inimigos()
        self._processar_ataques_inimigos()
        self._verificar_colisoes()
        self.todos_sprites.update()
