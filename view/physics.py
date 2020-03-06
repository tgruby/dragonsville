from model import monsters
from controller import fight
from view import dungeon_creator, screen, images


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
    ladder_up = 'U'
    ladder_down = 'D'
    monster = 'M'
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

    current_dungeon_id = 0
    current_dungeon = None
    current_dungeon_map = None
    current_x = 0
    current_y = 0
    current_direction = north
    current_image = None

    dungeons = None

    def __init__(self, dungeon_id, direction, our_hero):
        self.dungeons = dungeon_creator.get_dungeons()
        self.current_dungeon_id = dungeon_id
        self.current_dungeon = self.dungeons[dungeon_id]["maze"]
        self.current_dungeon_map = self.dungeons[dungeon_id]["map"]
        self.current_direction = direction
        self.our_hero = our_hero
        # We assume on instantiation that we came "down" into the dungeon.  So we need to find the up_ladder in this
        # dungeon Using for loop
        for i in range(len(self.current_dungeon)):
            for j in range(len(self.current_dungeon[0])):
                if self.current_dungeon[i][j] == self.ladder_up:
                    self.current_y = i
                    self.current_x = j
                    return

    def generate_perspective(self):
        # Simplify variables
        d = self.current_direction
        x = self.current_x
        y = self.current_y
        # Positions should be listed in order of nearest left, nearest right, second nearest left...
        pos = []

        visible_limit = False
        for block_range in self.blocks:
            left_block = self.get_value_at_block(d, x, y, block_range[0])
            center_block = self.get_value_at_block(d, x, y, block_range[1])
            right_block = self.get_value_at_block(d, x, y, block_range[2])
            pos.append('_')
            pos.append(left_block)
            pos.append(center_block)
            pos.append(right_block)
            if center_block is self.wall:
                visible_limit = True
                break

        # If we have visibility out all 3 blocks, check to see if our end block is a hall or a wall.
        if not visible_limit and len(pos) is 12:
            pos.append('_')
            pos.append(self.get_value_at_block(d, x, y, self.distant_center_block))

        image_file = "dungeon"
        for p in pos:
            image_file = image_file + p

        self.current_image = image_file
        self.update_map()  # Don't forget to update the map

        try:
            return getattr(images, image_file)
        except:
            return images.cactus + '\n  ' + image_file

    # Return what we find in this block: wall, hallway, door, up-ladder, down-ladder
    def get_value_at_block(self, direction, x, y, block):
        try:
            x1 = block[direction]['x']
            y1 = block[direction]['y']
            value = self.current_dungeon[y + y1][x + x1]
            if value == self.hallway_1 or value == self.x_marks_the_spot:
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
                value == self.ladder_up or \
                value == self.ladder_down or \
                value == self.x_marks_the_spot:
            self.current_y += y1
            self.current_x += x1
            if self.current_dungeon[self.current_y][self.current_x] == self.x_marks_the_spot:
                fight.fight_a_monster(self.our_hero, monsters.Monster(monsters.red_dragon), self)
            return "You move one space " + self.get_direction() + "."
        else:
            return "You can't walk through walls!"

    def climb_down(self):
        # First check if they are on a down_ladder
        if self.current_dungeon[self.current_y][self.current_x] == self.ladder_down:
            self.current_dungeon_id = self.current_dungeon_id + 1
            self.current_dungeon = self.dungeons[self.current_dungeon_id]["maze"]
            self.current_dungeon_map = self.dungeons[self.current_dungeon_id]["map"]
            # We just came "down" into the next dungeon.  So we need to find the up_ladder in this dungeon and start
            # there.
            for i in range(len(self.current_dungeon)):
                for j in range(len(self.current_dungeon[i])):
                    if self.current_dungeon[i][j] == self.ladder_up:
                        self.current_y = i
                        self.current_x = j
                        break
            return "You climb down into the next dungeon!"
        else:
            return "You can't do that here!"

    def climb_up(self):
        # First check if they are on a down_ladder
        if self.current_dungeon[self.current_y][self.current_x] == self.ladder_up:
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
                        if self.current_dungeon[i][j] == self.ladder_down:
                            self.current_y = i
                            self.current_x = j
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
        dungeon_name = 'Dungeon ' + str(self.current_dungeon_id)
        new_map = screen.center_text(dungeon_name, ' ', len(map_array[0])) + '\n'
        for line in map_array:
            new_map += line + '\n'
        self.current_dungeon_map = new_map

    def change_char(self, s, p, r):
        return s[:p] + r + s[p + 1:]