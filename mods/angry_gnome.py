import random
import model.items

object_definition = {
    "name": "Angry Gnome",
    "type": "monster",
    "level": 5,
    "image": "angry_gnome.txt",
    "hit_points": random.randint(5, 10),
    "gold": random.randint(8, 18),
    "weapon": model.items.fists_and_feet
}