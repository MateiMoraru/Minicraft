import random
import pygame
from window import Window
from rect import *
from spritesheet import Spritesheet


class Particles:
    def __init__(self, window: Window, spritesheet: Spritesheet, pos: Tuple[int, int], size: int=10, acceletaion: int=0.2, multiplier: int=1, underground: bool=False):
        self.window = window
        self.spritesheet = spritesheet
        self.pos = pos
        self.size = size
        self.acceletaion = acceletaion
        self.multiplier = multiplier
        self.underground = underground
        self.particles_amount = 10
        self.particles = []
        self.gravity = True

    
    def add_particles(self, pos: Tuple[int, int]=None, texture: int=None, color: Tuple[int, int, int]=(0, 0, 0), multiplier: int=None):
        if multiplier is None:
            multiplier = self.multiplier
        if pos is None:
            pos = self.pos
        particles_amount = int(self.particles_amount * self.multiplier)

        for i in range(particles_amount):
            particle = self.new_particle((pos[0] + random.uniform(-5, 5) * self.size, pos[1] + random.uniform(-5, 5) * self.size), texture, color)
            self.particles.append(particle)


    def new_particle(self, pos: Tuple[int, int], texture: int=None, color: Tuple[int, int, int]=(0, 0, 0)):
        tex = self.spritesheet.image(texture, size=(self.size * 5, self.size * 5))
        tex_size = tex.get_size()
        x = tex_size[0] / self.size - 1
        y = tex_size[1] / self.size - 1
        rect_subsurface = [random.uniform(1, x) * self.size, random.uniform(1, y) * self.size, self.size, self.size]
        cutout = tex.subsurface(rect_subsurface)
        particle = Rect(pos, (self.size, self.size), (color[0], color[1], color[2], random.randint(0, 100)), "PARTCILE", self.window.get(), cutout)
        particle.add_force([random.uniform(-1, 1), 0])
        return particle
    

    def draw(self, offset: Tuple[int, int]=(0, 0), underground: bool=False):
        if underground == self.underground:
            for particle in self.particles:
                particle.draw(offset)
                rect(self.window.get(), (particle.pos[0] + offset[0], particle.pos[1] + offset[1]), particle.size, particle.color)

    
    def loop(self, die_chance: float=0.95):
        for particle in self.particles:
            if not self.gravity:
                particle.add_force([0, self.acceletaion])

            if random.random() > die_chance:
                self.particles.remove(particle)

    
    def set_pos(self, pos: Tuple[int, int]):
        self.pos = pos


    def no_gravity(self):
        self.gravity = False