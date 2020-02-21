import random
from view import images
from model import items


# Class object to represent any active monster
class Monster:
    # Class Level Variables

    # Monster Constructor
    def __init__(self, monster_definition):
        self.name = monster_definition["name"]
        self.image = monster_definition["image"]
        self.hit_points = monster_definition["hit_points"]
        self.gold = monster_definition["gold"]
        self.weapon = monster_definition["weapon"]

    # Method to call when the monster attacks a character
    def attack(self, character):
        # Calculate Damage Inflicted
        weapon = self.weapon
        damage = random.randint(0, weapon["damage"])
        # Calculate Damage prevented by protection
        protection = 0
        if character.equipped_armor is not None:
            protection += random.randint(0, -character.equipped_armor["damage"])
        if character.equipped_shield is not None:
            protection += random.randint(0, -character.equipped_shield["damage"])
        damage = damage - protection
        # Prevent damage from being negative (healing the hero)
        if damage < 0:
            damage = 0
        # Subtract the damage from our hero's hit points
        character.hit_points -= damage
        return "The " + weapon["attack_message"] % (self.name, damage)

    def is_alive(self):
        return self.hit_points > 0


# Dictionaries of all Monsters in the Game
angry_gnome = {
    "name": "Angry Gnome",
    "type": "monster",
    "image": images.gnome,
    "hit_points": random.randint(5, 10),
    "gold": random.randint(8, 18),
    "weapon": items.fists_and_feet
}

skeleton = {
    "name": "Skeleton",
    "type": "monster",
    "image": images.skeleton,
    "hit_points": random.randint(5, 15),
    "gold": random.randint(15, 25),
    "weapon": items.fists_and_feet
}

skeleton_warrior = {
    "name": "Skeleton Warrior",
    "type": "monster",
    "image": images.skeleton_warrior,
    "hit_points": random.randint(20, 35),
    "gold": random.randint(25, 45),
    "weapon": items.battle_axe
}

giant_ant = {
    "name": "Giant Ant",
    "type": "monster",
    "image": images.giant_ant,
    "hit_points": random.randint(5, 10),
    "gold": random.randint(8, 12),
    "weapon": items.pincers
}

banshee = {
    "name": "Banshee",
    "type": "monster",
    "image": images.banshee,
    "hit_points": random.randint(10, 60),
    "gold": random.randint(20, 80),
    "weapon": items.scream
}

half_orc = {
    "name": "Half Orc",
    "type": "monster",
    "image": images.half_orc,
    "hit_points": random.randint(10, 50),
    "gold": random.randint(25, 75),
    "weapon": items.battle_axe
}

minotaur = {
    "name": "Minotaur",
    "type": "monster",
    "image": images.minotaur,
    "hit_points": random.randint(40, 100),
    "gold": random.randint(20, 150),
    "weapon": items.battle_axe
}

giant_spider = {
    "name": "Giant Spider",
    "type": "monster",
    "image": images.giant_spider,
    "hit_points": random.randint(5, 15),
    "gold": random.randint(4, 10),
    "weapon": items.fangs
}

vampire_bat_swarm = {
    "name": "Vampire Bat Swarm",
    "type": "monster",
    "image": images.vampire_bat,
    "hit_points": random.randint(5, 15),
    "gold": random.randint(0, 10),
    "weapon": items.fangs
}

goblin = {
    "name": "Goblin",
    "type": "monster",
    "image": images.goblin,
    "hit_points": random.randint(5, 20),
    "gold": random.randint(8, 22),
    "weapon": items.club
}

swarm_of_bees = {
    "name": "Swarm of Bees",
    "type": "monster",
    "image": images.swarm_of_bees,
    "hit_points": random.randint(5, 20),
    "gold": random.randint(0, 5),
    "weapon": items.stingers
}

wolf = {
    "name": "Wolf",
    "type": "monster",
    "image": images.wolf,
    "hit_points": random.randint(5, 25),
    "gold": random.randint(5, 10),
    "weapon": items.teeth
}

badger = {
    "name": "Badger",
    "type": "monster",
    "image": images.badger,
    "hit_points": random.randint(5, 15),
    "gold": random.randint(5, 15),
    "weapon": items.teeth
}

giant_rat = {
    "name": "Giant Rat",
    "type": "monster",
    "image": images.rat,
    "hit_points": random.randint(5, 10),
    "gold": random.randint(5, 10),
    "weapon": items.teeth
}

red_dragon = {
    "name": "Red Dragon",
    "type": "monster",
    "image": images.dragon,
    "hit_points": random.randint(1000, 1000),
    "gold": random.randint(500, 2000),
    "weapon": items.fireball
}

dungeon_0 = [
    giant_rat,
    wolf,
    swarm_of_bees,
    giant_ant,
    giant_spider
]

dungeon_1 = [
    angry_gnome,
    badger,
    skeleton,
    vampire_bat_swarm
]

dungeon_2 = [
    goblin,
    skeleton_warrior,
    half_orc
]

dungeon_3 = [
    banshee,
    minotaur
]

all_monsters = [
    dungeon_0,
    dungeon_1,
    dungeon_2,
    dungeon_3
]


# This Function is to decide which monster to spawn in a given dungeon.
def get_a_monster_for_dungeon(dungeon_id):
    monsters = []
    for index in range(dungeon_id + 1):
        for m in all_monsters[index]:
            monsters.append(m)
    monster_id = random.randint(0, len(monsters)-1)
    monster = Monster(monsters[monster_id])
    return monster
