import random
import pygame
from campfire import Campfire
from item import Item
from player import Player
from spritesheet import *
from rect import *
from window import Window
from particles import Particles
from sfx_manager import *
from light import LightSource
from zombie import Zombie

class Environment:
    def __init__(self, window: Window, spritesheet: Spritesheet, spritesheet_ui: Spritesheet, font: pygame.Font, font2: pygame.Font, sfx: SFX):
        self.window = window
        self.spritesheet = spritesheet 
        self.spritesheet_ui = spritesheet_ui
        self.font = font
        self.font2 = font2
        self.sprite_size = 64
        self.map = []
        self.generate_map()
        self.player = Player(window, spritesheet, spritesheet_ui, font, font2, sfx)
        self.selected_block = 0
        self.water_animation_timer = 0
        self.sfx = sfx

        self.ground_items = []
        self.special_blocks = []
        self.light_sources = []
        self.particles = Particles(self.window, self.spritesheet, (0, 0), 5)

        self.time = 2000
        self.time_direction = 1
        self.time_acceleration = .1
        self.light_filter = pygame.surface.Surface(self.window.size)
        self.light_filter.fill((100, 100, 100))

        self.entities = []
        self.entities.append(Zombie(self.window, self.spritesheet, self.player.player.pos, self.sprite_size))

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
                            self.add_rect(pos, block_id)
                            if block_type == "GRASS_BLOCK" and random.random() > 0.95:
                                self.add_rect(pos, TREE_1)
                            elif (block_type == "SAND_BLOCK" or block_type == "GRASS_BLOCK") and random.random() > 0.96:
                                self.add_rect(pos, ROCK_1)
                            elif block_type == "GRASS_BLOCK" and random.random() > 0.995:
                                self.add_rect(pos, ROCK_IRON)
                            elif block_type == "GRASS_BLOCK":
                                if random.random() > 0.98:
                                    self.add_rect(pos, FLOWER_1)
                                elif random.random() > 0.95:
                                    self.add_rect(pos, GRASS_1)
                                elif random.random() > 0.95:
                                    self.add_rect(pos, GRASS_2)
                                elif random.random() > 0.95:
                                    self.add_rect(pos, BUSH)
                    elif water is not None:
                        if dist_point(pos, (water[0], water[1])) < water[2] * self.sprite_size:
                            self.add_rect(pos, WATER_BLOCK_1)
                        else:
                            self.add_rect(pos, WATER_BLOCK_1)
                        if random.random() > 0.99:
                            patch_of_sand = None
                    else:
                        if dist_point(pos, (patch_of_sand[0], patch_of_sand[1])) < patch_of_sand[2] * self.sprite_size:
                            self.add_rect(pos, SAND_BLOCK)
                        else:
                            self.add_rect(pos, WATER_BLOCK_1)
                        if random.random() > 0.98:
                            patch_of_sand = None
                else:
                    block_type = "WATER_BLOCK_1"
                    block_id = WATER_BLOCK_1
                    self.add_rect(pos, block_id)

    def add_rect(self, pos: Tuple[int, int], texture_id: int, coll: bool=False):
        size = (self.sprite_size, self.sprite_size)
        color = (0, 0, 0)
        block_type = ID_STR(texture_id)
        window = self.window.get()
        tex = self.spritesheet.image(texture_id)
        rect = Rect(pos, size, color, block_type, window, tex, collidable=coll, texture_id=texture_id)
        self.map.append(rect)


    def draw(self):
        offset = self.player.offset
        self.water_animation_timer += self.window.delta_time
        changed_water_tex = False
        
        self.player.set_in_water(False)

        for block in self.map:
            if self.in_boundaries(block, offset):
                block.draw(offset=offset)
                for light_source in self.light_sources:
                    if light_source.in_range(block):
                        light_source.draw(block, offset)
                if self.player.produce_light:
                    if self.player.light.in_range(block):
                        self.player.light.draw(block, offset)
                if block.texture_id == GRASS_BLOCK_DUG:
                    if random.random() > 0.999:
                        block.set_texture(self.spritesheet.image(GRASS_BLOCK))
                
                if block.collidable or block.texture_id in BLOCK_COLLIDABLE:
                    self.player.check_collision(block)
                    for entity in self.entities:
                        entity.check_collision(block, offset=offset)
                if block.texture_id == DOOR_CLOSED:
                    if block.collide_rect(self.player.player.rect, offset=offset):
                        block.set_texture(self.spritesheet.image(DOOR_OPENED))
                        block.texture_id = DOOR_OPENED
                if block.texture_id == DOOR_OPENED:
                    if not block.collide_rect(self.player.player.rect, offset=offset):
                        block.set_texture(self.spritesheet.image(DOOR_CLOSED))
                        block.texture_id = DOOR_CLOSED
                if block.collide_rect(self.player.colliders[1].rect, offset=offset):
                    self.player_floor_block = block
                

                mouse_pos = pygame.mouse.get_pos()
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
        
        self.window.get().blit(self.light_filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        
        for block in self.special_blocks:
            block.draw(offset)
            if isinstance(block, Campfire):
                if block.campfire.collide_rect(self.player.player.rect, offset=offset):
                    if random.random() > 0.99:
                        self.player.harm(1, "FIRE")
                if block.campfire.collide_point(pygame.mouse.get_pos(), offset=offset):
                    self.selected_block = block
                
                for cooked in block.cooked:
                    self.ground_items.append(Item(self.window, self.spritesheet, (block.campfire.center[0] + random.uniform(-1.5, 1.5) * self.sprite_size, block.campfire.center[1] + random.uniform(-1.5, 1.5) * self.sprite_size), BRICK))
                    block.cooked.remove(cooked)

        for item in self.ground_items:
            item.draw(offset)
            item.loop()
            if dist_point(self.player.player.center, (item.pos[0] + offset[0], item.pos[1] + offset[1])) < self.sprite_size:
                self.ground_items.remove(item)
                self.player.inventory.add_item([item.type, 1])
                self.sfx.play(ITEM_PICKUP)

        for entity in self.entities:
            entity.draw(offset=offset)
            entity.loop(self.player, offset=offset)

        if changed_water_tex:
            self.water_animation_timer = 0

        self.particles.draw()
        self.player.draw()

    
    def in_boundaries(self, block: Rect, offset: Tuple[int, int]):
        return block.pos[0] > -offset[0] - block.size[0] and block.pos[0] < self.window.size[0] - offset[0] + block.size[0] and block.pos[1] > -offset[1] - block.size[0] and block.pos[1] < self.window.size[1] - offset[1]
    
    
    def update_time_of_day(self):
        self.time += self.window.delta_time * self.time_direction * self.time_acceleration
        
        if self.time >= 15000:
            self.time_direction *= -1
        elif self.time <= 1000:
            self.time_direction *= -1

        self.light_filter.fill((self.time / 100, self.time / 100, self.time / 100))


    def loop(self):
        dt = self.window.delta_time

        self.update_time_of_day()

        self.particles.loop(0.8)
        self.player.loop(dt, self.player_floor_block)

        for block in self.player.blocks_to_remove:
            if block in self.map:
                if len(block.type) <= 1:
                    results = BLOCK_DROPS[ID_STR(block.texture_id)]
                else:
                    results = BLOCK_DROPS[block.type]
                for result in results:
                    amount = 1
                    if len(result) == 3:
                        amount = random.randint(result[1], result[2])
                    for item in range(0, amount):
                        self.ground_items.append(Item(self.window, self.spritesheet, (block.pos[0] + self.sprite_size / 6 + random.randint(-50, 50), block.pos[1] + self.sprite_size / 6 + random.randint(-50, 50)), result[0], (self.sprite_size / 1.5, self.sprite_size / 1.5)))
                self.particles.add_particles((block.center[0] + block.size[0] / 2+ self.player.offset[0], block.center[1] + self.player.offset[1]), block.texture_id)
                self.sfx.play(HIT_BLOCK)
                self.map.remove(block)
                self.player.blocks_to_remove.remove(block)
        for block in self.player.blocks_to_add:
            if isinstance(self.selected_block, Campfire):
                if block[0] != CLAY:
                    self.player.inventory.add_item((block[0], 1))
                    self.player.blocks_to_add.remove(block)
                    return
                self.selected_block.add_to_fire(self.player.inventory.item[0])
                self.player.blocks_to_add.remove(block)
                return
            if not block[0] in SPECIAL_BLOCKS and block[0] in BLOCK_PLACABLE:
                self.map.append(Rect(self.selected_block.pos, self.selected_block.size, (0, 0, 0), "", self.window.get(), self.spritesheet.image(block[0], size=(self.sprite_size, self.sprite_size)), texture_id=block[0]))
            elif block[0] in LIGHT_BLOCKS:
                self.light_sources.append(LightSource(self.window, self.selected_block.center, 3, color=(255, 226, 110)))
                if block[0] == CAMPFIRE_1:
                    self.special_blocks.append(Campfire(self.window, self.spritesheet, self.selected_block.pos, self.selected_block.size))
                elif block[0] == TORCH:
                    self.special_blocks.append(Rect(self.selected_block.pos, self.selected_block.size, (0, 0, 0), "TORCH", self.window.get(), self.spritesheet.image(TORCH, size=(self.sprite_size, self.sprite_size))))
            self.particles.add_particles((self.selected_block.center[0] + self.selected_block.size[0] / 2 + self.player.offset[0], self.selected_block.center[1] + self.player.offset[1]), block[0])
            self.sfx.play(PLACE_BLOCK)
            self.player.blocks_to_add.remove(block)