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
        self.hotbar = [[AXE, 1], [PICAXE, 1]]
        self.selected_hotbar_slot = 0

    
    def draw(self):
        pos = [self.window.get_center()[0] - (self.hotbar_length / 2 * self.hotbar_item_size), self.window.size[1] - self.hotbar_item_size]
        for i in range(self.hotbar_length):
            if self.selected_hotbar_slot == i:
                self.window.get().blit(self.hotbar_dark_texture, pos)
            else:
                self.window.get().blit(self.hotbar_texture, pos)
            if i < len(self.hotbar):
                self.window.get().blit(self.spritesheet.image(self.hotbar[i][0], size=(self.hotbar_item_size / 1.3, self.hotbar_item_size / 1.3)), (pos[0] + 5, pos[1]))
                Text(self.font, str(self.hotbar[i][1]), (0, 0, 0), (pos[0] + self.hotbar_item_size / 2 - self.font.size(str(self.hotbar[i][1]))[0] / 2, pos[1] + self.hotbar_item_size - 15)).draw(self.window.get())
            pos[0] += self.hotbar_item_size

    
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
    

    def add_item(self, item: int, amount: int=1):
        for items in self.hotbar:
            if items[0] == item:
                items[1] += amount
                return
        if len(self.hotbar) < self.hotbar_length:
            self.hotbar.append([item, amount])
