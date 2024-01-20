import pygame
from window import Window
from spritesheet import Spritesheet
from typing import Tuple
import time

class Animation:
    def __init__(self, window: Window, spritesheet: Spritesheet, frames: int, start_id: int, delay: int=.2, size: Tuple[int, int]=(64, 64)):
        self.window = window
        self.spritesheet = spritesheet
        self.start_id = start_id
        self.frames = []
        self.current_frame = 0
        self.delay = delay

        for i in range(0, frames):
            frame = spritesheet.image(start_id + i)
            frame = pygame.transform.scale(frame, size)
            self.frames.append(frame)


    def start(self):
        self.start_time = time.time()

    @property
    def get(self):
        delta_time = time.time() - self.start_time
        if delta_time > self.delay:
            self.current_frame += 1
            self.start_time = time.time()
            if self.current_frame == len(self.frames):
                self.current_frame = 0
        return self.frames[self.current_frame]