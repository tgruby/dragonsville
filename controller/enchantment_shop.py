from view import screen, images
import common
from model import enchantments

commands = "Enter a (#) to purchase an item, (L)eave Shop"


# TODO: Create Potions from monster parts to affect the hero
# TODO: Create Scrolls from monster parts for casting spells to affect monsters
# TODO: Create weapons and equipment enchantments from monster parts to enhance their abilities

# This function controls our interactions at the weapons store
def enter_the_shop(our_hero):
    is_leaving_the_shop = False
    message = "Welcome to Janet's Enchantments!  Would you like me to use some of your monster " \
              "'treasures' to make you potent elixir for your journeys?"
    left_pane = images.shop
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
            # Change this to enchantment objects
            if item_number_picked < len(enchantments.all_enchantments):
                item = enchantments.all_enchantments[item_number_picked]
                if our_hero.gold < item["cost"]:
                    message = "You don't have enough money for that!"
                else:
                    our_hero.gold -= item["cost"]
                    # TODO: This is where we need to add logic to take away monster parts from our hero, and give
                    #  them the enchanted item.
                    our_hero.inventory.append(item)
                    message = "You have purchased the %s." % item["name"]
            else:
                message = "There is no item of that number!"


def draw_list():
    # TODO: This entire list needs to be updated
    border = "<====================<o>====================>\n"
    response = border
    response += "  # | Item         | Type   | Dmg | Cost " + '\n'
    response += border
    for number, e in enumerate(enchantments.all_enchantments):
        response += common.front_padding(str(number), 3) + " | " \
                    + common.back_padding(e["name"], 12) + " | " \
                    + common.front_padding(str(e["type"]), 6) + " | " \
                    + common.front_padding(str(e["damage"]), 3) + " | " \
                    + common.front_padding(str(e["cost"]), 4) + '\n'
    response += border
    return response
