import time
import pygame
from inventory import Inventory
from text import Text
from window import Window
from rect import Rect, collide_point
from spritesheet import *

class Crafting:
    def __init__(self, window: Window, spritesheet: Spritesheet, spritesheet_ui: Spritesheet, font: pygame.font):
        self.window = window
        self.spritesheet = spritesheet
        self.spritesheet_ui = spritesheet_ui
        self.font = font

        self.start_index = 0
        self.size = 40
        self.hotbar_texture = self.spritesheet_ui.image(UI_INVENTORY_ITEM, size=(self.size, self.size))
        self.hotbar_texture_dark = self.spritesheet_ui.image(UI_INVENTORY_ITEM_DARK, size=(self.size, self.size))
        self.last_mouse_press = time.time()


    def draw(self, inventory: Inventory):
        pos = [self.window.size[0] / 6 * 3, self.window.size[1] / 10]
        pygame.draw.rect(self.window.get(), (66, 35, 9), [pos[0], pos[1], 350, 600])

        idx = 0
        for recipe in CRAFTING_RECIPES:
            if idx < self.start_index:
                idx += 1
                continue

            text = recipe.lower() + ':'
            req_items = []
            result = CRAFTING_RECIPES[recipe][-1][0]
            result_texture = self.spritesheet.image(result, size=(self.size - 10, self.size - 10))

            for i in range(len(CRAFTING_RECIPES[recipe]) - 1):
                item = CRAFTING_RECIPES[recipe][i]
            #for item in CRAFTING_RECIPES[recipe]:
                text += f" {item[1]} {ID_STR(item[0]).lower()} &"
                req_items.append(item)

            text = text.replace("_", " ")
            text = text[:-1]
            Text(self.font, text, (0, 0, 0), (pos[0] + self.size + 5, pos[1] + 15 + self.size * (idx - self.start_index))).draw(self.window.get())
            
            if collide_point([pos[0], pos[1] + 5 + self.size * (idx - self.start_index), self.size, self.size], pygame.mouse.get_pos()):
                hpos = (pos[0], pos[1] + 5 + self.size * (idx - self.start_index))
                self.window.get().blit(self.hotbar_texture_dark, hpos)
                self.window.get().blit(result_texture, (hpos[0] + 5, hpos[1] + 5))
                
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
                hpos = (pos[0], pos[1] + 5 + self.size * (idx - self.start_index))
                self.window.get().blit(self.hotbar_texture, hpos)
                self.window.get().blit(result_texture, (hpos[0] + 5, hpos[1] + 5))
            idx += 1


    def scroll(self, dy: int):
        self.start_index += dy
        if self.start_index < 0:
            self.start_index = 0

CRAFTING_RECIPES = {
    "STICK": [(LOG, 2), (STICK, 4)],
    "PLANK": [(LOG, 4), (PLANK, 4)],
    "STONE AXE": [(STICK, 2), (STONE, 3), (STONE_AXE, 1)],
    "STONE PICKAXE": [(STICK, 2), (STONE, 3), (STONE_PICKAXE, 1)],
    "PLANKS BLOCK": [(PLANK, 4), (PLANK_BLOCK, 1)],
    "PLANKS FLOOR": [(PLANK, 4), (PLANK_FLOOR, 1)],
    "CRAFTING TABLE": [(PLANK, 4), (IRON_INGOT, 3), (CRAFTING_TABLE, 1)],
    "DOOR": [(PLANK, 6), (DOOR_CLOSED, 1)],
    "CAMPFIRE": [(STICK, 4), (COAL, 2), (STONE, 3), (CAMPFIRE_1, 1)],
    "BRICK_BLOCK": [(BRICK, 4), (BRICK_BLOCK, 1)],
    "TORCH": [(COAL, 1), (STICK, 2), (TORCH, 1)],
    "IRON AXE": [(STICK, 2), (IRON_INGOT, 3), (AXE, 1)],
    "IRON PICKAXE": [(STICK, 2), (IRON_INGOT, 3), (PICKAXE, 1)]
}
