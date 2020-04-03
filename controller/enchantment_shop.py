from view import screen, images
import common
from model import enchantments

commands = "Enter a (#) to purchase an item, (S)ell an Item, (L)eave Shop"
starter_message = "Welcome to Janet's Enchantments!  Would you like me to use some of your monster " \
              "'treasures' to make you potent elixir for your journeys?"
border = "<====================<o>====================>\n"


# TODO: Create more Scrolls for casting spells to affect monsters

# This function controls our interactions at the weapons store
def enter_the_shop(our_hero):
    is_leaving_the_shop = False
    message = starter_message
    left_pane = images.shop
    right_pane = draw_purchase_list()
    commands_pane = commands
    item = None

    while not is_leaving_the_shop:
        screen.paint(
            common.get_stats(None, our_hero),
            commands_pane,
            message,
            left_pane,
            right_pane
        )
        next_move = input("Next? ")
        if next_move.lower() == 'l':
            is_leaving_the_shop = True
        if next_move.lower() == 's':
            sell_items(our_hero)
        elif next_move.isdigit():
            item_number_picked = int(next_move)
            if item_number_picked < len(enchantments.all_enchantments):
                item = enchantments.all_enchantments[item_number_picked]
                if our_hero.gold < item["cost"]:
                    message = "You don't have enough money for that!"
                else:
                    our_hero.gold -= item["cost"]
                    our_hero.inventory.append(item)
                    message = "You have purchased the %s." % item["name"]
                    commands_pane = commands


# This function controls our interactions at the weapons store
def sell_items(our_hero):
    is_done_selling = False
    message = "Wonderful, we have been running low on hard to get items for our spells and potions!  What are you " \
              "willing to part with? "
    left_pane = images.shop
    commands_pane = "Enter a (#) to sell an item, or go (L)eave."

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
                if selected_item["type"] == "loot":
                    our_hero.gold += selected_item["cost"]
                    our_hero.inventory.remove(selected_item)
                    message = "You sold %s for %d gold." % (selected_item["name"], selected_item["cost"])
                else:
                    message = "You cannot sell that item here!"
        elif next_move.lower() == 'n':
            commands_pane = commands
            message = starter_message


def draw_purchase_list():
    response = border
    response += "  # | Item                           | Cost " + '\n'
    response += border
    for number, e in enumerate(enchantments.all_enchantments):
        response += common.front_padding(str(number), 3) + " | " \
                    + common.back_padding(e["name"], 30) + " | " \
                    + common.front_padding(str(e["cost"]), 4) + '\n'
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
                    + common.front_padding(str(item[3]), 4) + '\n'
    response += border
    return response


# Create a Filtered list of only items we can sell in the enchantment shop
def filtered_sell_list(our_hero):
    filtered_list = []
    items_list = common.collapse_inventory_items(our_hero)
    for item in items_list:
        if item[2] == "loot":
            filtered_list.append(item)

    return filtered_list