import rctools as rc

blueprints = list(map(rc.ints, rc.aoc_in(__file__)[0].splitlines()))
BP = tuple([((z[1], 0, 0), (z[2], 0, 0), (z[3], z[4], 0), (z[5], 0, z[6]))
           for z in blueprints])

# robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
# items = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}

robots = [1, 0, 0, 0]
items  = [0, 0, 0, 0]

def simulate(bp, robots, items, t=10):
    if t == 0:
        return items[0]
    for i, v in enumerate(robots):
        items[i] += robots[i]
    for robot in bp:
        purchase = [a - b for a, b in zip(items, robot)] + [items[3]]
        if all(z >= 0 for z in purchase):
            robots[i] += 1
            return max(simulate(bp, robots, purchase, t - 1))

print(simulate(BP[0], robots, items))
