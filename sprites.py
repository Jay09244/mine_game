import pygame 


class Entidade (pygame .sprite .Sprite ):
    def _init_ (self ,x ,y ,velocidade ):
        super ()._init_ ()
        self .velocidade =velocidade 
        self .image =pygame .Surface ((40 ,40 ))
        self .rect =self .image .get_rect (center =(x ,y ))

    def mover (self ,dx ,dy ):
        self .rect .x +=dx 
        self .rect .y +=dy