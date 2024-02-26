import math
import random
import time
import pygame
from animation import Animation
from crafting import Crafting
from inventory import Inventory
from light import LightSource
from particles import Particles
from rect import *
from window import Window
from spritesheet import *
from sfx_manager import *
from text import *

class Player:
    def __init__(self, window: Window, spritesheet: Spritesheet, spritesheet_ui: Spritesheet, font: pygame.font, font2: pygame.font, sfx: SFX):
        self.window = window
        self.spritesheet = spritesheet
        self.sfx = sfx
        self.font = font
        self.font2 = font2
        self.speed = 0.5
        self.direction = "stand"
        self.offset = [0, 0]
        self.underground_offset = [0, 0]
        self.underground = False
        self.size = [64, 64]
        self.player = Rect((window.get_center()[0] - self.size[0] / 2, window.get_center()[1] - self.size[1] / 2), self.size, (0, 0, 0), "PLAYER", self.window.get(), spritesheet.image(PLAYER_1))
        self.default_texture = self.player.texture
        self.update_colliders()
        self.collided = [False, False, False, False]
        self.walk_sfx_time = time.time()

        self.selected_block = None
        self.selected_entity = None
        self.current_damage = 1
        self.blocks_to_remove = []
        self.blocks_to_add = []
        self.xp = 5
        self.level_up = 10
        self.level = 1
        self.last_cave_level_change = time.time()

        self.health = 10
        self.heart_texture = spritesheet_ui.image(UI_HEART, size=(45, 45))
        self.xp_bar_texture = spritesheet_ui.image(UI_XP_BAR, size=(350, 90))

        self.inventory = Inventory(window, spritesheet, spritesheet_ui, font2)
        self.crafting = Crafting(window, spritesheet, spritesheet_ui, font2)

        self.particles = Particles(self.window, self.spritesheet, self.player.pos, 5, acceletaion=0.01, multiplier=0.1)

        self.produce_light = False
        self.light = LightSource(self.window, self.player.pos, 3, color=(255, 226, 110), max_intensity=200)

        self.animation_down = Animation(window, spritesheet, 2, PLAYER_2, delay=0.15)
        self.animation_down.start()
        self.animation_left = Animation(window, spritesheet, 3, PLAYER_LEFT_1, delay=0.15)
        self.animation_left.start()
        self.animation_right = Animation(window, spritesheet, 3, PLAYER_RIGHT_1, delay=0.15)
        self.animation_right.start()
        self.animation_up = Animation(window, spritesheet, 2, PLAYER_UP_2, delay=0.15)
        self.animation_up.start()


    def update_colliders(self):
        self.colliders = [None, None, None, None]
        collider_up = Rect((self.player.pos[0] + 15, self.player.pos[1]), (self.player.size[0] - 30, 5), (255, 0, 0), "COLLIDER_UP", self.window.get())
        collider_down = Rect((self.player.pos[0] + 15, self.player.pos[1] + self.player.size[1]), (self.player.size[0] - 30, 5), (255, 0, 0), "COLLIDER_DOWN", self.window.get())
        collider_left = Rect((self.player.pos[0] + 10, self.player.pos[1] + 10), (5, self.player.size[1] - 10), (255, 0, 0), "COLLIDER_RIGHT", self.window.get())
        collider_right = Rect((self.player.pos[0] + self.player.size[0] - 15, self.player.pos[1] + 10), (5, self.player.size[1] - 10), (255, 0, 0), "COLLIDER_RIGHT", self.window.get())
        collider_middle = Rect((self.player.pos[0] + 15, self.player.pos[1] + self.player.size[1] / 2), (self.player.size[0] - 30, 5), (255, 0, 0), "COLLIDER_MIDDLE", self.window.get())

        self.colliders[0] = collider_up
        self.colliders[1] = collider_down
        self.colliders[2] = collider_left
        self.colliders[3] = collider_right
        self.collider_middle = collider_middle


    def update_current_damage(self):
        current_tool = self.inventory.item[0]
        if current_tool not in WEAPON_DAMAGE:
            self.current_damage = 1
            return
        for tool in WEAPON_DAMAGE:
            if tool == current_tool:
                self.current_damage = WEAPON_DAMAGE[tool]


    def draw(self):
        if self.in_water:
            tex = self.player.texture
            tex = tex.subsurface([0, 0, tex.get_size()[0], tex.get_size()[1] / 2])
            self.player.set_texture(tex, False)
        
        if not self.in_water:
            self.particles.draw()
        self.player.draw()
        self.inventory.draw()
        self.draw_health()
        self.draw_xp_bar()
        #self.draw_colliders()


    def draw_xp_bar(self):
        pos = (self.window.size[0] / 2 - 175, -20)
        self.window.get().blit(self.xp_bar_texture, pos)
        w = self.xp / self.level_up * 350
        rect(self.window.get(), (pos[0] + 22, pos[1] + 39), (w, 5), (108, 43, 138, 200))
        Text(self.font, str(self.level), (198, 169, 212), (pos[0] - 20, pos[1] + 29)).draw(self.window.get())
        Text(self.font, str(self.level + 1), (198, 169, 212), (pos[0] + 360, pos[1] + 29)).draw(self.window.get())
        Text(self.font2, f"{self.xp}/{self.level_up}", (198, 169, 212), (pos[0] + 150, pos[1] + 50)).draw(self.window.get())

    
    def draw_health(self):
        pos = [self.window.size[0] - 46, 0]
        for i in range(0, self.health, 2):
            self.window.get().blit(self.heart_texture, pos)
            pos[0] -= 46


    def draw_colliders(self):
        for collider in self.colliders:
            if self.collided[self.colliders.index(collider)]:
                collider.draw()


    def check_collision(self, block: Rect):
        offset = self.offset
        if self.underground:
            offset = self.underground_offset
        
        collided = False
        for collider in self.colliders:
            if block.collide_rect(collider.rect, offset=offset):
                self.collided[self.colliders.index(collider)] = True
                collided = True
        return collided


    def loop(self, delta_time: float, floor_block: Rect, debugging=False):
        self.update_colliders()
        self.particles.loop(0.75)

        self.produce_light = self.inventory.item[0] == TORCH
        if self.produce_light:
            self.light.set_pos((self.player.center[0] - self.offset[0], self.player.center[1] - self.offset[1]))

        keys = pygame.key.get_pressed()
        move = [0, 0]
        if keys[pygame.K_w] and not self.collided[0]:
            move[1] += self.speed * delta_time 
            self.direction = "up"
        if keys[pygame.K_a] and not self.collided[2]:
            move[0] += self.speed * delta_time 
            self.direction = "left"
        if keys[pygame.K_s] and not self.collided[1]:
            move[1] -= self.speed * delta_time 
            self.direction = "down"
        if keys[pygame.K_d] and not self.collided[3]:
            move[0] -= self.speed * delta_time
            self.direction = "right"
        if move[0] != 0 and move[1] != 0:
            move[0] /= math.sqrt(2)
            move[1] /= math.sqrt(2)
        if self.in_water:
            move[0] /= 2
            move[1] /= 2
        if not self.underground:
            self.offset[0] += move[0]
            self.offset[1] += move[1]
        else:
            self.underground_offset[0] += move[0]
            self.underground_offset[1] += move[1]

        if move[0] == 0 and move[1] == 0:
            self.direction = "stand"
            self.sfx.stop(WALK)
        else:
            delay = 0.3 + random.uniform(-0.1, 0.25)
            if self.in_water:
                delay = 0.9
            if time.time() - self.walk_sfx_time > delay:
                if not self.in_water:
                    self.sfx.play(WALK, debugging=debugging)
                else:
                    self.sfx.play(SWIM, debugging=debugging)
                self.walk_sfx_time = time.time()
            x = 3
            x_mult, y_mult = (random.uniform(.1, x), random.uniform(.1, x))
            self.particles.add_particles([self.player.pos[0] + self.player.size[0] / 2 + move[0] * x_mult, self.player.pos[1] + self.player.size[1] + move[1] * y_mult], floor_block.texture_id, multiplier=0.1)

        self.collided = [False, False, False, False]

        if self.direction == "stand":
            self.player.set_texture(self.default_texture)
        else:
            if self.direction == "down":
                frame = self.animation_down.get
            elif self.direction == "right":
                frame = self.animation_right.get
            elif self.direction == "left":
                frame = self.animation_left.get
            elif self.direction == "up":
                frame = self.animation_up.get
            self.player.set_texture(frame)


    def set_in_water(self, bool=True):
        self.in_water = bool


    def add_xp(self, xp: int):
        self.xp += xp

        if self.xp > self.level_up:
            self.xp = 0
            self.level += 1
            self.level_up *= 2.5

    
    def harm(self, damage: int, source: str=None, debugging=False):
        if debugging:
            print(f"INFO: Player took -{damage}hp from {source}")
        self.sfx.play(DAMAGE, debugging=debugging)
        self.health -= damage
        self.particles.add_particles([self.player.pos[0] + self.player.size[0] / 2, self.player.pos[1] + self.player.size[1] / 2], BLOOD, multiplier=2)
        self.damage_source = source
        return (damage, source)


    def attack(self):
        current_tool = self.inventory.item
        current_tool_type = ID_STR(current_tool[0])

        used_tool = False

        if self.selected_entity is not None:
            self.selected_entity.harm(self.current_damage)
            return ("ENTITY", self.current_damage)
        if self.selected_block:
            type = ID_STR(self.selected_block.texture_id)
            if type == "GRASS_BLOCK" and current_tool[0] == SHOVEL:
                self.blocks_to_remove.append(self.selected_block)
                self.blocks_to_add.append([GRASS_BLOCK_DUG, 0])
                used_tool = True

                #return?? why was return here

            for tool in BLOCK_BREAKING:
                if current_tool_type == tool or tool == "ANY":
                    if type in BLOCK_BREAKING[tool]:
                        self.blocks_to_remove.append(self.selected_block)
                        used_tool = True
            if current_tool_type == None or current_tool_type not in ID_STR(current_tool[0]):
                return
            if used_tool and random.random() > TOOL_BREAK_CHANCE[current_tool_type]:
                self.inventory.remove_current_item()
                print(f"INFO: ITEM BROKE! chance: {TOOL_BREAK_CHANCE[current_tool_type]}")


    def place(self):
        if self.inventory.item[0] in BLOCK_PLACABLE and self.selected_block.texture_id in BACKGROUND_BLOCKS:
            self.blocks_to_add.append(self.inventory.item)
            self.inventory.remove_current_item(1)
        elif self.selected_block.texture_id == CRAFTING_TABLE:
            return "CRAFT"
        elif self.inventory.item[0] in COOKABLE_ITEMS:
            self.blocks_to_add.append(self.inventory.item)
            self.inventory.remove_current_item(1)
        elif self.inventory.item[0] in FRUIT:
            dhealth = FRUIT_HEALTH[ID_STR(self.inventory.item[0])]
            if self.health + dhealth <= 10:
                self.health += dhealth
            self.sfx.play(EAT)
            self.inventory.remove_current_item(1)
        elif self.selected_block.__type__ == "CHEST":
            self.selected_block.opened = True
            print(self.selected_block.rarity)
