import time
import pygame
from menu import Menu
from spritesheet import Spritesheet
from window import Window
from environment import Environment
from text import FloatingText, Text
from sfx_manager import *

# GAME STATES
MAINMENU = 0
INGAME = 1
INVENTORY = 2
CRAFTING = 3
DIED_MENU = 4

class Main:
    def __init__(self):
        start = time.time()
        print("Initialising pygame...")
        pygame.init()
        print("Initialising window...")
        self.window = Window(size=(1200, 800), fps=0, window_title="Minicraft")
        self.window.set_color((54, 119, 224))
        print("Loading fonts...")
        self.font = pygame.Font("assets/font.ttf", 30)
        self.font2 = pygame.Font("assets/font.ttf", 15)
        print("Loading spritesheets...")
        self.spritesheet = Spritesheet("assets/spritesheet.png", 16, 256)
        self.spritesheet_ui = Spritesheet("assets/spritesheet_ui.png", 16, 64)
        print("Loading sound effects...")
        self.sfx = SFX()
        self.sfx.play(BACKGROUND_NOISE, 0.3)
        print("Initialising environment...")
        self.environment = Environment(self.window, self.spritesheet, self.spritesheet_ui, self.font, self.font2, self.sfx)
        print(f"Done! (Everything loaded correctly in {round((time.time() - start) * 1000, 2)}ms)")
        
        self.running = True
        self.state = 0
        self.debugging = False
        main_menu = Menu(self.window.get(), self.window.size, self.window.size)
        main_menu.add_buttons(self.main_menu_start, self.font, (self.window.size[0] / 2 , self.window.size[1] / 2), (500, 50), (111, 123, 128, 255), "Start Game")
        main_menu.add_buttons(self.quit, self.font, (self.window.size[0] / 2, self.window.size[1] / 2 + 100), (500, 50), (111, 123, 128, 255), "Exit")
        main_menu.add_buttons(self.debug, self.font, (self.window.size[0] / 2, self.window.size[1] / 2 + 200), (500, 50), (111, 123, 128, 255), "Debug Mode")
        self.main_menu = main_menu

        died_menu = Menu(self.window.get(), self.window.size, self.window.size)
        died_menu.add_buttons(self.died_menu_restart, self.font, (self.window.size[0] / 2 , self.window.size[1] / 2), (500, 50), (111, 123, 128, 255), "Restart Game")
        died_menu.add_buttons(self.quit, self.font, (self.window.size[0] / 2, self.window.size[1] / 2 + 100), (500, 50), (111, 123, 128, 255), "Exit")
        self.died_menu = died_menu



    def run(self):
        #try:
        self.loop()
        self.quit(0)
        #except Exception as e:
        #    print(f"Encountered error: {e}")
        #    self.quit(-1)


    def loop(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.quit()
                
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_END:
                        self.quit()
                    if e.key == pygame.K_ESCAPE:
                        if self.state == MAINMENU:
                            self.state = INGAME
                        elif self.state == INGAME:
                            self.state = MAINMENU
                    if e.key == pygame.K_e:
                        if self.state == INVENTORY:
                            self.state = INGAME
                        elif self.state == CRAFTING:
                            self.state = INGAME
                        elif self.state == INGAME:
                            self.state = INVENTORY
                    if e.key == pygame.K_1:
                        self.environment.player.inventory.selected_item(0)
                    if e.key == pygame.K_2:
                        self.environment.player.inventory.selected_item(1)
                    if e.key == pygame.K_3:
                        self.environment.player.inventory.selected_item(2)
                    if e.key == pygame.K_4:
                        self.environment.player.inventory.selected_item(3)
                    if e.key == pygame.K_5:
                        self.environment.player.inventory.selected_item(4)
                if self.state == INGAME:
                    if e.type == pygame.MOUSEWHEEL:
                        self.environment.player.inventory.change_item(e.y)
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pressed()
                        if mouse[0]:
                            res = self.environment.player.attack()
                            if res is not None and res[0] == "ENTITY":
                                pos = self.environment.player.selected_entity.enemy.center
                                self.environment.floating_texts.append(FloatingText(self.font, f"-{res[1]}", (200, 50, 50), (pos[0] + self.environment.player.offset[0], pos[1] + self.environment.player.offset[1]), (0, 0.3), fadeout=.5))
                        if mouse[2]:
                            r = self.environment.player.place()
                            if r == "CRAFT":
                                self.state = CRAFTING
            if self.environment.player.underground:
                self.window.set_color((20, 9, 5))

            if self.environment.player.health <= 0:
                self.state = DIED_MENU
                text = f"Died due to {self.environment.player.damage_source}"
                self.died_menu.add_text(self.font, (self.window.size[0] / 2 - self.font.size(text)[0] / 2, self.window.size[1] / 2 - 100), (500, 50), (255, 255, 255, 255), text)
            
            self.draw()
        

    def draw(self):
        self.window.draw_start()
        if self.state == INGAME:
            self.environment.draw()
            self.environment.loop(self.debugging)
        if self.state == MAINMENU:
            self.main_menu.draw()
        if self.state == INVENTORY:
            self.environment.draw()
            self.environment.player.inventory.draw_inventory()
        if self.state == CRAFTING:
            self.environment.draw()
            self.environment.player.crafting.draw(self.environment.player.inventory)
            self.environment.player.inventory.draw_inventory()
        if self.state == DIED_MENU:
            self.died_menu.draw()
        Text(self.font, f"FPS: {self.window.get_fps()}", (0, 0, 0), (0, 0)).draw(self.window.get())
        self.window.draw_end()


    def main_menu_start(self):
        self.state = INGAME


    def debug(self):
        self.debugging = not self.debugging

    def died_menu_restart(self):
        self.environment = Environment(self.window, self.spritesheet, self.spritesheet_ui, self.font, self.font2, self.sfx)
        self.state = MAINMENU

    def quit(self, code:int=0):
        print(f"Exited program with exit code: {code}")
        self.window.quit()
        pygame.quit()
        quit()


if __name__ == "__main__":
    main = Main()
    main.run()