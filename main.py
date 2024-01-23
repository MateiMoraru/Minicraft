import pygame
from menu import Menu
from spritesheet import Spritesheet
from window import Window
from environment import Environment
from text import Text
from sfx_manager import SFX

# GAME STATES
MAINMENU = 0
INGAME = 1
INVENTORY = 2
CRAFTING = 3

class Main:
    def __init__(self):
        print("Initialising pygame...")
        pygame.init()
        print("Initialising window...")
        self.window = Window(size=(1200, 800), fps=60, window_title="Minicraft")
        self.window.set_color((54, 119, 224))
        print("Loading fonts and sprites...")
        self.font = pygame.Font("assets/font.ttf", 30)
        self.font2 = pygame.Font("assets/font.ttf", 15)
        self.spritesheet = Spritesheet("assets/spritesheet.png", 16, 256)
        self.spritesheet_ui = Spritesheet("assets/spritesheet_ui.png", 16, 64)
        self.sfx = SFX()
        print("Initialising objects...")
        self.environment = Environment(self.window, self.spritesheet, self.spritesheet_ui, self.font, self.font2, self.sfx)
        print("Done!")
        
        self.running = True
        self.state = 0
        main_menu = Menu(self.window.get(), self.window.size, self.window.size)
        main_menu.add_buttons(self.main_menu_start, self.font, (self.window.size[0] / 2 , self.window.size[1] / 2), (500, 50), (111, 123, 128, 255), "Start Game")
        main_menu.add_buttons(self.quit, self.font, (self.window.size[0] / 2, self.window.size[1] / 2 + 100), (500, 50), (111, 123, 128, 255), "Exit")
        self.main_menu = main_menu


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
                if self.state == INGAME:
                    if e.type == pygame.MOUSEWHEEL:
                        self.environment.player.inventory.change_item(e.y)
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pressed()
                        if mouse[0]:
                            self.environment.player.attack()
                        if mouse[2]:
                            r = self.environment.player.place()
                            if r == "CRAFT":
                                self.state = CRAFTING
            self.draw()
        

    def draw(self):
        self.window.draw_start()
        self.environment.draw()
        if self.state == INGAME:
            self.environment.loop()
        if self.state == MAINMENU:
            self.main_menu.draw()
        if self.state == INVENTORY:
            self.environment.player.inventory.draw_inventory()
        if self.state == CRAFTING:
            self.environment.player.crafting.draw(self.environment.player.inventory)
            self.environment.player.inventory.draw_inventory()
        Text(self.font, f"FPS: {self.window.get_fps()}", (0, 0, 0), (0, 0)).draw(self.window.get())
        self.window.draw_end()


    def main_menu_start(self):
        self.state = INGAME


    def quit(self, code:int=0):
        print(f"Exited program with exit code: {code}")
        self.window.quit()
        pygame.quit()
        quit()


if __name__ == "__main__":
    main = Main()
    main.run()