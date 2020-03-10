import common
import logging
from view import images
from model import characters
from controller import town

# TODO: Convert from ladders to up and down doorways.  Should simplify screen logic.
# TODO: Add Leveling up for characters
# TODO: Allow to create multiple characters
# TODO: Allow for multiple monster attacks at the same time
# TODO: Move Monsters+ to individual external files including level guides to allow for independent creation and loading
# TODO: Fix all the broken dungeon images
# TODO: Add doorways and rooms
# TODO: Add traps
# TODO: Add "guardians" that guard staircases going up and down
# TODO: Add the ability to "sense" coming up on monster guardians the square before.
# TODO: Move to web-based, so we can be more dynamic images than ascii art
# TODO: Add Alchemy Shop: exchange monster parts + gold for potions
# TODO: equip other items.


# Main function that starts the game.
def main():
    # Setup logging
    log = logging.getLogger('dragonsville')
    handler = logging.FileHandler('dragonsville.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)

    common.clear_screen()
    print(images.game_title)
    print(common.border)
    print("  Welcome brave warrior to the small town of Dragonsville!  We ")
    print("  thought we had a clever name until an actual dragon moved into town.")
    print("  He took over the lowest level of our local dungeons. Now a whole")
    print("  host of monsters have made it their home.  Will you be defeating ")
    print("  the dragon?  It sure would be helpful... although no one ever ")
    print("  comes out of there alive...")
    print(common.border)

    our_hero = common.load_hero()

    log.info("Finished Loading Splash Screen")
    if our_hero is None:
        name = input("What can we call you, hero? ")
        our_hero = characters.Character(characters.warrior)
        our_hero.name = name
    else:
        input("Welcome back, %s! We have been waiting for you!" % our_hero.name)

    town.walk_through_the_town(our_hero)


if __name__ == "__main__":
    main()
