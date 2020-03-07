import os
import pickle
import logging
from view import screen

# These borders are used throughout the game
border = "<=================================<>=================================>"
medium_border = "<=====================<>====================>"
short_border = "<========<>========>"
log = logging.getLogger('dragonsville')


# This helper function checks which type of computer we are on and calls the correct clear screen command.
def clear_screen():
    if os.name == "posix":
        os.system('clear')  # Running on MacOS System
    else:
        os.system('cls')  # Assume on Windows System


# This function saves our hero as he/she exists right now.
def save_hero(our_hero):
    save('our_hero', our_hero)


# This helper function is to save our hero to a "pickle" file, python's standard way to save objects to a file.
def load_hero():
    return load('our_hero')


# This function will be called when our hero is killed.  That means you can't play him/her again after death!
def delete_hero():
    delete("our_hero")


# This helper function is to save our hero to a "pickle" file, python's standard way to save objects to a file.
def load_dungeons():
    return load('dungeons')


# This function will be called when our hero is killed.  That means you can't play the same dungeons again after death!
def delete_dungeons():
    delete("dungeons")


# This function saves our hero as he/she exists right now.
def save(name, my_object):
    # Open the file
    with open(name + '.pkl', 'wb') as save_file:
        # dump our_hero structure into the pickle file
        pickle.dump(my_object, save_file)


# This helper function is to save an object to a "pickle" file, python's standard way to save objects to a file.
def load(name):
    try:
        # Open a File
        with open(name + '.pkl', 'rb') as load_file:
            # Load our_hero from the file (instead of creating a new one.
            my_object = pickle.load(load_file)
            # After the hero is read from file, return it so we can use him
            return my_object
    except IOError:
        # We failed to load the hero from the file.  In this case, just create a new hero.
        return None


# This function will be called when our hero is killed.  That means you can't play him/her again after death!
def delete(name):
    os.remove(name + '.pkl')


def get_stats(view, our_hero):
    if not our_hero.is_alive():
        return "*** YOU ARE DEAD ***"
    else:
        response = "Health: %d, Gold: %d, Weapon: %s" % (
            our_hero.hit_points, our_hero.gold, our_hero.equipped_weapon["name"])
        if view:
            response += ", Facing: " + view.get_direction()
        return response


# Create a string with spaces that take the offset of the string.
def padding(text, length):
    delta = length - len(text)
    buff = ''
    for x in range(delta):
        buff += ' '
    return buff


# put spaces in front of the text supplied.  So if the text is 4 char long and you want a 10 char long message,
# it will return a string with 6 spaces and 4 chars.
# For example: 'food' -> '      food'
def front_padding(text, length):
    return padding(text, length) + text


# put spaces in back of the text supplied.  So if the text is 4 char long and you want a 10 char long message,
# it will return a string with 4 chars and 6 spaces.
# For example: 'food' -> 'food      '
def back_padding(text, length):
    return text + padding(text, length)


# List out the various healing that our hero can have
def list_inventory(our_hero):
    response = screen.border(our_hero.name + "'s Inventory", 43) + '\n'
    response += "  Equipped Items:\n"
    response += "    Weapon..... %s (%d)\n" % (our_hero.equipped_weapon['name'], our_hero.equipped_weapon['damage'])
    if our_hero.equipped_armor is not None:
        response += "    Armor...... %s (%d)\n" % (our_hero.equipped_armor['name'], our_hero.equipped_armor['damage'])
    if our_hero.equipped_shield is not None:
        response += "    Shield..... %s (%d)\n" % (our_hero.equipped_shield['name'], our_hero.equipped_shield['damage'])
    response += medium_border + '\n'
    response += "  Inventory Items:\n"

    collapsed_items = collapse_inventory_items(our_hero)

    # List the items on the screen
    for num, i in enumerate(collapsed_items):
        response += "    %d. %d %s" % (num+1, i[0], i[1])
        response += '\n'
    response += medium_border
    return response


# Create a list of items in the inventory, with one item per item type and a count of items.
def collapse_inventory_items(our_hero):
    # Create Collections for each item (and count up the number of each that we have):
    collapsed_items = []
    for item in our_hero.inventory:
        item_found = False
        for collapsed_item in collapsed_items:
            if collapsed_item[1] == item["name"]:
                collapsed_item[0] += 1  # Increment Count
                item_found = True
        if not item_found:
            collapsed_item = [1, item["name"], item["type"], item]
            collapsed_items.append(collapsed_item)

    return collapsed_items
