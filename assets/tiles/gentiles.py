# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 18:37:58 2015
Last modified on 29.4.2015

@original author: juherask
@modifications: Jani Vuolle (ja.vuolle@gmail.com)
"""

from itertools import chain
 
def truncline(text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
        return real, done, stext             
        
def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped
 
 
def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)

import pygame as pg

pg.init();

screen = pg.display.set_mode((1024,768))

# colors
WHITE = [255,255,255]
GREY = [128,128,128]
BLUE = [0,0,200]
RED = [200,0,0]
GREEN = [0,200,0]
YELLOW = [255,255,0]
ORANGE = [255,128,0]
TEAL = [0,204,204]
PURPLE = [127,0,255]
BROWN = [102,51,0]
LBLUE = [51,153,255]
LGREEN = [51,255,51]
LBROWN = [210,180,140]
DRED = [110,10,30]

TILE_SIZE = 32 # desired tile size

kanji_font = pg.font.SysFont("TakaoPMincho", TILE_SIZE)

# render text
"""
merkisto = [
("henkilö", "人"),
("ruoho", "草"),
("ovi", "戸"),
("puu", "木"),
("kulta/raha", "金")
]
"""
merkisto = []
file = open("kanji_list.txt", encoding="utf8")

with file as ins:
    for line in ins:
        value = line.split(";");
        merkisto.append((value[1],value[0]))

current_row = 0

piirtopinta = pg.Surface((1+16*TILE_SIZE, len(merkisto)*TILE_SIZE))


for kanji in merkisto:
    selite = kanji[0]
    merkki = kanji[1]
    
    current_column = 0

    
    selite_font = pg.font.SysFont("Arial", 12)
    selite_array = wrapline(str(current_row) + '.' + selite,selite_font,TILE_SIZE)
    label = selite_font.render(selite_array[0], 1, (WHITE))
    piirtopinta.blit(label, (0, current_row*TILE_SIZE))
    
    if len(selite_array) > 1:
        label = selite_font.render(selite_array[1], 1, (WHITE))
        piirtopinta.blit(label, (0, current_row*TILE_SIZE+13))
    
    label = kanji_font.render(merkki, 1, (WHITE))
    piirtopinta.blit(label, (TILE_SIZE, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (GREY))
    piirtopinta.blit(label, (TILE_SIZE*2, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (BLUE))
    piirtopinta.blit(label, (TILE_SIZE*3, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (RED))
    piirtopinta.blit(label, (TILE_SIZE*4, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (GREEN))
    piirtopinta.blit(label, (TILE_SIZE*5, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (YELLOW))
    piirtopinta.blit(label, (TILE_SIZE*6, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (ORANGE))
    piirtopinta.blit(label, (TILE_SIZE*7, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (TEAL))
    piirtopinta.blit(label, (TILE_SIZE*8, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (PURPLE))
    piirtopinta.blit(label, (TILE_SIZE*9, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (BROWN))
    piirtopinta.blit(label, (TILE_SIZE*10, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (LBLUE))
    piirtopinta.blit(label, (TILE_SIZE*11, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (LGREEN))
    piirtopinta.blit(label, (TILE_SIZE*12, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (LBROWN))
    piirtopinta.blit(label, (TILE_SIZE*13, current_row*TILE_SIZE))
    label = kanji_font.render(merkki, 1, (DRED))
    piirtopinta.blit(label, (TILE_SIZE*14, current_row*TILE_SIZE))

    current_row += 1
#screen.blit(piirtopinta, (0,0))
