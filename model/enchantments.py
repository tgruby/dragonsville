import logging

log = logging.getLogger('dragonsville')


# Class object to represent any active monster
class EnchantedItem:
    # Class Level Variables

    # Monster Constructor
    def __init__(self, enchantment_type):
        self.name = enchantment_type["name"]
        self.description = enchantment_type["description"]
        self.type = enchantment_type["type"]
        self.hit_points = enchantment_type["max_hit_points"]
        self.gold = enchantment_type["cost"]

    # Method to call when the monster attacks a character
    def use_item(self, our_hero, monster):
        if self.type == "potion":
            pass
        elif self.type == "scroll":
            pass


# Dictionaries of all enchantments in the Game

health_potion = {
    "name": "Healing Potion",
    "description": "This potion will refresh you, making you feel ready for the next battle.",
    "type": "potion",
    "max_hit_points": 30,
    "affects": "character",
    "cost": 10
}

gandalfs_granola = {
    "name": "Gandalf's Granola",
    "description": "This Granola bar will make you feel young again, like Gandolf!",
    "type": "potion",
    "max_hit_points": 100,
    "affects": "character",
    "cost": 100
}

super_scroll= {
    "name": "Super Scroll",
    "description": "This Scroll, when read, creates a tiny tornato sending loose debris at frightening speeds into "
                   "your foe.",
    "type": "scroll",
    "max_hit_points": 500,
    "affects": "character",
    "cost": 1000
}

all_enchantments = [
    health_potion,
    gandalfs_granola,
    super_scroll
]
