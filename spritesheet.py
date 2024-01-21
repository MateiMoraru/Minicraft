import pygame

class Spritesheet(object):
    def __init__(self, filename, size:int=32, total_size:int=320):
        self.size = size #ex 16x16
        self.total_size = total_size #128x128
        self.sprites_no = self.total_size / self.size
        self.unit_size = total_size / size

        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            print(message)
        

    def image_at(self, rectangle, colorkey = None):

        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    

    def image(self, id, colorkey = (0, 0, 0), size=(32, 32)):
        x = (id % (self.sprites_no)) * self.size
        y = (id // (self.sprites_no)) * self.size
        image = self.image_at((x, y, self.size, self.size), colorkey)
        return pygame.transform.scale(image, size)
    

    def images_at(self, rects, colorkey = (0, 0, 0)):
        return [self.image_at(rect, colorkey) for rect in rects]
    

    def load_strip(self, rect, image_count, colorkey = (0, 0, 0)):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
    
GRASS_BLOCK = 0
SAND_BLOCK = 1
WATER_BLOCK_1 = 2
WATER_BLOCK_2 = 3
TREE_1 = 4
ROCK_1 = 5
LOG = 6
STONE = 7
PLANK = 8
STICK = 9
PLAYER_1 = 16
PLAYER_2 = 17
PLAYER_3 = 18
PLAYER_RIGHT_1 = 20
PLAYER_RIGHT_2 = 21
PLAYER_RIGHT_3 = 22
PLAYER_LEFT_1 = 23
PLAYER_LEFT_2 = 24
PLAYER_LEFT_3 = 25
PLAYER_UP_1 = 26
PLAYER_UP_2 = 27
PLAYER_UP_3 = 28
AXE = 32
PICAXE = 33
STONE_AXE = 34
STONE_PICKAXE = 35
CRAFTING_TABLE = 48

UI_HOTBAR_ITEM = 0
UI_HOTBAR_ITEM_DARK = 1
UI_INVENTORY_ITEM = 2
UI_INVENTORY_ITEM_DARK = 3

BLOCK_DROPS = {
    "TREE_1": LOG,
    "ROCK_1": STONE,
    "CRAFTING_TABLE": CRAFTING_TABLE,
    TREE_1: LOG,
    ROCK_1: STONE,
    CRAFTING_TABLE: CRAFTING_TABLE
}

BLOCK_PLACABLE = [
    CRAFTING_TABLE
]

BLOCK_COLLIDABLE = [
    TREE_1,
    ROCK_1,
    CRAFTING_TABLE
]

BACKGROUND_BLOCKS = [
    GRASS_BLOCK,
    SAND_BLOCK
]

ITEM_ID = {
    LOG: "LOG",
    STONE: "STONE",
    PLANK: "PLANK",
    STICK: "STICK"
}