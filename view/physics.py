import logging
from model import monsters
from controller import fight, dungeon
from view import dungeon_creator, screen, images, perspectives

log = logging.getLogger('dragonsville')


# This class is used to contain all the logic to manage the point of view of the hero as she moves through the maze.
# We use a class object here to simplify the encapsulation of the code: attributes and functions that naturally live
# together to create an "object".
class PointOfView:
    # Dungeon Map Keys
    hallway_1 = ' '
    hallway = 'H'
    wall_1 = '-'
    wall_2 = '+'
    wall_3 = '|'
    wall = 'W'
    door = 'D'
    doorway_up = '^'
    doorway_down = 'v'
    treasure = 'T'
    x_marks_the_spot = 'X'

    # Direction Keys
    north = 0
    east = 1
    south = 2
    west = 3

    # First Left Block by Direction: North, East, South, West
    near_left_block = [
        {"y": 0, "x": -1},
        {"y": -1, "x": 0},
        {"y": 0, "x": +1},
        {"y": +1, "x": 0}
    ]

    near_center_block = [
        {"y": 0, "x": 0},
        {"y": 0, "x": 0},
        {"y": 0, "x": 0},
        {"y": 0, "x": 0}
    ]

    near_right_block = [
        {"y": 0, "x": +1},
        {"y": +1, "x": 0},
        {"y": 0, "x": -1},
        {"y": -1, "x": 0}
    ]

    mid_left_block = [
        {"y": -1, "x": -1},
        {"y": -1, "x": +1},
        {"y": +1, "x": +1},
        {"y": +1, "x": -1}
    ]

    mid_center_block = [
        {"y": -1, "x": 0},
        {"y": 0, "x": +1},
        {"y": +1, "x": 0},
        {"y": 0, "x": -1}
    ]

    mid_right_block = [
        {"y": -1, "x": +1},
        {"y": +1, "x": +1},
        {"y": +1, "x": -1},
        {"y": -1, "x": -1}
    ]

    far_left_block = [
        {"y": -2, "x": -1},
        {"y": -1, "x": +2},
        {"y": +2, "x": +1},
        {"y": +1, "x": -2}
    ]

    far_center_block = [
        {"y": -2, "x": 0},
        {"y": 0, "x": +2},
        {"y": +2, "x": 0},
        {"y": 0, "x": -2}
    ]

    far_right_block = [
        {"y": -2, "x": +1},
        {"y": +1, "x": +2},
        {"y": +2, "x": -1},
        {"y": -1, "x": -2}
    ]

    distant_center_block = [
        {"y": -3, "x": 0},
        {"y": 0, "x": +3},
        {"y": +3, "x": 0},
        {"y": 0, "x": -3}
    ]

    blocks = [
        [near_left_block, near_center_block, near_right_block],
        [mid_left_block, mid_center_block, mid_right_block],
        [far_left_block, far_center_block, far_right_block]
    ]

    perspective_map = {
        "left_0": "a",
        "left_1": "b",
        "left_2": "c",
        "center_1": "d",
        "center_2": "e",
        "center_3": "f",
        "right_2": "g",
        "right_1": "h",
        "right_0": "i",
    }

    current_dungeon_id = 0
    current_dungeon = None
    current_dungeon_map = None
    current_x = 0
    current_y = 0
    current_direction = north

    dungeons = None

    def __init__(self, dungeon_id, direction, our_hero):
        self.dungeons = dungeon_creator.get_dungeons()
        self.current_dungeon_id = dungeon_id
        self.current_dungeon = self.dungeons[dungeon_id]["maze"]
        self.current_dungeon_map = self.dungeons[dungeon_id]["map"]
        self.current_direction = direction
        self.our_hero = our_hero

        # We assume on instantiation that we came "down" into the dungeon.
        # So we need to find the up door in this dungeon by scanning the 2d array
        for i in range(len(self.current_dungeon) - 1):
            for j in range(len(self.current_dungeon[0]) - 1):
                if self.current_dungeon[i][j] == self.doorway_up:
                    self.current_y = i
                    self.current_x = j + 1
                    log.info("starting x: %d, y: %d" % (j, i))
                    return

    def generate_perspective(self):
        # Simplify variables
        d = self.current_direction
        x = self.current_x
        y = self.current_y
        # Positions should be listed in order of nearest left, nearest right, second nearest left...
        obstructions = []

        visible_limit = False

        for i, block_range in enumerate(self.blocks):
            # Ignore the Door (treat it as a Hall) if we are standing in the doorway.
            ignore_door = False
            if i is 0:
                ignore_door = True
            left_obstruction = self.get_value_at_block(d, x, y, False, block_range[0])
            center_obstruction = self.get_value_at_block(d, x, y, ignore_door, block_range[1])
            right_obstruction = self.get_value_at_block(d, x, y, False, block_range[2])

            if i != 0 and (center_obstruction == self.wall or center_obstruction == self.door):
                obstructions.append("block_" + self.perspective_map.get("center_" + str(i)) + '_' + center_obstruction)
                visible_limit = True
                break
            else:
                obstructions.append("block_" + self.perspective_map.get("left_" + str(i)) + '_' + left_obstruction)
                obstructions.append("block_" + self.perspective_map.get("right_" + str(i)) + '_' + right_obstruction)

        # If we have visibility out all 3 blocks, check to see if our end block is a hall or a wall.
        if not visible_limit:
            distant_center = self.get_value_at_block(d, x, y, False, self.distant_center_block)
            obstructions.append("block_" + self.perspective_map.get("center_" + str(3)) + '_' + distant_center)

        image_file = perspectives.build_view(obstructions)
        self.update_map()  # Don't forget to update the map
        return image_file

    # Return what we find in this block: wall, hallway, door ignoring variations
    def get_value_at_block(self, direction, x, y, ignore_door, block):
        try:
            x1 = block[direction]['x']
            y1 = block[direction]['y']
            value = self.current_dungeon[y + y1][x + x1]
            if value == self.doorway_down or value == self.doorway_up or value == self.door:
                if ignore_door:
                    return self.hallway
                else:
                    return self.door
            if value == self.hallway_1 or value == self.x_marks_the_spot or value == self.treasure:
                return self.hallway
            elif value == self.wall_1 or value == self.wall_2 or value == self.wall_3:
                return self.wall
            else:
                return value
        except IndexError:
            return self.wall

    def get_location(self):
        return "x: " + str(self.current_x) + ", y: " + str(self.current_y)

    def get_direction(self):
        if self.current_direction == self.north:
            return "North"
        if self.current_direction == self.west:
            return "West"
        if self.current_direction == self.south:
            return "South"
        if self.current_direction == self.east:
            return "East"

    def turn_left(self):
        self.current_direction = self.current_direction - 1
        if self.current_direction < 0:
            self.current_direction = 3
        return "You turned left."

    def turn_right(self):
        self.current_direction = self.current_direction + 1
        if self.current_direction > 3:
            self.current_direction = 0
        return "You turned right."

    def step_forward(self):
        x1 = self.mid_center_block[self.current_direction]['x']
        y1 = self.mid_center_block[self.current_direction]['y']
        value = self.current_dungeon[self.current_y + y1][self.current_x + x1]
        if value == self.hallway_1 or \
                value == self.doorway_up or \
                value == self.doorway_down or \
                value == self.door or \
                value == self.treasure or \
                value == self.x_marks_the_spot:
            self.current_y += y1
            self.current_x += x1
            if value == self.x_marks_the_spot:
                fight.fight_a_monster(self.our_hero, monsters.Monster(monsters.red_dragon), self)
            if value == self.doorway_up:
                return self.climb_up()
            if value == self.doorway_down:
                return self.climb_down()
            if value == self.treasure:
                dungeon.check_for_treasure_callback(self.our_hero, self)
            return "You move one space " + self.get_direction() + "."
        else:
            return "You can't walk through walls!"

    def turn_around(self):
        if self.current_direction == self.north:
            self.current_direction = self.south
        elif self.current_direction == self.south:
            self.current_direction = self.north
        elif self.current_direction == self.east:
            self.current_direction = self.west
        elif self.current_direction == self.west:
            self.current_direction = self.east

    def climb_down(self):
        # First check if they are on a down_ladder
        if self.current_dungeon[self.current_y][self.current_x] == self.doorway_down:
            self.current_dungeon_id = self.current_dungeon_id + 1
            self.current_dungeon = self.dungeons[self.current_dungeon_id]["maze"]
            self.current_dungeon_map = self.dungeons[self.current_dungeon_id]["map"]
            # We just came "down" into the next dungeon.  So we need to find the up_ladder in this dungeon and start
            # there.
            for i in range(len(self.current_dungeon)):
                for j in range(len(self.current_dungeon[i])):
                    if self.current_dungeon[i][j] == self.doorway_up:
                        self.current_y = i
                        self.current_x = j
                        self.turn_around()  # Turn around, so we are "entering" the next dungeon
                        self.step_forward()  # Take one more step forward to enter the dungeon
                        break
            return "You climb down into the next dungeon!"
        else:
            return "You can't do that here!"

    def climb_up(self):
        # First check if they are on a down_ladder
        if self.current_dungeon[self.current_y][self.current_x] == self.doorway_up:
            self.current_dungeon_id = self.current_dungeon_id - 1
            # In this case, we climbed out of the dungeons, just return
            if self.current_dungeon_id < 0:
                return
            else:
                self.current_dungeon = self.dungeons[self.current_dungeon_id]["maze"]
                self.current_dungeon_map = self.dungeons[self.current_dungeon_id]["map"]
                # We just came "up" into the next dungeon.  So we need to find the down_ladder in this dungeon and start
                # there.
                for i in range(len(self.current_dungeon)):
                    for j in range(len(self.current_dungeon[i])):
                        if self.current_dungeon[i][j] == self.doorway_down:
                            self.current_y = i
                            self.current_x = j
                            self.turn_around()  # Turn around, so we are "entering" the next dungeon
                            self.step_forward()  # Take one more step forward to enter the dungeon
                            break
                return "You climb up into the higher dungeon."
        else:
            return "You can't do that here!"

    def update_map(self):
        # First check if they are on a down_ladder
        self.current_dungeon_map = self.dungeons[self.current_dungeon_id]["map"]
        map_array = str.splitlines(self.current_dungeon_map)
        # Get Vertical Row (y) where we stand
        row_string = map_array[self.current_y]
        # replace our x location with a '*'
        row_string = self.change_char(row_string, self.current_x * 2, '*')
        map_array[self.current_y] = row_string
        dungeon_name = 'Level ' + str(self.current_dungeon_id)
        new_map = screen.center_text(dungeon_name, ' ', len(map_array[0])) + '\n'
        for line in map_array:
            new_map += line + '\n'
        self.current_dungeon_map = new_map

    def change_char(self, s, p, r):
        return s[:p] + r + s[p + 1:]
