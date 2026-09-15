import os 
import pygame 

from config import (
LARGURA ,
ALTURA ,
BRANCO ,
VERMELHO_CLARO ,
CINZA_BOTAO ,
CINZA_BOTAO_HOVER 
)


pygame .font .init ()

fonte_titulo =pygame .font .SysFont ("arial",64 ,bold =True )
fonte_botao =pygame .font .SysFont ("arial",30 ,bold =True )
fonte_texto =pygame .font .SysFont ("arial",25 )
fonte_hud =pygame .font .SysFont (None ,30 )

PASTA_ASSETS =os .path .join (
os .path .dirname (__file__ ),
"assets"
)

caminho_fundo =os .path .join (PASTA_ASSETS ,"fundo_menu.jpg")
try :
    fundo_menu =pygame .image .load (caminho_fundo ).convert ()
    fundo_menu =pygame .transform .scale (fundo_menu ,(LARGURA ,ALTURA ))
except pygame .error :
    fundo_menu =pygame .Surface ((LARGURA ,ALTURA ))
    fundo_menu .fill ((40 ,140 ,210 ))

caminho_nave =os .path .join (PASTA_ASSETS ,"nave.png")
try :
    nave_menu =pygame .image .load (caminho_nave ).convert_alpha ()
    nave_menu =pygame .transform .scale (nave_menu ,(180 ,135 ))
except pygame .error :
    nave_menu =None 

caminho_jogador =os .path .join (PASTA_ASSETS ,"jogador.png")
try :
    jogador_menu =pygame .image .load (caminho_jogador ).convert_alpha ()
    jogador_menu =pygame .transform .scale (jogador_menu ,(180 ,180 ))
except pygame .error :
    jogador_menu =None 
btn_iniciar_rect =pygame .Rect (LARGURA //2 -130 ,285 ,260 ,55 )
btn_instrucoes_rect =pygame .Rect (LARGURA //2 -130 ,355 ,260 ,55 )
btn_creditos_rect =pygame .Rect (LARGURA //2 -130 ,425 ,260 ,55 )
btn_sair_menu_rect =pygame .Rect (LARGURA //2 -130 ,495 ,260 ,55 )

btn_voltar_rect =pygame .Rect (LARGURA //2 -110 ,500 ,220 ,55 )

btn_reiniciar_rect =pygame .Rect (LARGURA //2 -120 ,ALTURA //2 -10 ,240 ,50 )
btn_sair_rect =pygame .Rect (LARGURA //2 -120 ,ALTURA //2 +60 ,240 ,50 )

def desenhar_botao (tela ,rect ,texto ,cor_normal =None ):
    mouse =pygame .mouse .get_pos ()
    if cor_normal is None :
        cor_normal =CINZA_BOTAO 

    if rect .collidepoint (mouse ):
        cor =CINZA_BOTAO_HOVER 
        brilho =rect .inflate (8 ,8 )
        pygame .draw .rect (tela ,BRANCO ,brilho ,border_radius =12 )
    else :
        cor =cor_normal 

    pygame .draw .rect (tela ,cor ,rect ,border_radius =10 )
    pygame .draw .rect (tela ,BRANCO ,rect ,width =2 ,border_radius =10 )

    texto_render =fonte_botao .render (texto ,True ,BRANCO )
    texto_rect =texto_render .get_rect (center =rect .center )
    tela .blit (texto_render ,texto_rect )


def desenhar_tela_inicio (tela ):


    tela .blit (fundo_menu ,(0 ,0 ))


    if nave_menu is not None :
        tela .blit (nave_menu ,(35 ,175 ))


    if jogador_menu is not None :
        tela .blit (jogador_menu ,(585 ,345 ))


    desenhar_botao (tela ,btn_iniciar_rect ,"INICIAR JOGO")
    desenhar_botao (tela ,btn_instrucoes_rect ,"INSTRUÇÕES")
    desenhar_botao (tela ,btn_creditos_rect ,"CRÉDITOS")
    desenhar_botao (tela ,btn_sair_menu_rect ,"SAIR")

def desenhar_tela_instrucoes (tela ):
    tela .blit (fundo_menu ,(0 ,0 ))

    camada =pygame .Surface ((LARGURA ,ALTURA ),pygame .SRCALPHA )
    camada .fill ((0 ,0 ,0 ,130 ))
    tela .blit (camada ,(0 ,0 ))

    painel =pygame .Rect (140 ,60 ,520 ,500 )
    pygame .draw .rect (tela ,(30 ,30 ,30 ),painel ,border_radius =15 )
    pygame .draw .rect (tela ,BRANCO ,painel ,width =2 ,border_radius =15 )

    titulo =fonte_titulo .render ("INSTRUÇÕES",True ,BRANCO )
    tela .blit (titulo ,titulo .get_rect (center =(LARGURA //2 ,115 )))

    instrucoes =[
    "W A S D  -  Mover a nave",
    "",
    "Mouse  -  Mirar",
    "Clique esquerdo  -  Atirar",
    "",
    "Destrua os robôs inimigos",
    "e faça o máximo de pontos!",
    "",
    "Colete os Power-Ups para",
    "ficar mais forte."
    ]

    y =180 
    for linha in instrucoes :
        texto =fonte_texto .render (linha ,True ,BRANCO )
        tela .blit (texto ,texto .get_rect (center =(LARGURA //2 ,y )))
        y +=32 

    desenhar_botao (tela ,btn_voltar_rect ,"VOLTAR")


def desenhar_tela_creditos (tela ):
    tela .blit (fundo_menu ,(0 ,0 ))

    camada =pygame .Surface ((LARGURA ,ALTURA ),pygame .SRCALPHA )
    camada .fill ((0 ,0 ,0 ,130 ))
    tela .blit (camada ,(0 ,0 ))

    painel =pygame .Rect (140 ,70 ,520 ,480 )
    pygame .draw .rect (tela ,(30 ,30 ,30 ),painel ,border_radius =15 )
    pygame .draw .rect (tela ,BRANCO ,painel ,width =2 ,border_radius =15 )

    titulo =fonte_titulo .render ("CRÉDITOS",True ,BRANCO )
    tela .blit (titulo ,titulo .get_rect (center =(LARGURA //2 ,130 )))

    textos =[
    "SKY RAIDER",
    "",
    "Projeto desenvolvido em Python",
    "utilizando Pygame.",
    "",
    "Programação:",
    "Equipe do projeto",
    "",
    "Projeto de POO",
    ]

    y =190 
    for linha in textos :
        texto =fonte_texto .render (linha ,True ,BRANCO )
        tela .blit (texto ,texto .get_rect (center =(LARGURA //2 ,y )))
        y +=32 

    desenhar_botao (tela ,btn_voltar_rect ,"VOLTAR")


def desenhar_hud (tela ,jogador ,pontos ):
    status_escudo =" [ESCUDO]"if jogador .tem_escudo else ""
    texto =fonte_hud .render (
    f"Vida: {jogador .vida }{status_escudo }  |  Pontos: {pontos }",
    True ,
    BRANCO 
    )
    tela .blit (texto ,(10 ,10 ))


def desenhar_tela_game_over (tela ):
    tela .fill ((10 ,10 ,10 ))

    txt_game_over =fonte_titulo .render ("GAME OVER",True ,VERMELHO_CLARO )
    tela .blit (txt_game_over ,txt_game_over .get_rect (center =(LARGURA //2 ,ALTURA //3 )))

    desenhar_botao (tela ,btn_reiniciar_rect ,"NOVA PARTIDA")
    desenhar_botao (tela ,btn_sair_rect ,"SAIR")
