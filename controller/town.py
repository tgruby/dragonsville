import sys
import common
from view import screen, images
from controller import dungeon, cartography_shop, equipment_shop, temple, enchantment_shop

town_commands = "(E)quipment Shop, (M)agic Shop, (C)artographer, (T)emple, (D)ungeon, (L)eave Town"


# Function to navigate the town
def walk_through_the_town(our_hero):
    is_leaving_town = False
    message = "Welcome to the town of Dragonsville!"
    left_pane = images.small_village

    while not is_leaving_town:

        # Save our hero every time he/she enters the town.  This will capture coming back from the weapons shop,
        # the temple, or the dungeon.  This means a hero in the dungeon that doesn't come back doesn't get updated.
        common.save_hero(our_hero)

        right_pane = common.list_inventory(our_hero)
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
        # Quit Game
        if next_move.lower() == "l":
            sys.exit("You leave to the edge of town to rest."
                     "")
        # Visit the Magic shop
        if next_move.lower() == "m":
            enchantment_shop.enter_the_shop(our_hero)