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
            print('Failed to load spritesheet:', filename)
            print(message)
        print("INFO: Spritesheet loaded correctly")
        

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
    

### GAME TEXTURES: 
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
CAMPFIRE_1 = 10
CAMPFIRE_2 = 11
CAMPFIRE_3 = 12
CAMPFIRE_4 = 13
BLOOD = 14
FIRE_TEXTURE = 15
PLAYER_1 = 16
PLAYER_2 = 17
PLAYER_3 = 18
PLAYER_RIGHT_1 = 19
PLAYER_RIGHT_2 = 20
PLAYER_RIGHT_3 = 21
PLAYER_LEFT_1 = 22
PLAYER_LEFT_2 = 23
PLAYER_LEFT_3 = 24
PLAYER_UP_1 = 25
PLAYER_UP_2 = 26
PLAYER_UP_3 = 27
COAL = 28
ROCK_IRON = 29
IRON_ORE = 30
CLAY = 31
AXE = 32
PICKAXE = 33
STONE_AXE = 34
STONE_PICKAXE = 35
SHOVEL = 36
GRASS_BLOCK_DUG = 37
BRICK = 38
BRICK_BLOCK = 39
BLUEBERRY = 40
STRAWBERRY = 41
IRON_INGOT = 42
GOLD_INGOT = 43
GOLD_NUGGET = 46
BANANA = 47
CRAFTING_TABLE = 48
PLANK_BLOCK = 49
PLANK_FLOOR = 50
DOOR_CLOSED = 51
DOOR_OPENED = 52
STAIRSET = 53
CAVE_DIRT = 54
CAVE_STONE_1 = 55
CAVE_STONE_2 = 56
CHEST_CLOSED = 57
CHEST_OPENED = 58
FLOWER_1 =  64
GRASS_1 = 65
GRASS_2 = 66
WHEAT_SEEDS = 67
TORCH = 68
BUSH = 69
ZOMBIE = 80
ZOMBIE_2 = 81
ZOMBIE_3 = 82
ZOMBIE_RIGHT_1 = 83
ZOMBIE_RIGHT_2 = 84
ZOMBIE_RIGHT_3 = 85
ZOMBIE_LEFT_1 = 86
ZOMBIE_LEFT_2 = 87
ZOMBIE_LEFT_3 = 88
ZOMBIE_UP_1 = 89
ZOMBIE_UP_2 = 90
ZOMBIE_UP_3 = 91

### UI SPRITESHEET: 
UI_HOTBAR_ITEM = 0
UI_HOTBAR_ITEM_DARK = 1
UI_INVENTORY_ITEM = 2
UI_INVENTORY_ITEM_DARK = 3
UI_HEART = 4
UI_XP_BAR = 5


### GLOBAL TEXTURE-RELATED DICTS AND LISTS:

FRUIT = [
    BANANA,
    STRAWBERRY,
    BLUEBERRY
]

FRUIT_HEALTH = {
    "BANANA": 2,
    "STRAWBERRY": 1,
    "BLUEBERRY": 1
}

TOOLS = [
    "AXE",
    "PICKAXE",
    "STONE_AXE",
    "STONE_PICKAXE",
    "SHOVEL"
]

BLOCK_BREAKING = {
    "ANY": ["GRASS_1", "GRASS_2", "FLOWER_1", "TORCH"],
    "AXE": ["TREE_1", "CRAFTING_TABLE", "PLANK_BLOCK", "PLANK_FLOOR", "DOOR_CLOSED", "CAMPFIRE_1"],
    "STONE_AXE": ["TREE_1", "CRAFTING_TABLE", "PLANK_BLOCK", "PLANK_FLOOR", "DOOR_CLOSED"],
    "STONE_PICKAXE": ["ROCK_1", "ROCK_IRON"],
    "PICKAXE": ["ROCK_1", "ROCK_IRON", "BRICK_BLOCK"]
}

TOOL_BREAK_CHANCE = {
    "PICKAXE": 0.999,
    "AXE": 0.999,
    "STONE_PICKAXE": 0.95,
    "STONE_AXE": 0.95,
    "SHOVEL": 0.999
}

WEAPON_DAMAGE = {
    "ANY": 1,
    "STONE_AXE": 1.5,
    "STONE_PICKAXE": 1.5,
    "AXE": 2.5,
    "PICKAXE": 2,
    "SHOVEL": 1.5
}

COOKABLE_ITEMS = [
    CLAY,
    IRON_ORE,
    GOLD_NUGGET
]

COOK_RESULT = {
    "CLAY": BRICK,
    "IRON_ORE": IRON_INGOT,
    "GOLD_NUGGET": GOLD_INGOT,
}

