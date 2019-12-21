# ref: https://adventofcode.com/2019/day/10
import unittest
import itertools
import math


def main(inp):
  grid = inp.strip().split('\n')
  asteroid_coords = set((y,x) for (y,x) in itertools.product(range(len(grid)), range(len(grid[0]))) if grid[y][x] == '#')
  def get_common_factor(a, b):
    for i in range(2, max(abs(a), abs(b))+1):
      if a % i == 0 and b % i == 0:
        return i
    return None
  def get_visible(y, x):
    visible = {}
    for (ay, ax) in asteroid_coords:
      (dy, dx) = (y-ay, x-ax)
      if (dy, dx) == (0, 0):
        continue
      cf = 1
      while cf is not None:
        (dy, dx) = (int(dy/cf), int(dx/cf))
        cf = get_common_factor(dy, dx)
      if (dy, dx) not in visible or (abs(dy) <= abs(y-visible[(dy, dx)][0]) and abs(dx) <= abs(x-visible[(dy, dx)][1])):
        visible[(dy, dx)] = (ay, ax)
    return visible.values()
  (home_y, home_x) = max((len(get_visible(y,x)), (y,x)) for (y,x) in asteroid_coords)[1]
  destroyed_asteroids = []
  while len(destroyed_asteroids) < 200:
    for coord in sort_coords_by_angle((home_y, home_x), get_visible(home_y, home_x)):
      asteroid_coords.remove(coord)
      destroyed_asteroids.append(coord)
  print(destroyed_asteroids[200])
  print(destroyed_asteroids[199])
  print(destroyed_asteroids[198])
  return destroyed_asteroids[199][0] + 100 * destroyed_asteroids[199][1]


def sort_coords_by_angle(origin, coords):
  def get_angle(ay, ax):
    return -math.atan2(ax-origin[1], ay-origin[0])
  return sorted(coords, key=lambda p: get_angle(p[0], p[1]))


class Test10(unittest.TestCase):
  def test_sort_coords(self):
    self.assertEqual(
      [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)],
      sort_coords_by_angle((0,0), [(-1,1), (0,1), (1,-1), (1,1), (1,0), (0,-1), (-1,-1), (-1,0)]))

  def test_example(self):
    self.assertEqual(802, main('''
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
'''))


if __name__ == '__main__':
  with open('10.txt', 'r') as f:
    contents = f.read()
  print(main(contents))
