import random
import time
import pygame
from typing import Tuple
from animation import Animation
from player import Player
from window import Window
from spritesheet import *
from rect import *
from sfx_manager import *
from particles import Particles

class Enemy:
    def __init__(self, window: Window, spritesheet: Spritesheet, sfx: SFX, pos: Tuple[int, int], size: int, texture_id: int=ZOMBIE, name: str="ZOMBIE"):
        self.window = window
        self.spritesheet = spritesheet
        self.sfx = sfx
        self.default_texture = spritesheet.image(texture_id)
        self.name = name
        self.enemy = Rect(pos, (size, size), (0, 0, 0), name, window.get(), self.default_texture)
        self.direction = "stand"
        self.speed = 0.1
        self.health = 10
        if texture_id == ZOMBIE:
            self.damage_sound = ZOMBIE_DIE
        self.particles = Particles(self.window, self.spritesheet, pos, 5, .01, 1)
        self.special_item = RANDOM_ZOMBIE_DROP[random.randint(0, len(RANDOM_ZOMBIE_DROP) - 1)]

        self.animation_down = Animation(window, spritesheet, 2, texture_id + 1, delay=0.15)
        self.animation_down.start()
        self.animation_left = Animation(window, spritesheet, 3, texture_id + 6, delay=0.15)
        self.animation_left.start()
        self.animation_right = Animation(window, spritesheet, 3, texture_id + 3, delay=0.15)
        self.animation_right.start()
        self.animation_up = Animation(window, spritesheet, 2, texture_id + 9, delay=0.15)
        self.animation_up.start()
        self.update_colliders()
        self.collided = [False, False, False, False]
        self.last_attack = time.time()


    def update_colliders(self, offset: Tuple[int, int]=(0, 0)):
        self.colliders = [None, None, None, None]
        collider_up = Rect((self.enemy.pos[0] + 15 + offset[0], self.enemy.pos[1] + offset[1]), (self.enemy.size[0] - 30, 5), (255, 0, 0), "COLLIDER_UP", self.window.get())
        collider_down = Rect((self.enemy.pos[0] + 15 + offset[0], self.enemy.pos[1] + self.enemy.size[1] + offset[1]), (self.enemy.size[0] - 30, 5), (255, 0, 0), "COLLIDER_DOWN", self.window.get())
        collider_left = Rect((self.enemy.pos[0] + 10 + offset[0], self.enemy.pos[1] + 10 + offset[1]), (5, self.enemy.size[1] - 10), (255, 0, 0), "COLLIDER_RIGHT", self.window.get())
        collider_right = Rect((self.enemy.pos[0] + self.enemy.size[0] - 15 + offset[0], self.enemy.pos[1] + 10 + offset[1]), (5, self.enemy.size[1] - 10), (255, 0, 0), "COLLIDER_RIGHT", self.window.get())
        collider_middle = Rect((self.enemy.pos[0] + 15 + offset[0], self.enemy.pos[1] + self.enemy.size[1] / 2 + offset[1]), (self.enemy.size[0] - 30, 5), (255, 0, 0), "COLLIDER_MIDDLE", self.window.get())

        self.colliders[0] = collider_up
        self.colliders[1] = collider_down
        self.colliders[2] = collider_left
        self.colliders[3] = collider_right
        self.collider_middle = collider_middle

    
    def draw(self, offset: Tuple[int, int]=(0, 0)):
        self.enemy.draw(offset)
        self.particles.draw(offset)


    def loop(self, player:Player, offset: Tuple[int, int]=(0, 0)):
        self.update_colliders(offset)
        self.particles.loop(.9)

        dist = dist_block(self.enemy.center, player.player, offset)
        if dist > 4 * player.player.size[0]:
            return

        player_dx = player.player.pos[0] - (self.enemy.pos[0] + offset[0])
        if player_dx != 0:
            player_dx /= abs(player_dx)
        player_dy = player.player.pos[1] - (self.enemy.pos[1] + offset[1])
        if player_dy != 0:
            player_dy /= abs(player_dy)

        if player_dx > 0 and self.collided[3] or player_dx < 0 and self.collided[2]:
            player_dx = 0
        elif player_dy > 0 and self.collided[1] or player_dy < 0 and self.collided[0]:
            player_dy = 0 

        if abs(player.player.pos[0] - (self.enemy.pos[0] + offset[0])) >= abs(player.player.pos[1] - (self.enemy.pos[1] + offset[1])):
            if player_dx > 0 and not self.collided[3]:
                self.direction = "right"
            elif not self.collided[2]:
                self.direction = "left"
        else:
            if player_dy > 0 and not self.collided[1]:
                self.direction = "down"
            elif not self.collided[0]:
                self.direction = "up"

        move = [player_dx * self.speed * self.window.delta_time, player_dy * self.speed * self.window.delta_time]
        if (self.collided[3] and move[0] > 0) or (self.collided[2] and move[0] < 0):
            move[0] = 0
        if (self.collided[1] and move[1] > 0) or (self.collided[0] and move[1] < 0):
            move[1] = 0

        self.enemy.move(move[0], move[1])

        if self.direction == "stand":
            self.enemy.set_texture(self.default_texture)
        else:
            if self.direction == "down":
                frame = self.animation_down.get
            elif self.direction == "right":
                frame = self.animation_right.get
            elif self.direction == "left":
                frame = self.animation_left.get
            elif self.direction == "up":
                frame = self.animation_up.get
            self.enemy.set_texture(frame)
        self.collided = [False, False, False, False]

        self.attack(player)


    def attack(self, player: Player, damage: int=1):
        if time.time() - self.last_attack > 1:
            if self.enemy.collide_rect(player.player.rect, player.offset):
                player.harm(damage, self.name)
                self.last_attack = time.time()

    def check_collision(self, block: Rect, offset: Tuple[int, int]=(0, 0)):
        collided = False
        for collider in self.colliders:
            if block.collide_rect(collider.rect, offset=offset):
                self.collided[self.colliders.index(collider)] = True
                collided = True
        return collided
    

    def harm(self, damage: int):
        self.health -= damage
        self.particles.add_particles([self.enemy.pos[0] + self.enemy.size[0] / 2, self.enemy.pos[1] + self.enemy.size[1] / 2], BLOOD, multiplier=2)
        if self.health <= 0:
            self.sfx.play(self.damage_sound)
        return (damage)