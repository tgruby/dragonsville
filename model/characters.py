import random
from model import items


class Character:
    # Global Class Variables

    # Character Constructor (for our hero)
    def __init__(self, character_definition):
        self.name = character_definition["name"]
        self.image = character_definition["image"]
        self.type = character_definition["type"]
        self.race = character_definition["race"]
        self.hit_points = character_definition["hit_points"]
        self.gold = character_definition["gold"]
        self.equipped_weapon = character_definition["equipped_weapon"]
        self.equipped_armor = character_definition["equipped_armor"]
        self.equipped_shield = character_definition["equipped_shield"]
        self.inventory = character_definition["inventory"]
        self.killed_dragon = False

    # Return True if the character is alive, False if not.
    def is_alive(self):
        return self.hit_points > 0

    # Function that processes an attack of any character on another character
    def attack(self, monster):
        weapon = self.equipped_weapon
        damage = random.randint(0, weapon["damage"])
        monster.hit_points -= damage
        return weapon["attack_message"] % (self.name, damage)


warrior = {
    "name": None,
    "type": "warrior",
    "race": "human",
    "image": None,
    "hit_points": 100,
    "gold": random.randint(0, 5),
    "equipped_weapon": items.fists_and_feet,
    "equipped_armor": None,
    "equipped_shield": None,
    "inventory": []
}
