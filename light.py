from typing import Tuple
import pygame
from window import Window
from rect import *
class LightSource:
    def __init__(self, window: Window, pos: Tuple[int, int], range: int, color: Tuple[int, int, int]=(255, 255, 255), max_intensity: int=200):
        self.window = window
        self.pos = pos
        self.intensity = max_intensity / range
        self.range = range
        self.color = color

    
    def in_range(self, block: Rect):
        dist = dist_block(self.pos, block)

        return dist < self.range * block.size[0]
    

    def draw(self, block: Rect, offset: Tuple[int, int]=(0, 0)):
        dist = dist_block(self.pos, block) / block.size[0]

        intensity = self.intensity * self.range - self.intensity * dist
        if intensity < 50:
            intensity = 50
        rect(self.window.get(), (block.pos[0] + offset[0], block.pos[1] + offset[1]), block.size, (self.color[0], self.color[1], self.color[2], intensity - 50))


    def set_pos(self, pos: Tuple[int, int]):
        self.pos = pos
