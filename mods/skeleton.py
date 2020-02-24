import random
import model.items

object_definition = {
    "name": "Skeleton",
    "type": "monster",
    "level": 8,
    "image": "skeleton.txt",
    "hit_points": random.randint(5, 15),
    "gold": random.randint(15, 25),
    "weapon": model.items.fists_and_feet
}