from view import screen, images
import common
from model import items

commands = "Enter a (#) to purchase an item, (S)ell an item, or (L)eave Shop"
border = "<====================<o>====================>\n"
starter_message = "Welcome to Bill's Equipment Emporium, mighty warrior!  Would you like to upgrade your shoddy " \
              "equipment?"


# This function controls our interactions at the weapons store
def enter_the_shop(our_hero):
    is_leaving_the_shop = False
    message = starter_message
    left_pane = images.weapons_shop_logo
    right_pane = draw_buy_list()

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
        elif next_move.lower() == 's':
            sell_items(our_hero)
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


def sell_items(our_hero):
    is_done_selling = False
    message = "Wonderful, we have been running low on good hardware!  What are you " \
              "willing to part with? "
    left_pane = images.weapons_shop_logo
    commands_pane = "Enter a (#) to sell an item, or (L)eave."

    while not is_done_selling:
        screen.paint(
            common.get_stats(None, our_hero),
            commands_pane,
            message,
            left_pane,
            draw_sell_list(our_hero)
        )
        next_move = input("Next? ")
        if next_move.lower() == 'l':
            is_done_selling = True
        elif next_move.isdigit():
            item_number_picked = int(next_move)
            items_list = filtered_sell_list(our_hero)
            if item_number_picked > len(items_list)-1 or item_number_picked < 0:
                message = "You do not have an item of that number!"
            else:
                selected_item = items_list[item_number_picked][4]
                selected_item_quantity = items_list[item_number_picked][0]
                if selected_item["type"] == "weapon" or selected_item["type"] == "armor" or selected_item["type"] == "shield":
                    if selected_item["name"] == our_hero.equipped_weapon["name"] and selected_item_quantity == 1:
                        message = "You cannot sell equipped items!"
                    elif our_hero.equipped_armor is not None and selected_item["name"] == our_hero.equipped_armor["name"] and selected_item_quantity == 1:
                        message = "You cannot sell equipped items!"
                    elif our_hero.equipped_shield is not None and selected_item["name"] == our_hero.equipped_shield["name"] and selected_item_quantity == 1:
                        message = "You cannot sell equipped items!"
                    else:
                        our_hero.gold += selected_item["cost"] / 2
                        our_hero.inventory.remove(selected_item)
                        message = "You sold %s for %d gold." % (selected_item["name"], selected_item["cost"]/2)
                else:
                    message = "You cannot sell that item here!"
        elif next_move.lower() == 'n':
            commands_pane = commands
            message = starter_message


def draw_buy_list():
    response = border
    response += "  # | Item         | Type   | Dmg | Cost " + '\n'
    response += border
    for number, e in enumerate(items.equipment_list):
        response += common.front_padding(str(number), 3) + " | " \
                    + common.back_padding(e["name"], 12) + " | " \
                    + common.front_padding(str(e["type"]), 6) + " | " \
                    + common.front_padding(str(e["damage"]), 3) + " | " \
                    + common.front_padding(str(round(e["cost"])), 4) + '\n'
    response += border
    return response


def draw_sell_list(our_hero):
    items = filtered_sell_list(our_hero)
    response = border
    response += "  # | Items            | Type   | Value " + '\n'
    response += border
    for num, item in enumerate(items):
        response += common.front_padding(str(num), 3) + " | " \
                    + common.back_padding(str(item[0]) + " " + item[1], 16) + " | " \
                    + common.front_padding(str(item[2]), 6) + " | " \
                    + common.front_padding(str(round(item[3]/2)), 4) + '\n'
    response += border
    return response


# Create a Filtered list of only items we can sell in the equipment shop
def filtered_sell_list(our_hero):
    filtered_list = []
    items_list = common.collapse_inventory_items(our_hero)
    for item in items_list:
        if item[2] == "weapon" or item[2] == "shield" or item[2] == "armor":
            filtered_list.append(item)

    return filtered_list
