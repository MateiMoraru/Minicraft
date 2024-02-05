import random
from typing import Tuple
import pyautogui
import pygame

class Window:
    def __init__(self, size: Tuple[int, int]=(1920, 1080), fullscreen: int=0, display_no: int=0, fps: int=0, window_title: str="Windows Application"):
        self.size = size
        self.background_color = (255, 255, 255)
        self.fps = fps
        if fullscreen:
            screen_size = pyautogui.size()
            self.size = (screen_size.width, screen_size.height)
            self.scale = screen_size[0] / 1920
            print("Window size: " + str(self.size))
            self.window = pygame.display.set_mode(self.size, pygame.FULLSCREEN, vsync=1, display=display_no)
        else:
            self.window = pygame.display.set_mode(self.size, vsync=1, display=display_no)
        pygame.display.set_caption(window_title)

        self.clock = pygame.time.Clock()

    
    def set_ico(self, ico_name):
        icon = pygame.image.load(ico_name)
        pygame.display.set_icon(icon)

    
    def draw_start(self):
        self.delta_time = self.clock.tick(self.fps)
        self.window.fill(self.background_color)

    
    def draw_end(self):
        pygame.display.flip()

        if self.get_fps() > 60 and self.get_fps() < 120 and self.fps != 60:
            print(f"INFO: Set FPS cap to 60 (from {self.fps})")
            self.fps = 60
            

    def get(self):
        return self.window
    

    def get_center(self):
        return (self.size[0] / 2, self.size[1] / 2)
    

    def get_fps(self):
        return int(self.clock.get_fps())


    def set_color(self, color:Tuple[int, int, int]):
        self.background_color = color

    @property
    def boundaries(self):
        return self.size
    

    def random_in_boundaries(self):
        return (random.randint(0, self.size[0]), random.randint(0, self.size[1]))

    def quit(self):
        pygame.quit()
        quit()