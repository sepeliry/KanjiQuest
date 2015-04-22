# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 18:37:58 2015

@author: juherask
"""

from pygame import *

TILE_SIZE = 32

piirtopinta = Surface(1+16*TILE_SIZE, 1006*TILE_SIZE)


myfont = font.SysFont("Arial", 15)

# render text

merkisto = [
 ("ihminen", u"人"),
("ihminen", u"人"),
("ihminen", u"人")
]

for kanji in merkisto:
    selite = kanji[0]
    merkki = kanji[1]
    
    #TODO, piirrä 1. sarakkeeseen selite
    # 2-17 kanji merkki eri väreillä
    label = myfont.render("@", 1, (255,255,0))
    piirtopinta.blit(label, (100, 100))
    
