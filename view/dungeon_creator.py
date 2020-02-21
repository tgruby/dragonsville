from random import shuffle, randrange
import common


def get_dungeons():
    dungeons = common.load('dungeons')
    if dungeons is None:
        dungeons = make_dungeons()
        common.save('dungeons', dungeons)
    return dungeons


def make_dungeons():
    #  loop through and create 10 dungeons
    dungeons = []
    for dungeon_id in range(4):
        if dungeon_id == 3:
            dungeons.append(make_maze(8 + dungeon_id, 6 + dungeon_id, dungeon_id, True))
        else:
            dungeons.append(make_maze(8 + dungeon_id, 6 + dungeon_id, dungeon_id, False))

    return dungeons


def make_maze(w=16, h=8, dungeon_id=0, is_last=False):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["| "] * w + ['|'] for _ in range(h)] + [[]]
    ver2 = [["|   "] * w + ['|   '] for _ in range(h)] + [[]]
    hor = [["--"] * w + ['-'] for _ in range(h + 1)]
    hor2 = [["+---"] * w + ['+   '] for _ in range(h + 1)]

    WDL = '|D'
    WDL2 = '|DW '
    HDL = ' D'
    HDL2 = ' DW '
    if is_last:
        WDL = '|X'
        WDL2 = '| X '
        HDL = ' X'
        HDL2 = ' >< '

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

    # Insert the Up-Ladder and Down-Ladder
    if dungeon_id % 2 == 0:
        ver[0][0] = '|U'
        ver2[0][0] = '|UP '
        if ver[h-1][w-1] == '| ':
            ver[h-1][w-1] = WDL
            ver2[h - 1][w - 1] = WDL2
        else:
            ver[h-1][w-1] = HDL
            ver2[h - 1][w - 1] = HDL2
    else:
        ver[0][0] = WDL
        ver2[0][0] = WDL2
        if ver[h-1][w-1] == '| ':
            ver[h-1][w-1] = '|U'
            ver2[h - 1][w - 1] = '|UP '
        else:
            ver[h-1][w-1] = ' U'
            ver2[h - 1][w - 1] = ' UP '

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

