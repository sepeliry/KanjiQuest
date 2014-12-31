# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 21:44:24 2014

@author: jussi
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from random import randint


DISPLAY_COLS = 11
DISPLAY_ROWS = 9

class KivyRogue(GridLayout):
    @staticmethod
    def get_forest_tile():
        tile_char = ' '
        
        key = randint(0,4)
        if key==0:
            tile_char = u'木'
            tile_color = (30,200,10,255)
        if key>=1:
            tile_char = u'草'
            tile_color = (10,80,5,255)
        
        color_code = '#%02x%02x%02x%02x' % tile_color
        return Button(
            text=u"[color=%s]%s[/color]" % (color_code,tile_char),
            #color=tile_color,
            font_size=48,
            markup = True,
            font_name='TakaoPMincho.ttf',
            background_color=(0,0,0,0))
            
    def __init__(self, **kwargs):
        super(KivyRogue, self).__init__(**kwargs)
        
        self._keyboard = Window.request_keyboard(self.on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)

        self.cols = DISPLAY_COLS
        self.tiles =  [[0 for x in range(DISPLAY_ROWS)] for x in range(DISPLAY_COLS)] 
        
        for y in range(DISPLAY_ROWS):
            for x in range(DISPLAY_COLS):
                nbtn = KivyRogue.get_forest_tile()
                self.tiles[x][y] = nbtn
                self.add_widget(nbtn)
                nbtn.bind(on_press=self.on_pressed)
        self.add_widget(Label(text="                                                                                         "+
        "St:12  Dx:32  Ld:33  HP:20/214  Jut:32  Spi:49/100" , halign='right', font_size=32))

        self.overlapped_btn = None
        player_btn = self.tiles[int(DISPLAY_ROWS/2)+1][int(DISPLAY_COLS/2)-1]
        self._set_player_to_stand_on(player_btn)
        
        
    def _get_x_y_for_btn(self, btn):
        for y in range(DISPLAY_ROWS):
            for x in range(DISPLAY_COLS):
                if btn==self.tiles[x][y]:
                    return (x,y)
        return (None, None)
        
    def _set_player_to_stand_on(self, btn):
        if self.overlapped_btn:
            self.overlapped_btn.text = self.overlapped_text
            
        self.overlapped_btn = btn
        self.overlapped_text = btn.text
        self.overlapped_btn.text = u"人"
        
    def on_pressed(self,obj):
        # Get the direction where the clicked tile was compared to current pos
        click_x,click_y = self._get_x_y_for_btn(obj)
        current_x,current_y = self._get_x_y_for_btn(self.overlapped_btn)
        dx = click_x-current_x
        dy = click_y-current_y
        # normalize
        ndx = int(dx/max(1,abs(dx)))
        ndy = int(dy/max(1,abs(dy)))
        
        self._set_player_to_stand_on(self.tiles[current_x+ndx][current_y+ndy])
       
    def on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None
        
    def on_keyboard_down(self, keyboard, keycode, text, modifiers):

        x, y = self._get_x_y_for_btn(self.overlapped_btn)
        
        if x!=None and y!=None:
            if keycode[1] == 'left':
                x = max(0, x-1)
            elif keycode[1] == 'right':
                x = min(DISPLAY_COLS-1, x+1)
            elif keycode[1] == 'up':
                y = max(0, y-1)
            elif keycode[1] == 'down':
                y = min(DISPLAY_ROWS-1, y+1)
        
        self._set_player_to_stand_on(self.tiles[x][y])
        

class MyApp(App):
    def build(self):
        return KivyRogue()


if __name__ == '__main__':
    MyApp().run()