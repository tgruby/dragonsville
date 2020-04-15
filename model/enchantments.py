import logging
import random

log = logging.getLogger('dragonsville')


# Method to call when the hero uses a magical item
def use_item(item, our_hero, monster):
    if item["type"] == "potion":
        healing = random.randint(10, item["max_hit_points"])
        our_hero.hit_points = our_hero.hit_points + healing
        our_hero.inventory.remove(item)
        return item["action_message"]
    elif item["type"] == "scroll":
        damage = random.randint(10, item["max_hit_points"])
        monster.hit_points = monster.hit_points - damage
        our_hero.inventory.remove(item)
        return item["action_message"] % (monster.name, damage)


# Dictionaries of all enchantments in the Game

health_potion = {
    "name": "Simple Healing Potion",
    "action_message": "You drink the potion and a fuzzy feeling washes over you.",
    "type": "potion",
    "max_hit_points": 25,
    "affects": "character",
    "cost": 50
}

gandalfs_granola = {
    "name": "Gandalf's Healing Granola",
    "action_message": "You munch on Gandalf's Granola and begin to grow a beard, like Gandolf!",
    "type": "potion",
    "max_hit_points": 100,
    "affects": "character",
    "cost": 100
}

earthquake_scroll = {
    "name": "Earthquake Scroll",
    "action_message": "As you read the scroll the ground starts shaking sending large stones crashing down onto the %s dealing %d damage! The scroll disintegrates and ashes fall to the ground. ",
    "type": "scroll",
    "max_hit_points": 200,
    "affects": "character",
    "cost": 200
}

lightning_scroll = {
    "name": "Lightning Scroll",
    "action_message": "As you read the scroll it glows a bright white and a lightning bolt shoots out of your hands, hitting the %s for %d damage! The scroll disintegrates and ashes fall to the ground.",
    "type": "scroll",
    "max_hit_points": 100,
    "affects": "character",
    "cost": 100
}

all_enchantments = [
    health_potion,
    gandalfs_granola,
    lightning_scroll,
    earthquake_scroll
]
