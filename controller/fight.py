import sys
import common
import readchar
import random
import logging
from view import screen, images

log = logging.getLogger('dragonsville')
fight_commands = "(F)ight, (U)se item, (R)un away!"
border = "<====================<o>====================>\n"

# This Function is to attack a monster. This includes the loop to continue to attack until someone dies, or our hero
# runs away.
def fight_a_monster(our_hero, monster, view):
    is_attack_finished = False
    message = "A " + monster.name + " stands before you, blocking your path!"
    right_center_pane = monster.image
    commands = fight_commands
    while not is_attack_finished:
        screen.paint(
            common.get_stats(view, our_hero),

            commands,
            message,
            view.generate_perspective(),
            right_center_pane
        )
        if not our_hero.is_alive():
            sys.exit()
        next_move = readchar.readkey()
        if next_move.lower() == "f":
            log.info("%s has %d hit points before being attacked." % (monster.name, monster.hit_points))
            message = our_hero.attack(monster)
            log.info("%s has %d hit points after being attacked." % (monster.name, monster.hit_points))
            if monster.is_alive():
                message = message + '\n ' + monster.attack(our_hero)
                if not our_hero.is_alive():
                    message = message + '\n ' + "You have been Slain! ... or have you?  You come too and the %s is gone, with most of your gold.  You somehow crawl out of the dungeon..." % monster.name
                    hero_is_slain(our_hero, view, message)
            else:
                # Monster has been killed
                if monster.name == "Red Dragon":
                      dragon_killed(our_hero)
                # Grab Gold
                our_hero.gold += monster.gold
                right_center_pane = images.treasure_chest
                # Check to see if the monster drops it's weapon. If so, put it in the hero's inventory.
                drop_weapon = random.randint(0, 3)
                if drop_weapon == 0:
                    our_hero.inventory.append(monster.weapon)
                    message = message + " The monster has dropped " + monster.weapon["name"] + "!"
                message = message + " Digging through the %s remains you found %d gold!" % (monster.name, monster.gold)
                commands = "Press Enter to continue..."
                is_attack_finished = True
        if next_move.lower() == "u":
            use_item(our_hero, view, monster)
        # Run Away
        if next_move.lower() == "r":
            # The monster gets one last parting shot as you flee.
            message = monster.attack(our_hero)
            if not our_hero.is_alive():
                message = message + " You have been Slain! Better luck in your next life!"
                hero_is_slain(our_hero, view, message)
            message += '\n ' + "You run as fast as your little legs will carry you and get away..."
            is_attack_finished = True

    # Attack is finished, paint results screen and pause
    screen.paint(
        common.get_stats(view, our_hero),
        commands,
        message,
        view.generate_perspective(),
        right_center_pane
    )
    input("")


def use_item(our_hero, view, monster):
    is_done_using = False
    message = "Use which item?"
    left_pane = view.generate_perspective()
    commands_pane = "Enter a (#) to use an item, or (C)ancel."

    while not is_done_using:
        screen.paint(
            common.get_stats(None, our_hero),
            commands_pane,
            message,
            left_pane,
            draw_use_list(our_hero)
        )
        next_move = input("Next? ")
        if next_move.lower() == 'c':
            is_done_using = True
        elif next_move.isdigit():
            item_number_picked = int(next_move)
            items_list = filtered_use_list(our_hero)
            if item_number_picked > len(items_list)-1 or item_number_picked < 0:
                message = "You do not have an item of that number!"
            else:
                selected_item = items_list[item_number_picked][4]
                if selected_item["type"] == "scroll":
                    damage = random.randint(10,selected_item["max_hit_points"])
                    monster.hit_points = monster.hit_points - damage
                    our_hero.inventory.remove(selected_item)
                    message = selected_item["description"] % (monster.name, damage)
                elif selected_item["type"] == "potion":
                    healing = random.randint(10, selected_item["max_hit_points"])
                    our_hero.hit_points = our_hero.hit_points + healing
                    our_hero.inventory.remove(selected_item)
                    message = selected_item["description"]
                else:
                    message = "You cannot use that item here!"


def draw_use_list(our_hero):
    items = filtered_use_list(our_hero)
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
def filtered_use_list(our_hero):
    filtered_list = []
    items_list = common.collapse_inventory_items(our_hero)
    for item in items_list:
        if item[2] == "potion" or item[2] == "scroll":
            filtered_list.append(item)

    return filtered_list


# routine to run if your hero is slain
def hero_is_slain(our_hero, view, message):
    # Too Cruel, and less fun. Reset the character to a beat up state back in the town.
    # common.delete_hero()  # Delete our Hero file so we have to create a new hero
    # common.delete_dungeons()  # Reset the dungeons so we have to learn new dungeons with our new hero
    our_hero.hit_points = 4
    if our_hero.gold > 10:
        our_hero.gold = 4
    common.save_hero(our_hero)
    screen.paint(
        common.get_stats(view, our_hero),
        "restart the game",
        message,
        view.generate_perspective(),
        images.death
    )
    sys.exit()


# routine to run if your hero kills the dragon
def dragon_killed(our_hero):
    common.save_hero(our_hero)  # Save our Hero file so they can continue to play with the hero if they want
    print(images.castle)
    print("You have slain the dragon!!! The village rejoices, the dungeons slowly empty of monsters and return ")
    print("to the profitable gold mines they once were.  You are made king over all the local lands and reign for")
    print("many peaceful years.  Congratulations $s!!!")
    sys.exit()
