import pygame

DAMAGE = 0
ITEM_PICKUP = 1
HIT_BLOCK = 2
PLACE_BLOCK = 3
WALK = 4
BACKGROUND_NOISE = 5
SWIM = 6
ZOMBIE_DIE = 7

class SFX:
    def __init__(self):
        damage = pygame.mixer.Sound("assets/sfx/damage.wav")
        item_pickup = pygame.mixer.Sound("assets/sfx/item-pickup.wav")
        hit_block = pygame.mixer.Sound("assets/sfx/hit-block.wav")
        place_block = pygame.mixer.Sound("assets/sfx/place-block.wav")
        walk = pygame.mixer.Sound("assets/sfx/walk.wav")
        background_noise = pygame.mixer.Sound("assets/sfx/background-noise.mp3")
        swim = pygame.mixer.Sound("assets/sfx/swim.mp3")
        zombie_die = pygame.mixer.Sound("assets/sfx/zombie-die.mp3")

        self.sounds = [damage, item_pickup, hit_block, place_block, walk, background_noise, swim, zombie_die]

    
    def play(self, sound: int, volume: float=1.0):
        pygame.mixer.Sound.set_volume(self.sounds[sound], volume)
        pygame.mixer.Sound.play(self.sounds[sound])


    def stop(self, sound: int):
        pygame.mixer.Sound.stop(self.sounds[sound])