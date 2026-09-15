import pygame 

from config import (
LARGURA ,
ALTURA ,
FPS ,
CINZA_ESCURO ,
PRETO 
)

from mecanicas import Jogo 


pygame .init ()

TELA =pygame .display .set_mode (
(LARGURA ,ALTURA )
)


pygame .display .set_caption (
"Sky Raider"
)

clock =pygame .time .Clock ()



from interface import (
desenhar_hud ,
desenhar_tela_game_over ,
desenhar_tela_inicio ,
desenhar_tela_instrucoes ,
desenhar_tela_creditos ,

btn_reiniciar_rect ,
btn_sair_rect ,
btn_iniciar_rect ,
btn_instrucoes_rect ,
btn_creditos_rect ,
btn_sair_menu_rect ,
btn_voltar_rect 
)



def main ():

    jogo =Jogo ()

    rodando =True 

    tela_atual ="MENU"


    while rodando :

        clock .tick (FPS )



        for event in pygame .event .get ():

            if event .type ==pygame .QUIT :

                rodando =False 




            if tela_atual =="MENU":

                if event .type ==pygame .MOUSEBUTTONDOWN :

                    if event .button ==1 :


                        if btn_iniciar_rect .collidepoint (event .pos ):

                            jogo .iniciar_partida ()

                            tela_atual ="JOGANDO"



                        elif btn_instrucoes_rect .collidepoint (event .pos ):

                            tela_atual ="INSTRUCOES"



                        elif btn_creditos_rect .collidepoint (event .pos ):

                            tela_atual ="CREDITOS"



                        elif btn_sair_menu_rect .collidepoint (event .pos ):

                            rodando =False 

            elif tela_atual =="INSTRUCOES":

                if event .type ==pygame .MOUSEBUTTONDOWN :

                    if event .button ==1 :

                        if btn_voltar_rect .collidepoint (event .pos ):

                            tela_atual ="MENU"


            elif tela_atual =="CREDITOS":

                if event .type ==pygame .MOUSEBUTTONDOWN :

                    if event .button ==1 :

                        if btn_voltar_rect .collidepoint (event .pos ):

                            tela_atual ="MENU"



            elif tela_atual =="JOGANDO":

                if event .type ==pygame .MOUSEBUTTONDOWN :

                    if event .button ==1 :

                        jogo .atirar (event .pos )




            elif tela_atual =="GAME_OVER":

                if event .type ==pygame .MOUSEBUTTONDOWN :

                    if event .button ==1 :


                        if btn_reiniciar_rect .collidepoint (event .pos ):

                            jogo .iniciar_partida ()

                            tela_atual ="JOGANDO"



                        elif btn_sair_rect .collidepoint (event .pos ):

                            rodando =False 




        if tela_atual =="MENU":

            desenhar_tela_inicio (TELA )


        elif tela_atual =="INSTRUCOES":

            desenhar_tela_instrucoes (TELA )


        elif tela_atual =="CREDITOS":

            desenhar_tela_creditos (TELA )


        elif tela_atual =="JOGANDO":

            jogo .atualizar ()

            TELA .fill (CINZA_ESCURO )

            jogo .todos_sprites .draw (TELA )

            desenhar_hud (
            TELA ,
            jogo .jogador ,
            jogo .pontos 
            )


            if jogo .estado =="GAME_OVER":

                tela_atual ="GAME_OVER"


        elif tela_atual =="GAME_OVER":

            desenhar_tela_game_over (TELA )


        pygame .display .flip ()


    pygame .quit ()



if __name__ =="__main__":

    main ()
