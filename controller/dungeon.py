# The word "controller" in programming often is used to refer to parts of the program that control the flow of
# interactions between the user and the computer.  This is where we will put all of our controller code.

import common
import random
from view import physics, screen
from model import monsters
from controller import fight

# Commands
move_commands = "Left (A), Right (D), Forward (W), (U)p, Down (J), (I)nventory"


# This Function is to walk through the dungeon and display the results of moving through the dungeon on the screen. This
# continues to loop until we leave the dungeon.
def enter_the_dungeon(our_hero):
    # Instantiate a point of view object.  This will help us render the view of your character
    view = physics.PointOfView(0, physics.PointOfView.south, our_hero)
    message = "Welcome to the Dungeon!"
    next_move = None

    is_leaving_dungeon = False
    while not is_leaving_dungeon:
        left_pane = view.generate_perspective()
        if next_move != 'i':  # If the user has selected to see inventory, show that instead of the map.
            if has_map(our_hero, view.current_dungeon_id):
                right_pane = view.current_dungeon_map
            else:
                right_pane = "You have no map for Dungeon " + str(view.current_dungeon_id)

        screen.paint(
            common.get_stats(view, our_hero),
            move_commands,
            message,
            left_pane,
            right_pane
        )
        next_move = input("Next? ")
        # Turn Left
        if next_move.lower() == "a":
            message = view.turn_left()
        # Turn Right
        if next_move.lower() == "d":
            message = view.turn_right()
        # Step Forward
        if next_move.lower() == "w":
            message = view.step_forward()
            # Prevent "farming" by running into the wall right in front of the hero.
            if message != "You can't walk through walls!":
                # Test to see if we run into a skeleton
                run_into_a_monster = random.randint(1, 10)  # 10% spawn a monster
                if run_into_a_monster == 1:
                    # spawn a monster and go to battle!
                    monster = monsters.get_a_monster_for_dungeon(view.current_dungeon_id)
                    fight.fight_a_monster(our_hero, monster, view)
        # Go Up Ladder
        if next_move.lower() == "u":
            message = view.climb_up()
            if view.current_dungeon_id < 0:
                # we have left the dungeon_0, return
                is_leaving_dungeon = True
        # Go Down Ladder
        if next_move.lower() == "j":
            message = view.climb_down()
        # List Stats
        if next_move.lower() == "i":
            right_pane = common.list_inventory(our_hero)


# Determine if our hero has a map for this dungeon
def has_map(our_hero, dungeon_id):
    for i in our_hero.inventory:
        if "number" in i:
            if i["number"] == dungeon_id and i["type"] == "map":
                return True
    return False
