import pygame
from button import Button
from typing import List, Tuple

from text import Text

class Menu:
    def __init__(self, window:pygame.Surface, window_size:tuple, size:tuple, offset:tuple=(0, 0), color:tuple=(50, 50, 50, 255)):
        self.toggled = False
        self.window = window
        self.window_size = window_size
        self.pos = (window_size[0] / 2 - size[0] / 2 - offset[0], window_size[1] / 2 - size[1] / 2 - offset[1])
        self.size = size
        self.color = color

        self.menu = pygame.Surface(self.size)
        self.menu.set_alpha(self.color[3])
        self.menu.fill(self.color)

        self.buttons = []
        self.text = []

    
    def draw(self):
        self.window.blit(self.menu, (self.pos[0], self.pos[1])) 

        self.draw_buttons()
        self.draw_text()


    def draw_text(self):
        for text in self.text:
            text.draw(self.window)
            

    def draw_buttons(self):
        for button in self.buttons:
            button.loop()

    
    def add_buttons(self, onclick, font:pygame.Font, pos:List[int], size:List[int], color:Tuple[int, int, int, int]=(111, 123, 128, 255), text:str="", text_color:tuple=(0, 0, 0)):
        self.buttons.append(Button(onclick, self.window, self.window_size, font, pos, size, color, (79, 88, 92, 255), text, text_color))

    def add_text(self, font:pygame.Font, pos:List[int], size:List[int], color:Tuple[int, int, int, int]=(111, 123, 128, 255), text:str=""):
        self.text.append(Text(font, text, color, pos))