from random import shuffle, randrange
import common


def get_dungeons():
    dungeons = common.load('dungeons')
    if dungeons is None:
        dungeons = make_dungeons()
        common.save('dungeons', dungeons)
    return dungeons


def make_dungeons():
    #  loop through and create 4 dungeons, each progressively bigger
    dungeons = []
    for dungeon_id in range(4):
        if dungeon_id == 3:
            dungeons.append(make_maze(5 + dungeon_id, 3 + dungeon_id, dungeon_id, True))
        else:
            dungeons.append(make_maze(5 + dungeon_id, 3 + dungeon_id, dungeon_id, False))

    return dungeons


def make_maze(w=16, h=8, dungeon_id=0, is_last=False):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["| "] * w + ['|'] for _ in range(h)] + [[]]
    ver2 = [["|   "] * w + ['|   '] for _ in range(h)] + [[]]
    hor = [["+-"] * w + ['-'] for _ in range(h + 1)]
    hor2 = [["+---"] * w + ['+   '] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+ "
                hor2[max(y, yy)][x] = "+   "
            if yy == y:
                ver[y][max(x, xx)] = "  "
                ver2[y][max(x, xx)] = "    "
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    WDL2 = '| DW'
    HDL2 = '  DW'
    if is_last:
        WDL2 = '| X '
        HDL2 = ' >< '

    # Insert the Up-Ladder and Down-Ladder
    if dungeon_id % 2 == 0:
        ver2[0][0] = '|UP '
        if ver[h-1][w-1] == '| ':
            ver2[h - 1][w - 1] = WDL2
        else:
            ver2[h - 1][w - 1] = HDL2
    else:
        ver2[0][0] = WDL2
        if ver[h-1][w-1] == '| ':
            ver2[h - 1][w - 1] = '|UP '
        else:
            ver2[h - 1][w - 1] = ' UP '

    # Add Entrances and Exits
    upper_left = 'v '
    if is_last:
        upper_left = 'X '
    lower_right = '^'
    if dungeon_id % 2 == 0:
        upper_left = '^ '
        lower_right = 'v'
        if is_last:
            lower_right = 'X'
    ver[0][0] = upper_left
    ver[len(ver)-2][len(ver[0])-1] = lower_right

    # Prepare the Maze and Map for Output
    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    maze = []

    buff = []
    for index in range(0, len(s)):
        if s[index] == '\n':
            maze.append(buff)
            buff = []
        else:
            buff.append(s[index])

    mmap = ""
    for (a, b) in zip(hor2, ver2):
        mmap += ''.join(a + ['\n'] + b + ['\n'])

    return {
        "maze": maze,
        "map": mmap
    }


if __name__ == "__main__":
    # Testing
    maze = make_maze(6, 4, 0, False)
    print(maze.get("map"))
    for row in maze.get("maze"):
        print(row)

