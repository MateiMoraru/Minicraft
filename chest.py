import random
import time
from typing import Tuple
import pygame
from window import Window
from spritesheet import *
from rect import *
from inventory import Inventory
from text import Text

class Chest:
    __type__ = "CHEST"
    def __init__(self, window: Window, spritesheet: Spritesheet, pos: Tuple[float, float], size: Tuple[int, int]):
        self.window = window
        self.spritesheet = spritesheet
        self.pos = pos
        self.size = size

        self.texture_id = CHEST_CLOSED
        self.default_texture = spritesheet.image(CHEST_CLOSED, size=size)
        self.closed_texture = spritesheet.image(CHEST_OPENED, size=size)
        self.texture = self.default_texture
        
        self.item_size = 60
        self.length = 8

        self.rect = Rect(pos, size, (0, 0, 0), "CHEST", self.window.get(), self.texture, True, CHEST_CLOSED)
        
        self.opened = False

        self.selected_chest_slot = 0
        self.items = []
        for i in range(self.length * self.length):
            self.items.append([-1, -1])

    def draw(self, offset: Tuple[int, int], inventory: Inventory, underground: bool=False):
        self.selected_chest_slot = None
        self.rect.draw(offset, underground)

        if self.opened:
            inventory.draw_inventory()
            pos = [self.window.size[0] / 2, self.window.size[1] / 10]
            idx = 0
            for j in range(self.length):
                for i in range(self.length):
                    if collide_point([pos[0], pos[1], self.item_size, self.item_size], pygame.mouse.get_pos()):
                        self.selected_chest_slot = idx
                    if pygame.mouse.get_pressed()[0] and time.time() - inventory.select_hover_time > 0.3:
                        if inventory.selected_inventory_slot is not None:
                            if inventory.hovering_item is None:
                                inventory.hovering_item = self.items[self.selected_chest_slot]
                                inventory.inventory[inventory.selected_inventory_slot] = [-1, -1]
                                inventory.select_hover_time = time.time()
                            elif inventory.inventory[inventory.selected_inventory_slot][0] == -1:
                                inventory.inventory[inventory.selected_inventory_slot] = inventory.hovering_item
                                inventory.hovering_item = None
                                inventory.select_hover_time = time.time()
                        elif self.selected_chest_slot is not None:
                            if inventory.hovering_item is None:
                                inventory.hovering_item = self.items[self.selected_chest_slot]
                                self.items[self.selected_chest_slot] = [-1, -1]
                                inventory.select_hover_time = time.time()
                            elif self.items[self.selected_chest_slot][0] == -1:
                                self.items[self.selected_chest_slot] = inventory.hovering_item
                                inventory.hovering_item = None
                                inventory.select_hover_time = time.time()
                    if self.selected_chest_slot == idx:
                        inventory.window.get().blit(inventory.inventory_dark_texture, pos)
                    else:
                        inventory.window.get().blit(inventory.inventory_texture, pos)
                    if idx < len(self.items) and self.items[idx][0] != -1:
                        inventory.window.get().blit(self.spritesheet.image(self.items[idx][0], size=(inventory.inventory_item_size / 1.3, inventory.inventory_item_size / 1.3)), (pos[0] + 7, pos[1] + 4))
                        Text(inventory.font, str(self.items[idx][1]), (0, 0, 0), (pos[0] + inventory.inventory_item_size / 2 - inventory.font.size(str(self.items[idx][1]))[0] / 2, pos[1] + inventory.inventory_item_size - 15)).draw(self.window.get())
                    pos[0] += inventory.inventory_item_size
                    if self.items[idx][1] <= 0:
                        self.items[idx] = [-1, -1]
                    idx += 1
                pos[1] += inventory.inventory_item_size
                pos[0] = inventory.window.size[0] / 2


    #rarity: 0(bad), 1(ok), 2(super rare)
    def set_random(self, rarity: int = 1):
        items = CHEST_RANDOMIZER[rarity]
        for item in items:
            if random.random() > 0.2 * rarity:
                idx = random.randint(0, 63)
                while self.items[idx][0] != -1:
                    idx = random.randint(0, 64)
                self.items[idx] = [item[0], random.randint(1, item[1])]

CHEST_RANDOMIZER = [
    [[COAL, 12], [STRAWBERRY, 12], [IRON_ORE, 5], [STONE, 10], [CLAY, 16], [TORCH, 16]],
    [[BANANA, 16], [GOLD_NUGGET, 10], [TORCH, 32], [IRON_ORE, 10]],
    []
]