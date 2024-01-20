from pygame.sprite import Sprite

class Text(Sprite):
    def __init__(self, font, text, color, position):
        Sprite.__init__(self)
        self._font = font
        self._text = text
        self._color = color
        self._anchor = "topleft"
        self._position = position
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

    def set_position(self, position, anchor=None):
        self._position = position
        if anchor:
            self._anchor = anchor

        self.rect = self.image.get_rect(**{self._anchor: self._position})