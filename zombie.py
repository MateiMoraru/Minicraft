import time
import pygame
from typing import Tuple
from animation import Animation
from player import Player
from window import Window
from spritesheet import *
from rect import Rect
from enemy import Enemy
from sfx_manager import SFX

class Zombie(Enemy):
    def __init__(self, window: Window, spritesheet: Spritesheet, sfx: SFX, pos: Tuple[int, int], size: int):
        super().__init__(window, spritesheet, sfx, pos, size, ZOMBIE, "ZOMBIE")

    def loop(self, player:Player, offset: Tuple[int, int]=(0, 0)):
        super().loop(player, offset=offset)

        self.attack(player)


    def attack(self, player: Player):
        super().attack(player, damage=2)