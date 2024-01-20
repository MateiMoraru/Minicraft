import random
import pygame
from player import Player
from spritesheet import *
from rect import *
from window import Window

class Environment:
    def __init__(self, window: Window, spritesheet: Spritesheet):
        self.window = window
        self.spritesheet = spritesheet 
        self.sprite_size = 64
        self.map = []
        self.generate_map()
        self.player = Player(window, spritesheet)
        self.water_animation_timer = 0

    def generate_map(self):
        size = 40
        water_offset = 30

        patch_of_sand = None
        for y in range(-water_offset, size + water_offset):
            for x in range(-water_offset, size + water_offset):
                pos = [x * self.sprite_size, y * self.sprite_size]
                if x >= 0 and y > 0 and x <= size - 2 and y <= size - 2:
                    block_type = "GRASS_BLOCK"
                    block_id = GRASS_BLOCK
                    if x <= 1 or y <= 1 or x >= size - 3 or y >= size - 3:
                        block_type = "SAND_BLOCK"
                        block_id = SAND_BLOCK
                        if random.random() > 0.8 and x == 0 or y == 0 or x == size - 1 or y == size - 1:
                            block_type = "WATER_BLOCK_1"
                            block_id = WATER_BLOCK_1
                    if random.random() > 0.99:
                        block_type = "SAND_BLOCK"
                        block_id = SAND_BLOCK
                        patch_of_sand = [pos[0], pos[1], random.randint(2, 5)]
                    if patch_of_sand is None or dist_point(pos, (patch_of_sand[0], patch_of_sand[1])) > patch_of_sand[2] * self.sprite_size:
                        if block_id is not None:
                            rect = Rect(pos, (self.sprite_size, self.sprite_size), (0, 0, 0), block_type, self.window.get(), self.spritesheet.image(block_id))
                            self.map.append(rect)

                            if block_type == "GRASS_BLOCK" and random.random() > 0.95:
                                rect = Rect(pos, (self.sprite_size * 1, self.sprite_size * 1), (0, 0, 0), "TREE_1", self.window.get(), self.spritesheet.image(TREE_1), collidable=True)
                                self.map.append(rect)
                            elif random.random() > 0.96:
                                rect = Rect(pos, (self.sprite_size * 1, self.sprite_size * 1), (0, 0, 0), "ROCK_1", self.window.get(), self.spritesheet.image(ROCK_1), collidable=True)
                                self.map.append(rect)
                    else:
                        if dist_point(pos, (patch_of_sand[0], patch_of_sand[1])) < patch_of_sand[2] * self.sprite_size:
                            rect = Rect(pos, (self.sprite_size, self.sprite_size), (0, 0, 0), "SAND_BLOCK", self.window.get(), self.spritesheet.image(SAND_BLOCK))
                            self.map.append(rect)
                        else:
                            rect = Rect(pos, (self.sprite_size, self.sprite_size), (0, 0, 0), "WATER_BLOCK_1", self.window.get(), self.spritesheet.image(WATER_BLOCK_1))
                            self.map.append(rect)
                        if random.random() > 0.98:
                            patch_of_sand = None
                else:
                    block_type = "WATER_BLOCK_1"
                    block_id = WATER_BLOCK_1
                    rect = Rect(pos, (self.sprite_size, self.sprite_size), (0, 0, 0), block_type, self.window.get(), self.spritesheet.image(block_id))
                    self.map.append(rect)

    def draw(self):
        offset = self.player.offset
        self.water_animation_timer += self.window.delta_time
        changed_water_tex = False

        for block in self.map:
            if self.in_boundaries(block, offset):
                block.draw(offset=offset)
                if block.collidable:
                    self.player.check_collision(block)
                if block.type == "WATER_BLOCK_1" and self.water_animation_timer > 1000:
                    block.type = "WATER_BLOCK_2"
                    block.set_texture(self.spritesheet.image(WATER_BLOCK_2))
                    changed_water_tex = True
                elif block.type == "WATER_BLOCK_2" and self.water_animation_timer > 1000:
                    block.type = "WATER_BLOCK_1"
                    changed_water_tex = True
                    block.set_texture(self.spritesheet.image(WATER_BLOCK_1))
        
        if changed_water_tex:
            self.water_animation_timer = 0

        self.player.draw()

    
    def in_boundaries(self, block: Rect, offset: Tuple[int, int]):
        return block.pos[0] > -offset[0] - block.size[0] and block.pos[0] < self.window.size[0] - offset[0] + block.size[0] and block.pos[1] > -offset[1] - block.size[0] and block.pos[1] < self.window.size[1] - offset[1]
    
    
    def loop(self):
        dt = self.window.delta_time

        self.player.loop(dt)