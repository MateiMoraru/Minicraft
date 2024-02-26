from spritesheet import *
from zombie import Zombie


class Commands:
    def __init__(self, main):
        self.main = main

    
    def process_command(self, command: str):
        try:
            command = command.split(' ')
        except Exception as e:
            print(f"ERROR: {e}. Passed empty string as command?")
            return

        if command[0] == "set":
            try:
                arg = command[1]
                value = int(command[2])
            except:
                print("ERROR: Excpected set <argument: str>, <value: int>")
                return
            if arg == "time":
                self.main.environment.time = value
                print(f"INFO: Set current time to {value}")
            elif arg == "player-health":
                print(f"INFO: Set player's health to {value}")
                self.main.environment.player.health = value
        elif command[0] == "give-player":
            try:
                block = int(command[1])
                amount = int(command[2])
            except:
                print("ERROR: Excpected set <block: int>, <amount: int>")
                return
            self.main.environment.player.inventory.add_item([block, amount])
            print(f"INFO: Added {ID_STR(block)} (amount: {amount}) to player's inventory")
        elif command[0] == "clear":
            try:
                target = command[1]
            except:
                print("ERROR: Expected target argument")
                return
            if target == "entities":
                self.main.environment.entities = [[], []]
                print(f"INFO: Cleared all the entities")
            elif target == "items":
                self.main.environment.ground_items = [[], []]
                print(f"INFO: Cleared all the ground items")
        elif command[0] == "spawn": ### TODO: Make it dynamic
            try:
                entity = command[1]
            except:
                print("ERROR: Expected entity name")
                return

            cave = self.main.environment.cave_level
            window = self.main.window
            spritesheet = self.main.spritesheet
            sfx = self.main.environment.sfx
            pos = self.main.environment.player.player.pos
            offset = self.main.environment.player.offset
            pos = [pos[0] + offset[0], pos[1] + offset[1]]
            size = self.main.environment.sprite_size
            texture_id = ZOMBIE
            name = "ZOMBIE"
            self.main.environment.entities[cave].append(Zombie(window, spritesheet, sfx, pos, size))
