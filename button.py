from typing import Tuple, List
import pygame
from rect import rect
from text import Text

class Button:
    def __init__(self, onclick, window:pygame.Surface, window_size:Tuple[int, int], font:pygame.Font, pos:List[int], size:List[int], color:Tuple[int, int, int, int]=(111, 123, 128, 255), color_hover:Tuple[int, int, int, int]=(79, 88, 92, 255), text:str="", text_color:tuple=(0, 0, 0)):
        self.onclick = onclick
        self.window = window
        self.window_size = window_size
        self.pos = pos
        self.size = size
        self.default_color = color
        self.color = color
        self.color_hover = color_hover
        self.text = text
        self.text_color = text_color
        self.font = font

        self.pos = [self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2]
        
        text_width, text_height = self.font.size(self.text)
        self.text_pos = (self.pos[0] + self.size[0] / 2 -text_width / 2, self.pos[1] + self.size[1] / 2 - text_height / 2)


    def loop(self):
        rect(self.window, self.pos, self.size, self.color)
        Text(self.font, self.text, self.text_color, self.text_pos).draw(self.window)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.collide(mouse_pos):
            self.color = self.color_hover
            if mouse_pressed[0]:
                self.onclick()
        else:
            self.color = self.default_color


    def collide(self, mouse_pos:tuple):
        x = mouse_pos[0] > self.pos[0] and mouse_pos[0] < self.pos[0] + self.size[0]
        y = mouse_pos[1] > self.pos[1] and mouse_pos[1] < self.pos[1] + self.size[1]

        return x and y