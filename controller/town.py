import sys
import common
from view import screen, images
from controller import dungeon, cartography_shop, equipment_shop, temple

town_commands = "(E)quipment Shop, (C)artographer, (T)emple, (D)ungeon, (L)eave Town"


# Function to navigate the town
def walk_through_the_town(our_hero):
    is_leaving_town = False
    message = "Welcome to the town of Dragonsville!"
    left_pane = images.small_village

    while not is_leaving_town:

        # Save our hero every time he/she enters the town.  This will capture coming back from the weapons shop,
        # the temple, or the dungeon.  This means a hero in the dungeon that doesn't come back doesn't get updated.
        common.save_hero(our_hero)

        right_pane = draw_hero_stats(our_hero)
        screen.paint(
            common.get_stats(None, our_hero),
            town_commands,
            message,
            left_pane,
            right_pane
        )
        next_move = input("Next? ")
        # Visit the Shop to buy stuff
        if next_move.lower() == "e":
            equipment_shop.enter_the_shop(our_hero)
        # Go into the Temple
        if next_move.lower() == "c":
            cartography_shop.enter_the_map_shop(our_hero)
        # Go into the Temple
        if next_move.lower() == "t":
            temple.enter_the_temple(our_hero)
        # Enter Dungeon
        if next_move.lower() == "d":
            dungeon.enter_the_dungeon(our_hero)
        # Enter Dungeon
        if next_move.lower() == "z":
            # Hidden feature to find gold so we can test.  remove after testing.
            our_hero.gold += 100
            message = "You stumble over a bag of gold!"
        # Quit Game
        if next_move.lower() == "l":
            sys.exit("You leave town and trade the life of a hero for that of a peasant.")


# List out the various healing that our hero can have
def draw_hero_stats(our_hero):

    response = screen.border(our_hero.name + "'s Stats", 43) + '\n'
    response += "  Health..... %d\n" % our_hero.hit_points
    response += "  Gold....... %d\n" % our_hero.gold
    response += "  Weapon..... %s (%d)\n" % (our_hero.equipped_weapon['name'], our_hero.equipped_weapon['damage'])
    if our_hero.equipped_armor is not None:
        response += "  Armor...... %s (%d)\n" % (our_hero.equipped_armor['name'], our_hero.equipped_armor['damage'])
    if our_hero.equipped_shield is not None:
        response += "  Shield..... %s (%d)\n" % (our_hero.equipped_shield['name'], our_hero.equipped_shield['damage'])
    response += screen.border("o", 43) + '\n'
    response += "  Inventory Items:\n"
    for i in our_hero.inventory:
        response += "    " + i["type"] + ": " + i["name"]
        if "hit_point_adjustment" in i:
            response += "(" + i["hit_point_adjustment"] + ")"
        response += '\n'
    response += screen.border("o", 43)
    return response
