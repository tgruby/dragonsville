# The word "controller" in programming often is used to refer to parts of the program that control the flow of
# interactions between the user and the computer.  This is where we will put all of our controller code.

import common
import readchar
import random
from view import physics, screen, images
from model import monsters, items
from controller import inventory
from controller import fight

# Commands
move_commands = "Left (A), Right (D), Forward (W), (I)nventory"


# This Function is to walk through the dungeon and display the results of moving through the dungeon on the screen. This
# continues to loop until we leave the dungeon.
def enter_the_dungeon(our_hero):
    # Instantiate a point of view object.  This will help us render the view of your character
    view = physics.PointOfView(0, physics.PointOfView.east, our_hero)
    message = "Welcome to the Dungeon!"
    next_move = None

    is_leaving_dungeon = False
    while not is_leaving_dungeon:
        left_pane = view.generate_perspective()
        # Check to see if the character is in a dead-end.  If so, reward (first time only) them with a chest of gold.
        check_for_treasure(our_hero, left_pane, view)
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
        next_move = readchar.readkey()
        # Turn Left
        if next_move.lower() == "a":
            message = view.turn_left()
        # Turn Right
        if next_move.lower() == "d":
            message = view.turn_right()
        # Step Forward
        if next_move.lower() == "w":
            message = view.step_forward()
            if view.current_dungeon_id < 0:
                # we have left the dungeon_0, return
                is_leaving_dungeon = True
            # Prevent "farming" by running into the wall right in front of the hero.
            elif message != "You can't walk through walls!":
                # Test to see if we run into a skeleton
                run_into_a_monster = random.randint(1, 10)  # 10% spawn a monster
                if run_into_a_monster == 1:
                    # spawn a monster and go to battle!
                    monster = monsters.get_a_monster_for_dungeon(view.current_dungeon_id)
                    fight.fight_a_monster(our_hero, monster, view)
        # List Stats
        if next_move.lower() == "i":
            inventory.look_at_inventory(our_hero)


# Determine if our hero has a map for this dungeon
def has_map(our_hero, dungeon_id):
    for i in our_hero.inventory:
        if "number" in i:
            if i["number"] == dungeon_id and i["type"] == "map":
                return True
    return False


def check_for_treasure(our_hero, left_pane, view):
    if left_pane == getattr(images, "dungeon_WHW_WWW"):
        # Save picked_up_treasure to a pkl file so doesn't reset after a restart.
        collected_treasure = common.load("collected_treasure")
        if collected_treasure is None:
            collected_treasure = []
        location = str(view.current_dungeon_id) + '-' + str(view.current_x) + "-" + str(view.current_x)
        if location not in collected_treasure:
            collected_treasure.append(location)
            common.save("collected_treasure", collected_treasure)
            max_gold = (view.current_dungeon_id + 1) * 30
            min_gold = view.current_dungeon_id * 30
            treasure = random.randint(min_gold, max_gold)
            our_hero.gold += treasure
            right_center_pane = images.treasure_chest
            message = " You have found a treasure chest with %d gold in it!" % treasure
            # Check to see if there is a weapon in the treasure chest. If so, put it in the hero's inventory.
            drop_weapon = random.randint(0, 5)  # 17%
            if drop_weapon == 0:
                weapon = items.equipment_list[random.randint(0, len(items.equipment_list) - 1)]
                our_hero.inventory.append(weapon)
                message += " You find a %s in the chest!" % weapon["name"]
            commands = "Press Enter to continue..."
            # Attack is finished, paint results screen and pause
            screen.paint(
                common.get_stats(view, our_hero),
                commands,
                message,
                left_pane,
                right_center_pane
            )
            input("")
