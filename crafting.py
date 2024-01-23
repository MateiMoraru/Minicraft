import time
import pygame
from inventory import Inventory
from text import Text
from window import Window
from rect import Rect, collide_point
from spritesheet import *

class Crafting:
    def __init__(self, window: Window, spritesheet: Spritesheet, spritesheet_ui: Spritesheet, font: pygame.Font):
        self.window = window
        self.spritesheet = spritesheet
        self.spritesheet_ui = spritesheet_ui
        self.font = font

        self.size = 25
        self.hotbar_texture = self.spritesheet_ui.image(UI_INVENTORY_ITEM, size=(self.size, self.size))
        self.hotbar_texture_dark = self.spritesheet_ui.image(UI_INVENTORY_ITEM_DARK, size=(self.size, self.size))
        self.last_mouse_press = time.time()


    def draw(self, inventory: Inventory):
        pos = [self.window.size[0] / 6 * 3, self.window.size[1] / 10]
        pygame.draw.rect(self.window.get(), (66, 35, 9), [pos[0], pos[1], 350, 600])

        idx = 0
        for recipe in CRAFTING_RECIPES:
            text = recipe.lower() + ':'
            req_items = []
            for i in range(len(CRAFTING_RECIPES[recipe]) - 1):
                item = CRAFTING_RECIPES[recipe][i]
            #for item in CRAFTING_RECIPES[recipe]:
                text += f" {item[1]}x{ID_STR(item[0]).lower()}"
                req_items.append(item)

            Text(self.font, text, (0, 0, 0), (pos[0] + 30, pos[1] + 10 + 30 * idx)).draw(self.window.get())
            
            if collide_point([pos[0], pos[1] + 5 + 30 * idx, self.size, self.size], pygame.mouse.get_pos()):
                self.window.get().blit(self.hotbar_texture_dark, (pos[0], pos[1] + 5 + 30 * idx))
                if pygame.mouse.get_pressed()[0] and time.time() - self.last_mouse_press > 0.3:
                    self.last_mouse_press = time.time()
                    req_pass = True
                    for item in req_items:
                        if not inventory.has(item):
                            req_pass = False
                    if req_pass:
                        item = CRAFTING_RECIPES[recipe][-1]
                        for req in req_items:
                            inventory.remove(req)
                        inventory.add_item(item)
                        
            else:
                self.window.get().blit(self.hotbar_texture, (pos[0], pos[1] + 5 + 30 * idx))
            idx += 1


CRAFTING_RECIPES = {
    "STICK": [(LOG, 2), (STICK, 4)],
    "PLANK": [(LOG, 4), (PLANK, 4)],
    "STONE AXE": [(STICK, 2), (STONE, 3), (STONE_AXE, 1)],
    "STONE PICKAXE": [(STICK, 2), (STONE, 3), (STONE_PICKAXE, 1)],
    "PLANKS BLOCK": [(PLANK, 4), (PLANK_BLOCK, 1)],
    "PLANKS FLOOR": [(PLANK, 4), (PLANK_FLOOR, 1)],
    "DOOR": [(PLANK, 6), (DOOR_CLOSED, 1)],
    "CAMPFIRE": [(STICK, 4), (COAL, 2), (STONE, 3), (CAMPFIRE_1, 1)]
}