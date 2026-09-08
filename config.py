import pygame

pygame.init()

# TELA
LARGURA = 800
ALTURA = 600
FPS = 60

# CORES
PRETO = (10, 10, 10)
CINZA_ESCURO = (20, 20, 20)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
VERMELHO_CLARO = (255, 50, 50)
AMARELO = (255, 255, 0)
CINZA_BOTAO = (50, 50, 50)
CINZA_BOTAO_HOVER = (100, 100, 100)

# NOVAS CORES PARA ROBÔS E POWER-UPS
ROXO = (128, 0, 128)        # Robô Tanque
LARANJA = (255, 140, 0)     # Robô Atirador
AZUL_CLARO = (0, 191, 255)  # Tiro do inimigo
ROSA = (255, 105, 180)       # Power-up Vida Extra
CIANO = (0, 255, 255)       # Power-up Tiro Triplo
DOURADO = (255, 215, 0)     # Power-up Tiro Rápido
AZUL_ESC = (0, 0, 205)      # Power-up Escudo
