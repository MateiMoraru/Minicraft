import math
import pygame
from animation import Animation
from crafting import Crafting
from inventory import Inventory
from rect import Rect
from window import Window
from spritesheet import *

class Player:
    def __init__(self, window: Window, spritesheet: Spritesheet, spritesheet_ui: Spritesheet, font: pygame.Font, font2: pygame.Font):
        self.window = window
        self.speed = 0.5
        self.direction = "stand"
        self.offset = [0, 0]
        self.size = [64, 64]
        self.player = Rect((window.get_center()[0] - self.size[0] / 2, window.get_center()[1] - self.size[1] / 2), self.size, (0, 0, 0), "PLAYER", self.window.get(), spritesheet.image(PLAYER_1))
        self.default_texture = self.player.texture
        self.update_colliders()
        self.collided = [False, False, False, False]

        self.selected_block = 0
        self.blocks_to_remove = []
        self.blocks_to_add = []

        self.inventory = Inventory(window, spritesheet, spritesheet_ui, font2)
        self.crafting = Crafting(window, spritesheet, spritesheet_ui, font2)

        self.animation_down = Animation(window, spritesheet, 2, PLAYER_2)
        self.animation_down.start()
        self.animation_left = Animation(window, spritesheet, 3, PLAYER_LEFT_1 - 1)
        self.animation_left.start()
        self.animation_right = Animation(window, spritesheet, 3, PLAYER_RIGHT_1 - 1)
        self.animation_right.start()
        self.animation_up = Animation(window, spritesheet, 2, PLAYER_UP_1)
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

    def draw(self):
        if self.in_water:
            tex = self.player.texture
            tex = tex.subsurface([0, 0, tex.get_size()[0], tex.get_size()[1] / 2])
            self.player.set_texture(tex, False)
        self.player.draw()
        #self.draw_colliders()
        self.inventory.draw()

    def draw_colliders(self):
        for collider in self.colliders:
            if self.collided[self.colliders.index(collider)]:
                collider.draw()

    def check_collision(self, block: Rect):
        for collider in self.colliders:
            if block.collide_rect(collider.rect, offset=self.offset):
                self.collided[self.colliders.index(collider)] = True

    def loop(self, delta_time):
        self.update_colliders()

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
        self.offset[0] += move[0]
        self.offset[1] += move[1]

        if move[0] == 0 and move[1] == 0:
            self.direction = "stand"

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

    
    def attack(self):
        current_tool = self.inventory.item

        if self.selected_block != 0:
            if current_tool[0] == AXE:
                if self.selected_block.type == "TREE_1" or self.selected_block.texture_id == TREE_1:
                    self.blocks_to_remove.append(self.selected_block)
                elif self.selected_block.texture_id == CRAFTING_TABLE:
                    self.blocks_to_remove.append(self.selected_block)
            elif current_tool[0] == PICAXE:
                if self.selected_block.type == "ROCK_1" or self.selected_block.texture_id == ROCK_1:
                    self.blocks_to_remove.append(self.selected_block)

    def place(self):
        if self.inventory.item[0] in BLOCK_PLACABLE and self.selected_block.texture_id in BACKGROUND_BLOCKS:
            self.blocks_to_add.append(self.inventory.item)
            self.inventory.remove_current_item(1)
        elif self.selected_block.texture_id == CRAFTING_TABLE:
            return "CRAFT"