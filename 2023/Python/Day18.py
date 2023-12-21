fo = open("input.txt", "r")
f = list(fo)
fo.close()

grid = []
instructions = []
cctr = 0
rctr = 0
maxr = 1
minr = 1
maxc = 1
minc = 1
for l in f:
    instructions.append(l.strip().split())
    instructions[-1][1] = int(instructions[-1][1])
    if instructions[-1][0] == 'R':
        cctr += instructions[-1][1]
    elif instructions[-1][0] == 'L':
        cctr -= instructions[-1][1]
    elif instructions[-1][0] == 'D':
        rctr += instructions[-1][1]
    else:
        rctr -= instructions[-1][1]
    maxr = max(maxr, rctr)
    maxc = max(maxc, cctr)
    minr = min(minr, rctr)
    minc = min(minc, cctr)

r = maxr - minr + 1
c = maxc - minc + 1

for i in range(r + 2):
    grid.append([])
    for j in range(c + 2):
        grid[i].append('.')

x, y = -minc + 1, -minr + 1
grid[y][x] = '#'
for ins in instructions:
    if ins[0] == 'R':
        for nx in range(x, x + ins[1] + 1):
            grid[y][nx] = '#'
        x += ins[1]
    elif ins[0] == 'L':
        for nx in range(x - ins[1], x + 1):
            grid[y][nx] = '#'
        x -= ins[1]
    elif ins[0] == 'D':
        for ny in range(y, y + ins[1] + 1):
            grid[ny][x] = '#'
        y += ins[1]
    else:
        for ny in range(y - ins[1], y + 1):
            grid[ny][x] = '#'
        y -= ins[1]

for y in range(r):
    cnt = 0
    on_edge = False
    last_inc = None
    for x in range(c):
        if grid[y][x] == '#':
            if grid[y - 1][x] == '#' and grid[y + 1][x] == '#':
                cnt += 1
                on_edge = False
            elif grid[y - 1][x] == '#' and last_inc == 'lo':
                cnt += 1
                on_edge = False
            elif grid[y + 1][x] == '#' and last_inc == 'hi':
                cnt += 1
                on_edge = False
            else:
                on_edge = True
                if grid[y + 1][x] == '#':
                    last_inc = 'lo'
                elif grid[y - 1][x] == '#':
                    last_inc = 'hi'
        elif grid[y][x] == '.':
            on_edge = False
            last_inc = None
            if cnt % 2 == 1:
                grid[y][x] = '#'


area = 0
for y in grid:
    area += y.count('#')
print(area)

fo = open("input.txt", "r")
f = list(fo)
fo.close()

grid = []
instructions = []
for l in f:
    instructions.append(l.strip().split())
    l = int(instructions[-1][2][2:-2], 16)
    d = int(instructions[-1][2][-2], 16)
    if d == 0:
        d = 'R'
    elif d == 1:
        d = 'D'
    elif d == 2:
        d = 'L'
    elif d == 3:
        d = 'U'
    instructions[-1] = [d, l]

x, y = 0, 0
ox, oy = 0, 0
area = 0
perimeter = 0
for d, l in instructions:
    if d == 'R':
        x += l
    elif d == 'L':
        x -= l
    elif d == 'D':
        y += l
    else:
        y -= l
    area += (oy - y) * (ox + x)
    perimeter += l
    ox = x
    oy = y

area += (oy - y) * (ox + x)
print(abs(area) // 2 + perimeter // 2 + 1)