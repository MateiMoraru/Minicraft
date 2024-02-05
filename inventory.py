import time
import pygame
from window import Window
from rect import *
from spritesheet import *
from text import Text

class Inventory:
    def __init__(self, window: Window, spritesheet: Spritesheet, spritesheet_ui: Spritesheet, font: pygame.Font):
        self.window = window
        self.spritesheet = spritesheet
        self.spritesheet_ui = spritesheet_ui
        self.font = font

        self.hotbar_item_size = 60
        self.hotbar_texture = self.spritesheet_ui.image(UI_HOTBAR_ITEM, size=(self.hotbar_item_size, self.hotbar_item_size))
        self.hotbar_dark_texture = self.spritesheet_ui.image(UI_HOTBAR_ITEM_DARK, size=(self.hotbar_item_size, self.hotbar_item_size))
        self.hotbar_length = 5
        self.hotbar = [[AXE, 1], [PICAXE, 1], [SHOVEL, 1], [CAMPFIRE_1, 1], [TORCH, 1]]
        self.selected_hotbar_slot = 0
        self.selected_hotbar_inventory_slot = 0

        self.inventory_item_size = 60
        self.inventory_texture = self.spritesheet_ui.image(UI_INVENTORY_ITEM, size=(self.hotbar_item_size, self.hotbar_item_size))
        self.inventory_dark_texture = self.spritesheet_ui.image(UI_INVENTORY_ITEM_DARK, size=(self.hotbar_item_size, self.hotbar_item_size))
        self.inventory_length = 8
        self.inventory = []
        self.selected_inventory_slot = 0
        for i in range(self.inventory_length * self.inventory_length):
            self.inventory.append([-1, -1])
        self.inventory[0] = [PLANK_FLOOR, 64]
        self.inventory[1] = [PLANK, 64]
        self.inventory[2] = [BRICK, 64]
        self.hovering_item = None
        self.select_hover_time = time.time()

    
    def draw(self):
        pos = [self.window.get_center()[0] - (self.hotbar_length / 2 * self.hotbar_item_size), self.window.size[1] - self.hotbar_item_size]
        for i in range(self.hotbar_length):
            if self.selected_hotbar_slot == i:
                self.window.get().blit(self.hotbar_dark_texture, pos)
            else:
                self.window.get().blit(self.hotbar_texture, pos)
            if i < len(self.hotbar) and self.hotbar[i][0] != -1:
                self.window.get().blit(self.spritesheet.image(self.hotbar[i][0], size=(self.hotbar_item_size / 1.3, self.hotbar_item_size / 1.3)), (pos[0] + 7, pos[1] + 4))
                Text(self.font, str(self.hotbar[i][1]), (0, 0, 0), (pos[0] + self.hotbar_item_size / 2 - self.font.size(str(self.hotbar[i][1]))[0] / 2, pos[1] + self.hotbar_item_size - 15)).draw(self.window.get())
            pos[0] += self.hotbar_item_size
            if self.inventory[i][1] <= 0:
                self.inventory[i] = [-1, -1]

    
    def draw_inventory(self):
        pos = [self.window.size[0] / 12, self.window.size[1] / 10]
        idx = 0
        self.selected_inventory_slot = None
        self.selected_hotbar_inventory_slot = None
        for j in range(self.inventory_length):
            for i in range(self.inventory_length):
                if collide_point([pos[0], pos[1], self.inventory_item_size, self.inventory_item_size], pygame.mouse.get_pos()):
                    self.selected_inventory_slot = idx
                if pygame.mouse.get_pressed()[0] and self.selected_hotbar_inventory_slot is None and time.time() - self.select_hover_time > 0.3:
                    if self.selected_inventory_slot is not None:
                        if self.hovering_item is None:
                            self.hovering_item = self.inventory[self.selected_inventory_slot]
                            self.inventory[self.selected_inventory_slot] = [-1, -1]
                            self.select_hover_time = time.time()
                        elif self.inventory[self.selected_inventory_slot][0] == -1:
                            self.inventory[self.selected_inventory_slot] = self.hovering_item
                            self.hovering_item = None
                            self.select_hover_time = time.time()
                if self.selected_inventory_slot == idx:
                    self.window.get().blit(self.inventory_dark_texture, pos)
                else:
                    self.window.get().blit(self.inventory_texture, pos)
                if idx < len(self.inventory) and self.inventory[idx][0] != -1:
                    self.window.get().blit(self.spritesheet.image(self.inventory[idx][0], size=(self.inventory_item_size / 1.3, self.inventory_item_size / 1.3)), (pos[0] + 7, pos[1] + 4))
                    Text(self.font, str(self.inventory[idx][1]), (0, 0, 0), (pos[0] + self.inventory_item_size / 2 - self.font.size(str(self.inventory[idx][1]))[0] / 2, pos[1] + self.inventory_item_size - 15)).draw(self.window.get())
                pos[0] += self.inventory_item_size
                if self.inventory[idx][1] <= 0:
                    self.inventory[idx] = [-1, -1]
                idx += 1
            pos[1] += self.inventory_item_size
            pos[0] = self.window.size[0] / 12


        pos = [self.window.get_center()[0] - (self.hotbar_length / 2 * self.hotbar_item_size), self.window.size[1] - self.hotbar_item_size]
        for i in range(self.hotbar_length):
            if collide_point([pos[0], pos[1], self.inventory_item_size, self.inventory_item_size], pygame.mouse.get_pos()):
                self.selected_hotbar_inventory_slot = i
            if pygame.mouse.get_pressed()[0] and self.selected_inventory_slot == None and time.time() - self.select_hover_time > 0.3:
                if self.selected_hotbar_inventory_slot is not None:
                    if self.hovering_item is None:
                        self.hovering_item = self.hotbar[self.selected_hotbar_inventory_slot]
                        self.hotbar[self.selected_hotbar_inventory_slot] = [-1, -1]
                        self.select_hover_time = time.time()
                    elif self.hotbar[self.selected_hotbar_inventory_slot][0] == -1:
                        self.hotbar[self.selected_hotbar_inventory_slot] = self.hovering_item
                        self.hovering_item = None
                        self.select_hover_time = time.time()
            if self.selected_hotbar_slot == i or self.selected_hotbar_inventory_slot == i:
                self.window.get().blit(self.hotbar_dark_texture, pos)
            else:
                self.window.get().blit(self.hotbar_texture, pos)
            if i < len(self.hotbar) and self.hotbar[i][0] != -1:
                self.window.get().blit(self.spritesheet.image(self.hotbar[i][0], size=(self.hotbar_item_size / 1.3, self.hotbar_item_size / 1.3)), (pos[0] + 7, pos[1] + 4))
                Text(self.font, str(self.hotbar[i][1]), (0, 0, 0), (pos[0] + self.hotbar_item_size / 2 - self.font.size(str(self.hotbar[i][1]))[0] / 2, pos[1] + self.hotbar_item_size - 15)).draw(self.window.get())
            pos[0] += self.hotbar_item_size
                    
        if self.hovering_item is not None:
            self.window.get().blit(self.spritesheet.image(self.hovering_item[0], size=(self.inventory_item_size, self.inventory_item_size)), pygame.mouse.get_pos())

    
    def change_item(self, d:int=0):
        self.selected_hotbar_slot += d

        if self.selected_hotbar_slot == self.hotbar_length:
            self.selected_hotbar_slot = 0
        elif self.selected_hotbar_slot == -1:
            self.selected_hotbar_slot = self.hotbar_length - 1

    @property
    def item(self):
        if self.selected_hotbar_slot < self.hotbar_length:
            return self.hotbar[self.selected_hotbar_slot]
        return None
    

    def add_item(self, item: Tuple[int, int]):
        free_slot_hotbar = None
        for items in self.hotbar:
            if items[0] == item[0]:
                items[1] += item[1]
                return
            if items[0] == -1:
                free_slot_hotbar = self.hotbar.index(items)
        for items in self.inventory:
            if items[0] == item[0]:
                items[1] += item[1]
                return
            if items[0] == -1:
                free_slot = self.inventory.index(items)
        if free_slot_hotbar is not None:
            self.hotbar[free_slot_hotbar] = [item[0], item[1]]
            return
        
        if free_slot is not None:
            self.inventory[free_slot] = [item[0], item[1]]
            return
        
    
    def selected_item(self, index: int):
        self.selected_hotbar_slot = index
        

    def remove_current_item(self, amount: int=None):
        if amount == None:
            self.hotbar[self.selected_hotbar_slot] = [-1, -1]
        else:
            self.hotbar[self.selected_hotbar_slot][1] -= amount
            if self.hotbar[self.selected_hotbar_slot][1] <= 0:
                self.hotbar[self.selected_hotbar_slot] = [-1, -1]


    def remove(self, item: Tuple[int, int]):
        idx = 0
        for items in self.inventory:
            if items[0] == item[0]:
                items[1] -= item[1]
                if items[1] <= 0:
                    self.inventory[idx] = [-1, -1]


    def has(self, item: Tuple[int, int]):
        for items in self.inventory:
            if item[0] == items[0]:
                if item[1] == -1:
                    return True
                elif items[1] >= item[1]:
                    return True
        return False