BLOCK_DROPS = {
    "TREE_1": [[LOG, 1, 5], [STICK, 0, 2]],
    "ROCK_1": [[STONE, 1, 3], [COAL, 0, 1]],
    "CRAFTING_TABLE": [[CRAFTING_TABLE, 1]],
    "PLANK_BLOCK": [[PLANK_BLOCK, 1]],
    "PLANK_FLOOR": [[PLANK_FLOOR, 1]],
    "DOOR_CLOSED": [[DOOR_CLOSED, 1]],
    "CAMPFIRE_1": [[CAMPFIRE_1, 1]],
    "ROCK_IRON": [[STONE, 1, 5], [IRON_ORE, 1, 3]],
    "GRASS_1": [[GRASS_1, 1], [WHEAT_SEEDS, 1, 3]],
    "GRASS_2": [[GRASS_2, 1], [WHEAT_SEEDS, 1, 3]],
    "FLOWER_1": [[FLOWER_1, 1]],
    "GRASS_BLOCK": [[CLAY, 1]]
}

BLOCK_PLACABLE = [
    CRAFTING_TABLE,
    PLANK_BLOCK,
    PLANK_FLOOR,
    DOOR_CLOSED,
    CAMPFIRE_1,
    GRASS_1,
    GRASS_2,
    FLOWER_1,
    TORCH,
    GRASS_BLOCK_DUG,
    BRICK_BLOCK
]

BLOCK_COLLIDABLE = [
    TREE_1,
    ROCK_1,
    CRAFTING_TABLE,
    PLANK_BLOCK,
    CAMPFIRE_1,
    ROCK_IRON,
    BRICK_BLOCK,
    CAVE_STONE_2
]

ENEMY_COLLIDABLE = [
    WATER_BLOCK_1,
    WATER_BLOCK_2
]

BACKGROUND_BLOCKS = [
    GRASS_BLOCK,
    SAND_BLOCK,
    PLANK_FLOOR,
    CAVE_DIRT
]

LIGHT_AFFECTED_BLOCKS = [
    GRASS_BLOCK,
    SAND_BLOCK,
    CAVE_DIRT,
    WATER_BLOCK_1,
    WATER_BLOCK_2,


]

SPECIAL_BLOCKS = [
    CAMPFIRE_1,
    TORCH
]

LIGHT_BLOCKS = [
    CAMPFIRE_1,
    TORCH
]

RANDOM_ZOMBIE_DROP = [
    GOLD_NUGGET,
    IRON_ORE,
    BANANA,
    None,
]

ITEM_ID = {
    TREE_1: "TREE_1",
    ROCK_1: "ROCK_1",
    CRAFTING_TABLE: "CRAFTING_TABLE",
    PLANK_BLOCK: "PLANK_BLOCK",
    PLANK_FLOOR: "PLANK_FLOOR",
    LOG: "LOG",
    STONE: "STONE",
    PLANK: "PLANK",
    STICK: "STICK",
    AXE: "AXE",
    PICKAXE: "PICKAXE",
    DOOR_CLOSED: "DOOR_CLOSED",
    DOOR_OPENED: "DOOR_OPENED",
    CAMPFIRE_1: "CAMPFIRE_1",
    ROCK_IRON: "ROCK_IRON",
    COAL: "COAL",
    IRON_ORE: "IRON_ORE",
    GRASS_1: "GRASS_1",
    GRASS_2: "GRASS_2",
    FLOWER_1: "FLOWER_1",
    GRASS_BLOCK: "GRASS_BLOCK",
    BRICK: "BRICK",
    BRICK_BLOCK: "BRICK_BLOCK",
    SAND_BLOCK: "SAND_BLOCK",
    WATER_BLOCK_1: "WATER_BLOCK_1",
    WATER_BLOCK_2: "WATER_BLOCK_2",
    BUSH: "BUSH",
    TORCH: "TORCH",
    WHEAT_SEEDS: "WHEAT_SEEDS",
    GRASS_2: "GRASS_2",
    GRASS_1: "GRASS_1",
    FLOWER_1: "FLOWER_1",
    GRASS_BLOCK_DUG: "GRASS_BLOCK_DUG",
    SHOVEL: "SHOVEL",
    STONE_PICKAXE: "STONE_PICKAXE",
    STONE_AXE: "STONE_AXE",
    CLAY: "CLAY",
    IRON_ORE: "IRON_ORE",
    BANANA: "BANANA",
    BLUEBERRY: "BLUEBERRY",
    STRAWBERRY: "STRAWBERRY",
    CAVE_DIRT: "CAVE_DIRT",
    CAVE_STONE_1: "CAVE_STONE_1",
    CAVE_STONE_2: "CAVE_STONE_2",
    IRON_ORE: "IRON_ORE",
    GOLD_NUGGET: "GOLD_NUGGET",
    IRON_INGOT: "IRON_INGOT",
    GOLD_INGOT: "GOLD_INGOT"
}

def ID_STR(id: int):
    try:
        if id in ITEM_ID:
            for item in ITEM_ID:
                if item == id:
                    return ITEM_ID[item]
    except KeyError:
        print(f"ERROR: KeyError occured whilst looking for ID: {id}. No existing item with that ID!")
        return None
