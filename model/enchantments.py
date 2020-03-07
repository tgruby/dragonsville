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
    "name": "Health Potion",
    "descripton": "This potion will heal the drinker.",
    "type": "potion",
    "max_hit_points": 30,
    "cost": 10
}

all_enchantments = [
    health_potion
]
