from view import screen, images
import common
from model import maps

commands = "Enter a (#) to purchase an item, (L)eave Shop"


# This function controls our interactions at the weapons store
def enter_the_map_shop(our_hero):
    is_leaving_the_shop = False
    message = "Welcome to Tina's Cartography, mighty warrior! Would you like to buy a map of the dungeon? They are " \
              "incredibly useful, and many warriors died to produce them! "
    left_pane = images.scroll
    right_pane = draw_map_list()

    while not is_leaving_the_shop:
        screen.paint(
            common.get_stats(None, our_hero),
            commands,
            message,
            left_pane,
            right_pane
        )
        next_move = input("Next? ")
        if next_move.lower() == 'l':
            is_leaving_the_shop = True
        elif next_move.isdigit():
            number_picked = int(next_move)
            if number_picked < len(maps.map_list):
                m = maps.map_list[number_picked]
                if m in our_hero.inventory:
                    message = "You already own that map!"
                elif our_hero.gold < m["cost"]:
                    message = "You don't have enough money for that!"
                else:
                    our_hero.gold -= m["cost"]
                    our_hero.inventory.append(m)
                    message = "You have boughten the " + m["name"] + "!"
            else:
                message = "There is no map for that number!"


def draw_map_list():
    border = "<====================<o>====================>\n"
    response = border
    response += "  # | Item              | Cost " + '\n'
    response += border
    for number, m in enumerate(maps.map_list):
        response += common.front_padding(str(number), 3) + " | " \
                    + common.back_padding(m["name"], 17) + " | " \
                    + common.front_padding(str(m["cost"]), 4) + ' Gold\n'
    response += border
    return response
