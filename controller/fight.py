import sys
import common
from view import screen, images

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
            message = our_hero.attack(monster)
            if monster.is_alive():
                message = message + '\n ' + monster.attack(our_hero)
                if not our_hero.is_alive():
                    message = message + '\n ' + "You have been Slain! Better luck in your next life!"
                    hero_is_slain(our_hero, view, message)
            else:
                # Grab Gold from now dead monster
                our_hero.gold += monster.gold
                right_center_pane = images.treasure_chest
                message = message + " Digging through the %s remains you found %d gold!" % (monster.name, monster.gold)
                commands = "Press Enter to continue..."
                if monster.name == "Red Dragon":
                    our_hero.killed_dragon = True
                    message += " You have vanquished the dragon!!! You will be if you get out alive!"

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
