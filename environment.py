import random
import pygame
from campfire import Campfire
from chest import Chest
from enemy import Enemy
from item import Item
from player import Player
from spritesheet import *
from rect import *
from window import Window
from particles import Particles
from sfx_manager import *
from light import LightSource
from zombie import Zombie
from text import *

class Environment:
    def __init__(self, window: Window, spritesheet: Spritesheet, spritesheet_ui: Spritesheet, font: pygame.font, font2: pygame.font, sfx: SFX):
        self.window = window
        self.spritesheet = spritesheet 
        self.spritesheet_ui = spritesheet_ui
        self.font = font
        self.font2 = font2
        self.sprite_size = 64
        self.map = []
        self.underground = []
        self.special_blocks = [[], []]
        print("\tGenerating map...")
        self.cave_level = 0
        self.generate_map()
        print("\tGenerating cave system...")
        self.generate_underground()
        self.player = Player(window, spritesheet, spritesheet_ui, font, font2, sfx)
        self.selected_block = 0
        self.selected_entity = 0
        self.water_animation_timer = 0
        self.sfx = sfx

        self.ground_items = [[], []]
        self.light_sources = [[], []]
        self.particles = [Particles(self.window, self.spritesheet, (0, 0), 5), Particles(self.window, self.spritesheet, (0, 0), 5)]

        self.time = 2000
        self.time_direction = 1
        self.time_acceleration = .1
        self.light_filter = pygame.surface.Surface(self.window.size)
        self.light_filter.fill((100, 100, 100))
        self.underground_light_filter = pygame.surface.Surface(self.window.size)
        self.underground_light_filter.fill((20, 20, 20))

        self.entities = [[], []]

        self.floating_texts = [[], []]


    
    def generate_underground(self):
        self.underground = self.generate_cave(size=(10, 10), has_stairs=True)

    def generate_cave(self, size: Tuple[int, int] = (10, 10), has_stairs: bool=False):
        cave = []
        placed_stair = False
        x_range = [int(-size[1] / 2), random.randint(5, 13)]

        for i in range(int(-size[0] / 2), int(size[0] / 2)):
            y = i
            
            for j in range(x_range[0], x_range[0] + x_range[1]):
                x = j
                    
                pos = [(x + 10) * self.sprite_size, (y + 6) * self.sprite_size]
                
                block_type = CAVE_DIRT
                collide = False
                if x == x_range[0] or y == int(-size[1] / 2) or x >= x_range[0] + x_range[1] - 2 or y >= int(size[1] / 2) - 2:
                    block_type = CAVE_STONE_2
                    collide = True
                cave.append(self.add_rect(pos, block_type, collide, False))
                if random.random() > 0.55 and has_stairs and not collide == True and not placed_stair:
                    block_type = STAIRSET
                    cave.append(self.add_rect(pos, block_type, False, False))
                    placed_stair = True
            if i < 0:
                x_range[1] += random.randint(0, 1)
                x_range[0] += random.randint(0, 1)
            else:
                x_range[1] += random.randint(-1, 0)
                x_range[0] += random.randint(-1, 0)
                if x_range[1] < 0:
                    x_range[1] = 1
        return cave


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
                                elif random.random() > 0.999:
                                    self.add_rect(pos, STAIRSET)
                                elif random.random() > 0.99:
                                    self.special_blocks[0].append(Chest(self.window, self.spritesheet, pos, (self.sprite_size, self.sprite_size)))
                                    
                                    chest_rarity = 0
                                    if random.random() > 0.9:
                                        chest_rarity = 2
                                    elif random.random() > 0.6:
                                        chest_rarity = 1

                                    self.special_blocks[0][-1].set_random(chest_rarity)
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


    def add_rect(self, pos: Tuple[int, int], texture_id: int, coll: bool=False, add_to_map: bool=True):
        size = (self.sprite_size, self.sprite_size)
        color = (0, 0, 0)
        block_type = ID_STR(texture_id)
        window = self.window.get()
        tex = self.spritesheet.image(texture_id)
        rect = Rect(pos, size, color, block_type, window, tex, collidable=coll, texture_id=texture_id)

        if not add_to_map:
            return rect
        else:
            self.map.append(rect)


    def draw(self, debugging=False):
        offset = self.player.offset
        if self.cave_level == 1:
            offset = self.player.underground_offset
        self.water_animation_timer += self.window.delta_time
        self.selected_entity = None
        self.player.selected_entity = None
        
        self.player.set_in_water(False)

        if self.cave_level == 0:
            self.draw_map(offset)
            self.window.get().blit(self.light_filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

            for item in self.ground_items[self.cave_level]:
                item.draw(offset)
                item.loop()
                if dist_point(self.player.player.center, (item.pos[0] + offset[0], item.pos[1] + offset[1])) < self.sprite_size:
                    self.ground_items[self.cave_level].remove(item)
                    self.player.inventory.add_item([item.type, 1])
                    self.sfx.play(ITEM_PICKUP, debugging=debugging)

            for entity in self.entities[self.cave_level]:
                entity.draw(offset=offset)
                entity.loop(self.player, offset=offset)
                if entity.health <= 0:
                    if entity.special_item is not None:
                        self.ground_items[self.cave_level].append(Item(self.window, self.spritesheet, entity.enemy.pos, entity.special_item))
                    self.entities[self.cave_level].remove(entity)
                    self.selected_entity = None
                    self.player.selected_entity = None
                    self.player.add_xp(2)
                    self.floating_texts.append(FloatingText(self.font, "+2", (198, 169, 212), (self.player.player.center[0], self.player.player.pos[1] - 10), (0, 0.2)))

                if isinstance(entity, Enemy):
                    if entity.enemy.collide_point(pygame.mouse.get_pos(), offset=offset):
                        self.selected_entity = entity
                        self.player.selected_entity = self.selected_entity
                        rect(self.window.get(), (entity.enemy.pos[0] + offset[0], entity.enemy.pos[1] + offset[1]), entity.enemy.size, (0, 0, 0, 50))

            self.particles[self.cave_level].draw()
        else:
            self.draw_underground(offset=offset)

        for block in self.special_blocks[self.cave_level]:
                if block.__type__ == "CHEST":
                    if block.opened:
                        d = dist_block(self.player.player.center, block.rect, offset)
                        if d > 4 * self.sprite_size:
                            block.opened = False
                    block.draw(offset, self.player.inventory)
                    if block.rect.collide_point(pygame.mouse.get_pos(), offset=offset):
                        self.selected_block = block
                        self.player.selected_block = block
                elif block.__type__ == "CAMPFIRE":
                    block.draw(offset, underground=self.cave_level==1)
                    if block.campfire.collide_rect(self.player.player.rect, offset=offset):
                        if random.random() > 0.99:
                            self.player.harm(1, "FIRE")
                    if block.campfire.collide_point(pygame.mouse.get_pos(), offset=offset):
                        self.selected_block = block
                        self.player.selected_block = block
                    
                    for cooked in block.cooked:
                        if cooked[0] == -1:
                            block.cooked.remove(cooked)
                            break
                        result = COOK_RESULT[ID_STR(cooked[0])]
                        self.ground_items[self.cave_level].append(Item(self.window, self.spritesheet, (block.campfire.center[0] + random.uniform(-1.5, 1.5) * self.sprite_size, block.campfire.center[1] + random.uniform(-1.5, 1.5) * self.sprite_size), result))
                        block.cooked.remove(cooked)
                else:
                    block.draw(offset, underground=self.cave_level==1)
        self.player.draw()
        for text in self.floating_texts[self.cave_level]:
            text.draw(self.window.get())
            text.loop()
            if time.time() - text.time > text.fadeout:
                self.floating_texts[self.cave_level].remove(text)


    def draw_underground(self, offset: Tuple[int, int]=(0, 0)):
        for block in self.underground:
            if self.in_boundaries(block, offset=offset):
                block.draw(offset)
                for light_source in self.light_sources[1]:
                    if light_source.in_range(block):
                        light_source.draw(block, offset)
                if self.player.produce_light:
                    if self.player.light.in_range(block):
                        self.player.light.draw(block, offset)
                mouse_pos = pygame.mouse.get_pos()
                if dist_point(self.player.player.center, mouse_pos) <= 3 * self.sprite_size and block.collide_point(mouse_pos, offset=offset):
                    self.selected_block = block
                    self.player.selected_block = block
                    rect(self.window.get(), (block.pos[0] + offset[0], block.pos[1] + offset[1]), block.size, (0, 0, 0, 50))
                if block.collidable or block.texture_id in BLOCK_COLLIDABLE:
                    self.player.check_collision(block)
                if block.texture_id == STAIRSET:
                    if block.collide_rect(self.player.player.rect, offset=offset) and time.time() - self.player.last_cave_level_change > 0.1:
                        self.player.last_cave_level_change = time.time()
                        self.cave_level = 0
                        self.player.underground = False
                if block.collide_rect(self.player.colliders[1].rect, offset=offset):
                    self.player_floor_block = block
        
        self.window.get().blit(self.underground_light_filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    
    def draw_map(self, offset):
        changed_water_tex = False
        light_blocks = []

        for block in self.map:
            if self.in_boundaries(block, offset):
                block.draw(offset=offset)
                
                if block.texture_id in LIGHT_AFFECTED_BLOCKS:
                    for light_source in self.light_sources[0]:
                        if light_source.in_range(block):
                            light_source.draw(block, offset)

                    if self.player.produce_light:
                        if self.player.light.in_range(block) and block.pos not in light_blocks:
                            self.player.light.draw(block, offset)
                
                if block.texture_id == GRASS_BLOCK_DUG:
                    if random.random() > 0.999:
                        block.set_texture(self.spritesheet.image(GRASS_BLOCK))
                
                if block.texture_id == BUSH:
                    if random.random() > 0.999:
                        self.ground_items[self.cave_level].append(Item(self.window, self.spritesheet, (block.pos[0] + random.uniform(-1, 1) * block.size[0], block.pos[1] + random.uniform(-1, 1 * block.size[1])), FRUIT[random.randint(0, len(FRUIT) - 1)]))
                
                if block.collidable or block.texture_id in BLOCK_COLLIDABLE or block.texture_id in ENEMY_COLLIDABLE:
                    if not block.texture_id in ENEMY_COLLIDABLE and block.texture_id in BLOCK_COLLIDABLE:
                        self.player.check_collision(block)
                    elif block.texture_id in ENEMY_COLLIDABLE + BLOCK_COLLIDABLE:
                        for entity in self.entities[self.cave_level]:
                            entity.check_collision(block, offset=offset)
                
                if block.texture_id == DOOR_CLOSED:
                    if block.collide_rect(self.player.player.rect, offset=offset):
                        block.set_texture(self.spritesheet.image(DOOR_OPENED))
                        block.texture_id = DOOR_OPENED
                
                if block.texture_id == DOOR_OPENED:
                    if not block.collide_rect(self.player.player.rect, offset=offset):
                        block.set_texture(self.spritesheet.image(DOOR_CLOSED))
                        block.texture_id = DOOR_CLOSED
                
                if block.texture_id == STAIRSET:
                    if block.collide_rect(self.player.player.rect, offset=offset) and time.time() - self.player.last_cave_level_change > 0.1:
                        self.player.last_cave_level_change = time.time()
                        self.cave_level = 1
                        self.player.underground = True
                
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
        
        if changed_water_tex:
            self.water_animation_timer = 0
        

    def in_boundaries(self, block: Rect, offset: Tuple[int, int]):
        return block.pos[0] > -offset[0] - block.size[0] and block.pos[0] < self.window.size[0] - offset[0] + block.size[0] and block.pos[1] > -offset[1] - block.size[0] and block.pos[1] < self.window.size[1] - offset[1]
    
    
    def update_time_of_day(self):
        self.time += self.window.delta_time * self.time_direction * self.time_acceleration
        
        if self.time >= 15000:
            self.time_direction *= -1
        elif self.time <= 1000:
            self.time_direction *= -1

        self.light_filter.fill((self.time / 100, self.time / 100, self.time / 100))


    def loop(self, debugging=False):
        dt = self.window.delta_time

        self.update_time_of_day()

        self.particles[self.cave_level].loop(0.8)
        self.player.loop(dt, self.player_floor_block, debugging=debugging)

        if random.random() > .999 and self.time > 4000:
            pos = self.window.random_in_boundaries()
            if debugging:
                print(f"INFO: Spawned zombie at {pos} + {self.player.offset} = ({pos[0] + self.player.offset[0]}, {pos[1] + self.player.offset[1]})")
            self.entities[self.cave_level].append(Zombie(self.window, self.spritesheet, self.sfx, pos, self.sprite_size))


        ### Check player remove block from map
        for block in self.player.blocks_to_remove:
            if debugging:
                print(f"INFO: Removing block {block}")
            arr = self.map
            if self.cave_level == 1:
                arr = self.underground
            if block in arr:
                if len(block.type) <= 1:
                    results = BLOCK_DROPS[ID_STR(block.texture_id)]
                else:
                    results = BLOCK_DROPS[block.type]
                for result in results:
                    amount = 1
                    if len(result) == 3:
                        amount = random.randint(result[1], result[2])
                    for item in range(0, amount):
                        self.ground_items[self.cave_level].append(Item(self.window, self.spritesheet, (block.pos[0] + self.sprite_size / 6 + random.randint(-50, 50), block.pos[1] + self.sprite_size / 6 + random.randint(-50, 50)), result[0], (self.sprite_size / 1.5, self.sprite_size / 1.5)))
                self.particles[self.cave_level].add_particles((block.center[0] + block.size[0] / 2+ self.player.offset[0], block.center[1] + self.player.offset[1]), block.texture_id)
                self.sfx.play(HIT_BLOCK, debugging=debugging)
                arr.remove(block)
                self.player.blocks_to_remove.remove(block)

        ### Check player add block to map
        for block in self.player.blocks_to_add:
            if debugging:
                print(f"INFO: Adding block {block}")
            if isinstance(self.selected_block, Campfire):
                if block[0] not in COOKABLE_ITEMS:
                    self.player.inventory.add_item((block[0], 1))
                    self.player.blocks_to_add.remove(block)
                    return
                self.selected_block.add_to_fire(block[0])
                self.player.blocks_to_add.remove(block)
                return
            if not block[0] in SPECIAL_BLOCKS and block[0] in BLOCK_PLACABLE:
                rect = Rect(self.selected_block.pos, self.selected_block.size, (0, 0, 0), "", self.window.get(), self.spritesheet.image(block[0], size=(self.sprite_size, self.sprite_size)), texture_id=block[0])
                if self.cave_level == 0:
                    self.map.append(rect)
                else:
                    self.underground.append(rect)
            elif block[0] in LIGHT_BLOCKS:
                if block[0] == TORCH:
                    light_range = 3 
                elif block[0] == CAMPFIRE_1:
                    light_range = 4

                self.light_sources[self.cave_level].append(LightSource(self.window, self.selected_block.center, light_range, color=(255, 226, 110)))
                if block[0] == CAMPFIRE_1:
                    self.special_blocks[self.cave_level].append(Campfire(self.window, self.spritesheet, self.selected_block.pos, self.selected_block.size))
                    self.floating_texts[self.cave_level].append(FloatingText(self.font, "New Beggining", (198, 169, 212), (self.player.player.center[0], self.player.player.pos[1] - 10), (0, 0.2)))
                    self.floating_texts[self.cave_level].append(FloatingText(self.font, "+1", (198, 169, 212), (self.player.player.center[0], self.player.player.pos[1] - 30), (0, 0.2)))
                    self.player.add_xp(1)
                elif block[0] == TORCH:
                    sprite = self.spritesheet.image(TORCH, size=(self.sprite_size, self.sprite_size))
                    self.special_blocks[self.cave_level].append(Rect(self.selected_block.pos, self.selected_block.size, (0, 0, 0), "TORCH", self.window.get(),sprite))
            
            particle_pos = (self.selected_block.center[0] + self.selected_block.size[0] / 2 + self.player.offset[0],
                            self.selected_block.center[1] + self.player.offset[1])
            self.particles[self.cave_level].add_particles(particle_pos, block[0])
            
            self.sfx.play(PLACE_BLOCK, debugging=debugging)
            self.player.blocks_to_add.remove(block)
