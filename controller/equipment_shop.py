from view import screen, images
import common
from model import items

commands = "Enter a (#) to purchase an item, (L)eave Shop"


# This function controls our interactions at the weapons store
def enter_the_shop(our_hero):
    is_leaving_the_shop = False
    message = "Welcome to Bill's Equipment Emporium, mighty warrior!  Would you like to upgrade your shoddy " \
              "equipment?"
    left_pane = images.weapons_shop_logo
    right_pane = draw_list()

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
            item_number_picked = int(next_move)
            if item_number_picked < len(items.equipment_list):
                item = items.equipment_list[item_number_picked]
                if item in our_hero.inventory:
                    message = "You already own that item!"
                elif our_hero.gold < item["cost"]:
                    message = "You don't have enough money for that!"
                else:
                    our_hero.gold -= item["cost"]
                    if item["type"] == "weapon":
                        our_hero.equipped_weapon = item
                    elif item["type"] == "armor":
                        our_hero.equipped_armor = item
                    elif item["type"] == "shield":
                        our_hero.equipped_shield = item
                    our_hero.inventory.append(item)
                    message = "You have purchased the %s." % item["name"]
            else:
                message = "There is no weapon of that number!"


def draw_list():
    border = "<====================<o>====================>\n"
    response = border
    response += "  # | Item         | Type   | Dmg | Cost " + '\n'
    response += border
    for number, e in enumerate(items.equipment_list):
        response += common.front_padding(str(number), 3) + " | " \
                    + common.back_padding(e["name"], 12) + " | " \
                    + common.front_padding(str(e["type"]), 6) + " | " \
                    + common.front_padding(str(e["damage"]), 3) + " | " \
                    + common.front_padding(str(e["cost"]), 4) + '\n'
    response += border
    return response


