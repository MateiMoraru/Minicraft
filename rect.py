import math
from typing import *
import pygame

class Rect:
    def __init__(self, pos:Tuple[float], size:Tuple[float], color:Tuple[int], type:str, window:pygame.Surface, texture:pygame.Surface=None, collidable:bool=False, texture_id:int=None):
        self.pos = pos
        self.size = size
        self.type = type
        self.color = color
        self.window = window
        self.texture = texture
        self.texture_id = texture_id
        self.velocity = [0, 0]
        if texture is not None:
            self.texture = pygame.transform.scale(self.texture, self.size)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.center = (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2)
        self.light = 0
        self.collidable = collidable

    def draw(self, offset: Tuple[int, int]=(0, 0)):
        self.center = (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2)
        pos = [self.pos[0] + offset[0], self.pos[1] + offset[1]]

        if self.texture == None:
            if self.type != "air":
                pygame.draw.rect(self.window, self.color, self.rect)
        else:
            self.window.blit(self.texture, pos)
        if self.light > 0:
            rect(self.window, pos, self.size, (255, 255, 255, self.light))
        elif self.light < 0:
            rect(self.window, pos, self.size, (0, 0, 0, -self.light))

        self.pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]


    def collide_point(self, point, offset:tuple=(0, 0)):
        pos = [self.pos[0] + offset[0], self.pos[1] + offset[1]]
        collide_x = point[0] > pos[0] and point[0] < pos[0] + self.size[0]
        collide_y = point[1] > pos[1] and point[1] < pos[1] + self.size[1]

        return collide_x and collide_y
    
    
    def collide_rect(self, rect:pygame.Rect, offset:tuple=(0, 0)):
        block = pygame.Rect(self.pos[0] + offset[0], self.pos[1] + offset[1], self.size[0], self.size[1])

        return rect.colliderect(block)
    

    def set_type(self, type:str):
        self.type = type

    
    def set_texture(self, tex:pygame.Surface, scale=True):
        if scale:
            self.texture = pygame.transform.scale(tex, self.size)
        else:
            self.texture = tex

    
    def set_size(self, size:Tuple[float]):
        self.size = size

    
    def set_pos(self, pos:Tuple[float]):
        self.pos = pos


    def add_light(self, light:int):# If light's value is greater than 255, 
        self.light += light
        if self.light > 255:
            self.light = 255
        elif self.light < -255:
            self.light = -255

    def set_light(self, light:int):
        self.light = light
        if self.light > 255:
            self.light = 255
        elif self.light < -255:
            self.light = -255


    def rm_texture(self):
        self.texture = None
        self.type = "air"


    def add_force(self, velo: Tuple[int, int]):
        self.velocity[0] += velo[0]
        self.velocity[1] += velo[1]


    def move(self, x: float, y: float):
        self.pos = [self.pos[0] + x, self.pos[1] + y]


def rect(window: pygame.Surface, pos: tuple, size: tuple, color: tuple):
    surf = pygame.Surface(size)
    surf.set_alpha(color[3])
    surf.fill(color)
    window.blit(surf, pos)


def collide_point(rect:List[int], point:List[int]):
    collide_x = point[0] > rect[0] and point[0] < rect[0] + rect[2]
    collide_y = point[1] > rect[1] and point[1] < rect[1] + rect[3]
    return collide_x and collide_y


def dist_block(point:tuple, rect:Rect, offset: Tuple[int, int]=(0, 0)):
    dx = abs(point[0] - (rect.rect.x + rect.rect.w / 2 + offset[0])) ** 2
    dy = abs(point[1] - (rect.rect.y + rect.rect.h / 2 + offset[1])) ** 2

    return math.sqrt(dx + dy) 
    
    
def dist_point(point:tuple, point2:tuple):
    dx = abs(point[0] - point2[0]) ** 2
    dy = abs(point[1] - point2[1]) ** 2

    return math.sqrt(dx + dy) 