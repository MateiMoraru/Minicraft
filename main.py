import pygame
from spritesheet import Spritesheet
from window import Window
from environment import Environment
from text import Text

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
        self.spritesheet_ui = Spritesheet("assets/spritesheet_ui.png", 16, 256)
        print("Initialising objects...")
        self.environment = Environment(self.window, self.spritesheet, self.spritesheet_ui, self.font, self.font2)
        print("Done!")
        
        self.running = True


    def run(self):
        try:
            self.loop()
        except Exception as e:
            print(f"Encountered error: {e}")
            self.quit(-1)


    def loop(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.quit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_END:
                        self.quit()
                if e.type == pygame.MOUSEWHEEL:
                    self.environment.player.inventory.change_item(e.y)
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.environment.player.attack()
            self.draw()
        

    def draw(self):
        self.window.draw_start()
        self.environment.draw()
        self.environment.loop()
        Text(self.font, f"FPS: {self.window.get_fps()}", (0, 0, 0), (0, 0)).draw(self.window.get())
        self.window.draw_end()


    def quit(self, code:int=0):
        print(f"Exited program with exit code: {code}")
        self.window.quit()
        pygame.quit()
        quit()


if __name__ == "__main__":
    main = Main()
    main.run()