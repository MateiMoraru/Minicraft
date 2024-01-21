import random
import pygame
from item import Item
from player import Player
from spritesheet import *
from rect import *
from window import Window

class Environment:
    def __init__(self, window: Window, spritesheet: Spritesheet, spritesheet_ui: Spritesheet, font: pygame.Font, font2: pygame.Font):
        self.window = window
        self.spritesheet = spritesheet 
        self.spritesheet_ui = spritesheet_ui
        self.font = font
        self.font2 = font2
        self.sprite_size = 64
        self.map = []
        self.generate_map()
        self.player = Player(window, spritesheet, spritesheet_ui, font, font2)
        self.selected_block = 0
        self.water_animation_timer = 0

        self.ground_items = []

    def generate_map(self):
        size = 120
        water_offset = 10

        patch_of_sand = None
        water = None
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
                    elif random.random() > 0.99:
                        block_type = "WATER_BLOCK_1"
                        block_id = WATER_BLOCK_1
                        water = [pos[0], pos[1], random.randint(2, 5)]
                    if (patch_of_sand is None or dist_point(pos, (patch_of_sand[0], patch_of_sand[1])) > patch_of_sand[2] * self.sprite_size) and (water is None or dist_point(pos, (water[0], water[1])) > water[2] * self.sprite_size):
                        if block_id is not None:
                            rect = Rect(pos, (self.sprite_size, self.sprite_size), (0, 0, 0), block_type, self.window.get(), self.spritesheet.image(block_id), texture_id=block_id)
                            self.map.append(rect)

                            if block_type == "GRASS_BLOCK" and random.random() > 0.95:
                                rect = Rect(pos, (self.sprite_size * 1, self.sprite_size * 1), (0, 0, 0), "TREE_1", self.window.get(), self.spritesheet.image(TREE_1), collidable=True, texture_id=TREE_1)
                                self.map.append(rect)
                            elif random.random() > 0.96:
                                rect = Rect(pos, (self.sprite_size * 1, self.sprite_size * 1), (0, 0, 0), "ROCK_1", self.window.get(), self.spritesheet.image(ROCK_1), collidable=True, texture_id=ROCK_1)
                                self.map.append(rect)
                    elif water is not None:
                        if dist_point(pos, (water[0], water[1])) < water[2] * self.sprite_size:
                            rect = Rect(pos, (self.sprite_size, self.sprite_size), (0, 0, 0), "WATER_BLOCK_1", self.window.get(), self.spritesheet.image(WATER_BLOCK_1), texture_id=WATER_BLOCK_1)
                            self.map.append(rect)
                        else:
                            rect = Rect(pos, (self.sprite_size, self.sprite_size), (0, 0, 0), "WATER_BLOCK_1", self.window.get(), self.spritesheet.image(WATER_BLOCK_1), texture_id=WATER_BLOCK_1)
                            self.map.append(rect)
                        if random.random() > 0.99:
                            patch_of_sand = None
                    else:
                        if dist_point(pos, (patch_of_sand[0], patch_of_sand[1])) < patch_of_sand[2] * self.sprite_size:
                            rect = Rect(pos, (self.sprite_size, self.sprite_size), (0, 0, 0), "SAND_BLOCK", self.window.get(), self.spritesheet.image(SAND_BLOCK), texture_id=SAND_BLOCK)
                            self.map.append(rect)
                        else:
                            rect = Rect(pos, (self.sprite_size, self.sprite_size), (0, 0, 0), "WATER_BLOCK_1", self.window.get(), self.spritesheet.image(WATER_BLOCK_1), texture_id=WATER_BLOCK_1)
                            self.map.append(rect)
                        if random.random() > 0.98:
                            patch_of_sand = None
                else:
                    block_type = "WATER_BLOCK_1"
                    block_id = WATER_BLOCK_1
                    rect = Rect(pos, (self.sprite_size, self.sprite_size), (0, 0, 0), block_type, self.window.get(), self.spritesheet.image(block_id), texture_id=block_id)
                    self.map.append(rect)

    def draw(self):
        offset = self.player.offset
        self.water_animation_timer += self.window.delta_time
        changed_water_tex = False
        
        self.player.set_in_water(False)

        for block in self.map:
            if self.in_boundaries(block, offset):
                block.draw(offset=offset)
                if block.collidable or block.texture_id in BLOCK_COLLIDABLE:
                    self.player.check_collision(block)

                mouse_pos = pygame.mouse.get_pos()
                #mouse_pos = [mouse_pos[0] - offset[0], mouse_pos[1] - offset[1]]
                if dist_point(self.player.player.center, mouse_pos) <= 3 * self.sprite_size and block.collide_point(mouse_pos, offset=offset):
                    self.selected_block = block
                    self.player.selected_block = block
                    rect(self.window.get(), (block.pos[0] + offset[0], block.pos[1] + offset[1]), block.size, (0, 0, 0, 50))

                if block.type == "WATER_BLOCK_1" or block.type == "WATER_BLOCK_2":
                    if block.collide_rect(self.player.collider_middle.rect, offset=offset):
                        self.player.set_in_water()
                if block.type == "WATER_BLOCK_1" and self.water_animation_timer > 1000:
                    block.type = "WATER_BLOCK_2"
                    block.set_texture(self.spritesheet.image(WATER_BLOCK_2))
                    changed_water_tex = True
                elif block.type == "WATER_BLOCK_2" and self.water_animation_timer > 1000:
                    block.type = "WATER_BLOCK_1"
                    changed_water_tex = True
                    block.set_texture(self.spritesheet.image(WATER_BLOCK_1))
        
        for item in self.ground_items:
            item.draw(offset)
            item.loop()
            if dist_point(self.player.player.center, (item.pos[0] + offset[0], item.pos[1] + offset[1])) < self.sprite_size:
                self.ground_items.remove(item)
                self.player.inventory.add_item(item.type)

        if changed_water_tex:
            self.water_animation_timer = 0

        self.player.draw()

    
    def in_boundaries(self, block: Rect, offset: Tuple[int, int]):
        return block.pos[0] > -offset[0] - block.size[0] and block.pos[0] < self.window.size[0] - offset[0] + block.size[0] and block.pos[1] > -offset[1] - block.size[0] and block.pos[1] < self.window.size[1] - offset[1]
    
    
    def loop(self):
        dt = self.window.delta_time

        self.player.loop(dt)

        for block in self.player.blocks_to_remove:
            if block in self.map:
                if len(block.type) <= 1:
                    result = BLOCK_DROPS[block.texture_id]
                else:
                    result = BLOCK_DROPS[block.type]
                self.ground_items.append(Item(self.window, self.spritesheet, (block.pos[0] + self.sprite_size / 6, block.pos[1] + self.sprite_size / 6), result, (self.sprite_size / 1.5, self.sprite_size / 1.5)))
                self.map.remove(block)
        for block in self.player.blocks_to_add:
            self.map.append(Rect(self.selected_block.pos, self.selected_block.size, (0, 0, 0), "", self.window.get(), self.spritesheet.image(block[0], size=(self.sprite_size, self.sprite_size)), texture_id=block[0]))
            self.player.blocks_to_add.remove(block)