import common
from view import images
from model import characters
from controller import town


# TODO: Add Dropping Items from Monsters
# TODO: Add Leveling Up
# TODO: Fix all the broken 'views'


# Main function that starts the game.
def main():

    common.clear_screen()
    print(images.game_title)
    print(images.dragon)
    print(common.border)
    print("  Welcome brave warrior to the small town of Dragonsville!  We ")
    print("  thought we had a clever name until an actual dragon moved into town.")
    print("  He took over the lowest level of our local dungeons. Now a whole")
    print("  host of monsters have made it their home.  Will you be defeating ")
    print("  the dragon?  It sure would be helpful... although no one ever ")
    print("  comes out of there alive...")
    print(common.border)

    our_hero = common.load_hero()

    if our_hero is None:
        name = input("What can we call you, hero? ")
        our_hero = characters.Character(characters.warrior)
        our_hero.name = name
    else:
        input("Welcome back, %s! We have been waiting for you!" % our_hero.name)

    town.walk_through_the_town(our_hero)


if __name__ == "__main__":
    main()
