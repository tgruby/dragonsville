import logging
import random
from view import images
from model import items

log = logging.getLogger('dragonsville')


# Class object to represent any active monster
class Monster:
    # Class Level Variables

    # Monster Constructor
    def __init__(self, monster_definition):
        self.name = monster_definition["name"]
        self.image = monster_definition["image"]
        self.hit_points = random.randint(5, monster_definition["max_hit_points"])
        self.gold = random.randint(0, monster_definition["max_gold"])
        self.weapon = monster_definition["weapon"]
        self.level = monster_definition["level"]

    # Method to call when the monster attacks a character
    def attack(self, character):
        # Calculate Damage Inflicted
        weapon = self.weapon
        damage = random.randint(0, weapon["damage"])
        # Calculate Damage prevented by protection
        protection = 0
        if character.equipped_armor is not None:
            protection += random.randint(4, -character.equipped_armor["damage"])
        if character.equipped_shield is not None:
            protection += random.randint(4, -character.equipped_shield["damage"])
        damage = damage - protection
        # Prevent damage from being negative (healing the hero)
        if damage < 0:
            damage = 0
        # Subtract the damage from our hero's hit points
        character.hit_points -= damage
        return "The " + weapon["attack_message"] % (self.name, damage)

    def is_alive(self):
        return self.hit_points > 0


# This Function is to decide which monster to spawn in a given dungeon.
def get_a_monster_for_dungeon(dungeon_id):
    if dungeon_id < 0:
        return None
    dungeon_monsters = []

    # Build a list of monsters that we could find in this dungeon
    monster_leveling = 10 + (dungeon_id * 10)
    log.info("Monster Leveling %d for Dungeon %d" % (monster_leveling, dungeon_id))
    for index in range(len(all_monsters)):
        if all_monsters[index]["level"] < monster_leveling:
            dungeon_monsters.append(all_monsters[index])
    # Select a monster appropriate for the level of this dungeon.
    monster_id = random.randint(0, len(dungeon_monsters) - 1)
    monster = Monster(dungeon_monsters[monster_id])
    log.info("Monster Selected: %s, Level: %d for Dungeon %d" % (monster.name, monster.level, dungeon_id))
    return monster


# Dictionaries of all Monsters in the Game

giant_rat = {
    "name": "Giant Rat",
    "type": "monster",
    "level": 3,
    "image": images.rat,
    "max_hit_points": 10,
    "max_gold": 10,
    "weapon": items.rat_teeth
}

angry_gnome = {
    "name": "Angry Gnome",
    "type": "monster",
    "level": 4,
    "image": images.gnome,
    "max_hit_points": 10,
    "max_gold": random.randint(8, 18),
    "weapon": items.gnome_feet
}

swarm_of_bees = {
    "name": "Swarm of Bees",
    "type": "monster",
    "level": 5,
    "image": images.swarm_of_bees,
    "max_hit_points": 20,
    "max_gold": 5,
    "weapon": items.bee_stinger
}

giant_ant = {
    "name": "Giant Ant",
    "type": "monster",
    "level": 6,
    "image": images.giant_ant,
    "max_hit_points": 10,
    "max_gold": 12,
    "weapon": items.ant_pincers
}

badger = {
    "name": "Badger",
    "type": "monster",
    "level": 7,
    "image": images.badger,
    "max_hit_points": 15,
    "max_gold": 15,
    "weapon": items.badger_teeth
}

giant_spider = {
    "name": "Giant Spider",
    "type": "monster",
    "level": 8,
    "image": images.giant_spider,
    "max_hit_points": 15,
    "max_gold": 10,
    "weapon": items.spider_fangs
}

wolf = {
    "name": "Wolf",
    "type": "monster",
    "level": 11,
    "image": images.wolf,
    "max_hit_points": 50,
    "max_gold": 10,
    "weapon": items.wolf_teeth
}

goblin = {
    "name": "Goblin",
    "type": "monster",
    "level": 12,
    "image": images.goblin,
    "max_hit_points": 40,
    "max_gold": 60,
    "weapon": items.broad_sword
}
skeleton = {
    "name": "Skeleton",
    "type": "monster",
    "level": 13,
    "image": images.skeleton,
    "max_hit_points": 75,
    "max_gold": 50,
    "weapon": items.bony_fingers
}

vampire_bat_swarm = {
    "name": "Vampire Bat Swarm",
    "type": "monster",
    "level": 14,
    "image": images.vampire_bat,
    "max_hit_points": 60,
    "max_gold": 45,
    "weapon": items.bat_fangs
}

skeleton_warrior = {
    "name": "Skeleton Warrior",
    "type": "monster",
    "level": 23,
    "image": images.skeleton_warrior,
    "max_hit_points": 150,
    "max_gold": 85,
    "weapon": items.elvin_sword
}

half_orc = {
    "name": "Half Orc",
    "type": "monster",
    "level": 28,
    "image": images.half_orc,
    "max_hit_points": 200,
    "max_gold": 200,
    "weapon": items.elvin_sword
}

banshee = {
    "name": "Banshee",
    "type": "monster",
    "level": 32,
    "image": images.banshee,
    "max_hit_points": 250,
    "max_gold": 250,
    "weapon": items.banshee_scream
}

minotaur = {
    "name": "Minotaur",
    "type": "monster",
    "level": 35,
    "image": images.minotaur,
    "max_hit_points": 350,
    "max_gold": 350,
    "weapon": items.dragonbane
}

red_dragon = {
    "name": "Red Dragon",
    "type": "monster",
    "level": 99,
    "image": images.dragon,
    "max_hit_points": 750,
    "max_gold": 2000,
    "weapon": items.fireball
}

all_monsters = [
    giant_rat,
    wolf,
    swarm_of_bees,
    giant_ant,
    giant_spider,
    angry_gnome,
    badger,
    skeleton,
    vampire_bat_swarm,
    goblin,
    skeleton_warrior,
    half_orc,
    banshee,
    minotaur
]
