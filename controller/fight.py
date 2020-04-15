import sys
import common
import readchar
import random
import logging
from model import enchantments
from view import screen, images

log = logging.getLogger('dragonsville')
fight_commands = "(F)ight, (U)se item, (R)un away!"
screen_state = screen.State(None, None, None, None, None)


# This Function is to attack a monster. This includes the loop to continue to attack until someone dies, or our hero
# runs away.
def fight_a_monster(our_hero, monster, view):
    is_attack_finished = False
    screen_state.left_pane = view.generate_perspective()
    screen_state.right_pane = monster.image
    screen_state.messages = "A %s stands before you, blocking your path!" % monster.name
    screen_state.commands = fight_commands
    while not is_attack_finished:
        screen_state.stats = common.get_stats(view, our_hero)
        screen.paint(screen_state)
        next_move = readchar.readkey()
        if next_move.lower() == "f":
            screen_state.messages = our_hero.attack(monster)
            is_attack_finished = finish_attack(our_hero, monster, view)
            if is_attack_finished:
                screen_state.commands = "Press Enter to continue..."
        if next_move.lower() == "u":
            screen_state.messages = use_item(our_hero, view, monster)
            is_attack_finished = finish_attack(our_hero, monster, view)
            if is_attack_finished:
                screen_state.commands = "Press Enter to continue..."
        # Run Away
        if next_move.lower() == "r":
            # The monster gets one last parting shot as you flee.
            screen_state.messages = monster.attack(our_hero)
            if not our_hero.is_alive():
                hero_is_slain(our_hero, monster, screen_state, view)
            screen_state.messages += '\n ' + "You run as fast as your little legs will carry you and get away..."
            is_attack_finished = True

    # Attack is finished, paint results screen and pause
    screen.paint(screen_state)
    input("")


# Function to be called after attacking a monster or using a magical item.
def finish_attack(our_hero, monster, view):
    if monster.is_alive():
        screen_state.messages += '\n ' + monster.attack(our_hero)
        if not our_hero.is_alive():
            hero_is_slain(our_hero, monster, screen_state, view)
        return False
    else:
        # Monster has been killed
        if monster.name == "Red Dragon":
            dragon_killed(our_hero)
        # Grab Gold
        our_hero.gold += monster.gold
        screen_state.right_pane = images.treasure_chest
        # Check to see if the monster drops it's weapon. If so, put it in the hero's inventory.
        drop_weapon = random.randint(0, 3)
        if drop_weapon == 0:
            our_hero.inventory.append(monster.weapon)
            screen_state.messages += " The monster has dropped " + monster.weapon["name"] + "!"
        screen_state.messages += " Digging through the %s remains you found %d gold!" % (monster.name, monster.gold)
        return True


# Function to pick which magical item should be used.
def use_item(our_hero, view, monster):
    screen.paint(screen.State(
        common.get_stats(None, our_hero),
        "Enter a (#) to use an item, or (C)ancel.",
        "Use which item?",
        view.generate_perspective(),
        draw_use_list(our_hero)
    ))
    next_move = input("Next? ")
    if next_move.lower() == 'c':
        return "You wasted your time digging in your pack and the monster attacks you! "
    elif next_move.isdigit():
        item_number_picked = int(next_move)
        items_list = filtered_use_list(our_hero)
        if item_number_picked > len(items_list)-1 or item_number_picked < 0:
            return "You do not have an item of that number! You wasted your time digging in your pack and the " \
                      "monster attacks you! "
        else:
            selected_item = items_list[item_number_picked][4]
            return enchantments.use_item(selected_item, our_hero, monster)


# Function to draw a list of items to pick from.
def draw_use_list(our_hero):
    items = filtered_use_list(our_hero)
    response = common.medium_border + '\n'
    response += "  # | Items            | Type   | Value " + '\n'
    response = common.medium_border + '\n'
    for num, item in enumerate(items):
        response += common.front_padding(str(num), 3) + " | " \
                    + common.back_padding(str(item[0]) + " " + item[1], 16) + " | " \
                    + common.front_padding(str(item[2]), 6) + " | " \
                    + common.front_padding(str(round(item[3]/2)), 4) + '\n'
    response += common.medium_border
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
def hero_is_slain(our_hero, monster, screen_state, view):
    # Too Cruel, and less fun. Reset the character to a beat up state back in the town.
    # common.delete_hero()  # Delete our Hero file so we have to create a new hero
    # common.delete_dungeons()  # Reset the dungeons so we have to learn new dungeons with our new hero
    screen_state.stats = common.get_stats(view, our_hero)
    screen_state.messages += '\n ' + "You have been Slain! ... or have you?  You come too and the %s is gone, " \
                                        "with most of your gold.  You somehow crawl out of the dungeon..." % \
                      monster.name
    screen_state.commands = "restart the game"
    screen_state.left_pane = view.generate_perspective()
    screen_state.right_pane = images.death

    our_hero.hit_points = 4
    if our_hero.gold > 10:
        our_hero.gold = 4
    common.save_hero(our_hero)
    screen.paint(screen_state)
    sys.exit()


# routine to run if your hero kills the dragon
def dragon_killed(our_hero):
    common.save_hero(our_hero)  # Save our Hero file so they can continue to play with the hero if they want
    print(images.castle)
    print("You have slain the dragon!!! The village rejoices, the dungeons slowly empty of monsters and return ")
    print("to the profitable gold mines they once were.  You are made king over all the local lands and reign for")
    print("many peaceful years.  Congratulations $s!!!")
    sys.exit()
