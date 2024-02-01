import time
from typing import Tuple
import pygame
from pygame.sprite import Sprite

class Text(Sprite):
    def __init__(self, font: pygame.font, text: str, color: Tuple[int, int, int], position: Tuple[int, int], center: bool=False):
        Sprite.__init__(self)
        self._font = font
        self._text = text
        self._color = color
        self.center = center
        self._anchor = "topleft"
        
        self._position = [position[0], position[1]]
        if center:
            text_size = font.size(text)
            self._position[0] -= text_size[0] / 2
            self._position[1] -=text_size[1] / 2
        self._render()

    def _render(self):
        self.image = self._font.render(self._text, 1, self._color)
        self.rect = self.image.get_rect(**{self._anchor: self._position})

    def clip(self, rect):
        self.image = self.image.subsurface(rect)
        self.rect = self.image.get_rect(**{self._anchor: self._position})

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def set_text(self, text):
        self._text = text
        self._render()

    def set_font(self, font):
        self._font = font
        self._render()

    def set_color(self, color):
        self._color = color
        self._render()

    def set_position(self, position: Tuple[int, int], anchor=None):
        self._position = [position[0], position[1]]
        #if self.center:
        #    text_size = self._font.size(self._text)
        #    self._position[0] -= text_size[0] / 2
        #    self._position[1] -= text_size[1] / 2
        if anchor:
            self._anchor = anchor

        self.rect = self.image.get_rect(**{self._anchor: self._position})
        

class FloatingText(Text):
    def __init__(self, font: pygame.font, text: str, color: Tuple[int, int, int], pos: Tuple[int, int], velocity: Tuple[int, int], fadeout: int=2):
        super().__init__(font, text, color, pos, True)
        self.velocity = velocity
        self.time = time.time()
        self.fadeout = fadeout

    
    def loop(self):
        self.set_position((self._position[0] - self.velocity[0], self._position[1] - self.velocity[1]))
        if time.time() - self.time > self.fadeout:
            self._text = ""