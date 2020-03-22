import sys
import common
import random
import logging
from view import screen, images

log = logging.getLogger('dragonsville')
fight_commands = "(F)ight, (R)un away!"


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
        next_move = input("Next? ")
        if next_move.lower() == "f":
            log.info("%s has %d hit points before being attacked." % (monster.name, monster.hit_points))
            message = our_hero.attack(monster)
            log.info("%s has %d hit points after being attacked." % (monster.name, monster.hit_points))
            if monster.is_alive():
                message = message + '\n ' + monster.attack(our_hero)
                if not our_hero.is_alive():
                    message = message + '\n ' + "You have been Slain! Better luck in your next life!"
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


# routine to run if your hero is slain
def hero_is_slain(our_hero, view, message):
    common.delete_hero()  # Delete our Hero file so we have to create a new hero
    common.delete_dungeons()  # Reset the dungeons so we have to learn new dungeons with our new hero
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
