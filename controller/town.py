import sys
import common
from view import screen, images
from controller import dungeon, cartography_shop, equipment_shop, temple, enchantment_shop

town_commands = "(E)quipment, (M)agic, (C)artographer, (T)emple, (D)ungeon, (Q)uit"
town_message = "Enter a shop... or the dungeon if you dare!"


# Function to navigate the town
def walk_through_the_town(our_hero):
    is_leaving_town = False
    left_pane = images.small_village

    while not is_leaving_town:

        # Save our hero every time he/she enters the town.  This will capture coming back from the weapons shop,
        # the temple, or the dungeon.  This means a hero in the dungeon that doesn't come back doesn't get updated.
        common.save_hero(our_hero)

        right_pane = common.list_inventory(our_hero)
        screen.paint(screen.State(
            common.get_stats(None, our_hero),
            town_commands,
            town_message,
            left_pane,
            right_pane)
        )
        next_move = input("Next? ")
        # Visit the Shop to buy stuff
        if next_move.lower() == "e":
            equipment_shop.enter_the_shop(our_hero)
        # Go into the Temple
        if next_move.lower() == "c":
            cartography_shop.enter_the_map_shop(our_hero)
        # Visit the Magic shop
        if next_move.lower() == "m":
            enchantment_shop.enter_the_shop(our_hero)
        # Go into the Temple
        if next_move.lower() == "t":
            temple.enter_the_temple(our_hero)
        # Enter Dungeon
        if next_move.lower() == "d":
            dungeon.enter_the_dungeon(our_hero)
        # Quit Game
        if next_move.lower() == "q":
            sys.exit("Come back soon, we need you!")


# Function to navigate the town
def init(our_hero):
    view = {
        "stats_pane": common.get_stats(None, our_hero),
        "messages_pane": town_message,
        "view_pane": None,
        "info_pane": common.list_inventory(our_hero),
        "commands_pane": town_commands
    }
    return view
