from view import screen, images
import common
import logging
import random

commands = "Enter a (#) to equip an item, or (C)lose Pack"
log = logging.getLogger('dragonsville')


# This function controls our interactions at the weapons store
def look_at_inventory(our_hero):
    is_done = False
    message = "You open you pack and check your inventory..."
    left_pane = images.backpack_small
    right_pane = common.list_inventory(our_hero)

    while not is_done:
        screen.paint(screen.State(
            common.get_stats(None, our_hero),
            commands,
            message,
            left_pane,
            right_pane
        ))
        next_move = input("Next? ")
        if next_move.lower() == 'c':
            is_done = True
        elif next_move.isdigit():
            item_number_picked = int(next_move)
            # Collapse Inventory Items returns a 2D Array with each element listed as [count, name, type, object]
            items_list = common.collapse_inventory_items(our_hero)
            if item_number_picked > len(items_list):
                message = "You do not have an item of that number!"
                continue
            selected_item = items_list[item_number_picked - 1][4]
            if selected_item["type"] == "weapon":
                our_hero.equipped_weapon = selected_item
                message = "You have equipped the %s." % selected_item["name"]
            elif selected_item["type"] == "armor":
                our_hero.equipped_armor = selected_item
                message = "You have equipped the %s." % selected_item["name"]
            elif selected_item["type"] == "shield":
                our_hero.equipped_shield = selected_item
                message = "You have equipped the %s." % selected_item["name"]
            elif selected_item["type"] == "potion":
                if our_hero.hit_points == our_hero.max_hit_points:
                    message = "You don't need that right now."
                else:
                    healing = random.randint(4, selected_item["max_hit_points"])
                    if our_hero.hit_points + healing > our_hero.max_hit_points:
                        our_hero.hit_points = our_hero.max_hit_points
                    else:
                        our_hero.hit_points += healing
                    our_hero.inventory.remove(selected_item)
                    message = "You drank the %s and a warm fuzzy feeling comes over you." % selected_item["name"]
            else:
                message = "You cannot equip that item!"
            right_pane = common.list_inventory(our_hero)
