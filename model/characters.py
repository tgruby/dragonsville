import random
from model import items


class DungeonLocation:

    def __init__(self, dungeon_id, x, y):
        self.dungeon = dungeon_id
        self.x = x
        self.y = y


class Character:
    # Global Class Variables

    # Character Constructor (for our hero)
    def __init__(self, character_definition):
        self.name = character_definition["name"]
        self.image = character_definition["image"]
        self.type = character_definition["type"]
        self.race = character_definition["race"]
        self.max_hit_points = random.randint(12, character_definition["hit_points"])
        self.hit_points = self.max_hit_points
        self.experience_points = character_definition["experience_points"]
        self.level = 1
        self.gold = character_definition["gold"]
        self.equipped_weapon = character_definition["equipped_weapon"]
        self.equipped_armor = character_definition["equipped_armor"]
        self.equipped_shield = character_definition["equipped_shield"]
        self.inventory = character_definition["inventory"]
        self.location = None

    # Return True if the character is alive, False if not.
    def is_alive(self):
        return self.hit_points > 0

    # Function that processes an attack of any character on another character
    def attack(self, monster):
        weapon = self.equipped_weapon
        damage = random.randint(0, weapon["damage"])
        monster.hit_points -= damage
        message = weapon["attack_message"] % (self.name, damage)
        if not monster.is_alive():
            #  We killed the monster.  Add experience points to our hero
            self.experience_points += monster.level
            message += " You have killed the %s!" % monster.name
            if self.experience_points > (self.level * 30):  # level x 30 = next level
                # We have leveled up!  add additional hit points
                addl_hit_points = random.randint(4, 8)
                self.max_hit_points\
                    += addl_hit_points
                self.hit_points += addl_hit_points
                self.level += 1
                message += " You have gained enough experience to level up to level %d!" % self.level
        return message


warrior = {
    "name": None,
    "type": "warrior",
    "race": "human",
    "image": None,
    "hit_points": 20,
    "experience_points": 0,
    "gold": random.randint(10, 20),
    "equipped_weapon": items.dagger,
    "equipped_armor": None,
    "equipped_shield": None,
    "inventory": [items.dagger],
    "experience_levels": 25,
    "level_up_hit_points": 15
}
