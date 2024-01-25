import time
import pygame
from typing import Tuple
from animation import Animation
from player import Player
from window import Window
from spritesheet import *
from rect import Rect

class Zombie:
    def __init__(self, window: Window, spritesheet: Spritesheet, pos: Tuple[int, int], size: int):
        self.window = window
        self.spritesheet = spritesheet
        self.default_texture = spritesheet.image(ZOMBIE)
        self.zombie = Rect(pos, (size, size), (0, 0, 0), "ZOMBIE", window.get(), self.default_texture)
        self.direction = "stand"
        self.speed = 0.1

        self.animation_down = Animation(window, spritesheet, 2, ZOMBIE_2, delay=0.15)
        self.animation_down.start()
        self.animation_left = Animation(window, spritesheet, 3, ZOMBIE_LEFT_1, delay=0.15)
        self.animation_left.start()
        self.animation_right = Animation(window, spritesheet, 3, ZOMBIE_RIGHT_1, delay=0.15)
        self.animation_right.start()
        self.animation_up = Animation(window, spritesheet, 2, ZOMBIE_UP_2, delay=0.15)
        self.animation_up.start()
        self.update_colliders()
        self.collided = [False, False, False, False]
        self.last_attack = time.time()


    def update_colliders(self, offset: Tuple[int, int]=(0, 0)):
        self.colliders = [None, None, None, None]
        collider_up = Rect((self.zombie.pos[0] + 15 + offset[0], self.zombie.pos[1] + offset[1]), (self.zombie.size[0] - 30, 5), (255, 0, 0), "COLLIDER_UP", self.window.get())
        collider_down = Rect((self.zombie.pos[0] + 15 + offset[0], self.zombie.pos[1] + self.zombie.size[1] + offset[1]), (self.zombie.size[0] - 30, 5), (255, 0, 0), "COLLIDER_DOWN", self.window.get())
        collider_left = Rect((self.zombie.pos[0] + 10 + offset[0], self.zombie.pos[1] + 10 + offset[1]), (5, self.zombie.size[1] - 10), (255, 0, 0), "COLLIDER_RIGHT", self.window.get())
        collider_right = Rect((self.zombie.pos[0] + self.zombie.size[0] - 15 + offset[0], self.zombie.pos[1] + 10 + offset[1]), (5, self.zombie.size[1] - 10), (255, 0, 0), "COLLIDER_RIGHT", self.window.get())
        collider_middle = Rect((self.zombie.pos[0] + 15 + offset[0], self.zombie.pos[1] + self.zombie.size[1] / 2 + offset[1]), (self.zombie.size[0] - 30, 5), (255, 0, 0), "COLLIDER_MIDDLE", self.window.get())

        self.colliders[0] = collider_up
        self.colliders[1] = collider_down
        self.colliders[2] = collider_left
        self.colliders[3] = collider_right
        self.collider_middle = collider_middle

    
    def draw(self, offset: Tuple[int, int]=(0, 0)):
        self.zombie.draw(offset)


    def loop(self, player:Player, offset: Tuple[int, int]=(0, 0)):
        self.update_colliders(offset)
        player_dx = player.player.pos[0] - (self.zombie.pos[0] + offset[0])
        if player_dx != 0:
            player_dx /= abs(player_dx)
        player_dy = player.player.pos[1] - (self.zombie.pos[1] + offset[1])
        if player_dy != 0:
            player_dy /= abs(player_dy)

        if player_dx > 0 and self.collided[3]:
            player_dx = 0
        elif player_dx < 0 and self.collided[2]:
            player_dx = 0
        elif player_dy > 0 and self.collided[1]:
            player_dy = 0
        elif player_dy < 0 and self.collided[0]:
            player_dy = 0 

        if abs(player.player.pos[0] - (self.zombie.pos[0] + offset[0])) >= abs(player.player.pos[1] - (self.zombie.pos[1] + offset[1])):
            if player_dx > 0 and not self.collided[3]:
                self.direction = "right"
            elif not self.collided[2]:
                self.direction = "left"
        else:
            if player_dy > 0 and not self.collided[1]:
                self.direction = "down"
            elif not self.collided[0]:
                self.direction = "up"

        self.zombie.move(player_dx * self.speed * self.window.delta_time, player_dy * self.speed * self.window.delta_time)

        if self.direction == "stand":
            self.zombie.set_texture(self.default_texture)
        else:
            if self.direction == "down":
                frame = self.animation_down.get
            elif self.direction == "right":
                frame = self.animation_right.get
            elif self.direction == "left":
                frame = self.animation_left.get
            elif self.direction == "up":
                frame = self.animation_up.get
            self.zombie.set_texture(frame)
        self.collided = [False, False, False, False]

        self.attack(player)


    def attack(self, player: Player):
        if time.time() - self.last_attack > 1:
            if self.zombie.collide_rect(player.player.rect, player.offset):
                player.harm(2, "ZOMBIE")
                self.last_attack = time.time()

    def check_collision(self, block: Rect, offset: Tuple[int, int]=(0, 0)):
        collided = False
        for collider in self.colliders:
            if block.collide_rect(collider.rect, offset=offset):
                self.collided[self.colliders.index(collider)] = True
                collided = True
        return collided