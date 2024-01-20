import pygame
from window import Window
from spritesheet import *
from rect import *
from typing import Tuple

class Item:
    def __init__(self, window: Window, spritesheet: Spritesheet, pos: Tuple[int, int], item: int, size: Tuple[int, int]=(32, 32)):
        self.window = window
        self.pos = [pos[0], pos[1]]
        self.texture = spritesheet.image(item, size=size)
        self.type = item
        self.offset = 0
        self.acc = 0.1
    
    def draw(self, offset=(0, 0)):
        self.window.get().blit(self.texture, (self.pos[0] + offset[0], self.pos[1] + offset[1]))

    def loop(self):
        self.offset += self.acc
        self.pos[1] += self.acc

        if self.offset > 10:
            self.acc *= -1
        elif self.offset < -10:
            self.acc *= -1