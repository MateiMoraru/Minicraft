import pygame

DAMAGE = 0
ITEM_PICKUP = 1
HIT_BLOCK = 2
PLACE_BLOCK = 3
WALK = 4

class SFX:
    def __init__(self):
        damage = pygame.mixer.Sound("assets/sfx/damage.wav")
        item_pickup = pygame.mixer.Sound("assets/sfx/item-pickup.wav")
        hit_block = pygame.mixer.Sound("assets/sfx/hit-block.wav")
        place_block = pygame.mixer.Sound("assets/sfx/place-block.wav")
        walk = pygame.mixer.Sound("assets/sfx/walk.wav")

        self.sounds = [damage, item_pickup, hit_block, place_block, walk]

    
    def play(self, sound: int):
        pygame.mixer.Sound.play(self.sounds[sound])


    def stop(self, sound: int):
        pygame.mixer.Sound.stop(self.sounds[sound])