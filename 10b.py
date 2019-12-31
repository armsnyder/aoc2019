# ref: https://adventofcode.com/2019/day/10
import unittest
import itertools
import math
from typing import List, Tuple, Dict

Coord = Tuple[int, int]


def main(inp: str) -> int:
  home = find_home_asteroid(inp)[0]
  x, y = get_destroy_order(inp, home)[199]
  return x * 100 + y


def find_home_asteroid(asteroid_map: str) -> Tuple[Coord, int]:
  grid = asteroid_map.split('\n')
  asteroid_coords: List[Coord] = [(x, y) for (x, y) in itertools.product(range(len(grid[0])), range(len(grid)))
                                  if grid[y][x] == '#']

  def count_visible(origin: Coord) -> int:
    visible = set()
    for asteroid in asteroid_coords:
      if asteroid != origin:
        visible.add(calc_simple_vector(origin, asteroid))
    return len(visible)

  answer_inverted = max((count_visible(coord), coord) for coord in asteroid_coords)
  return answer_inverted[1], answer_inverted[0]


def get_destroy_order(asteroid_map: str, home: Coord) -> List[Coord]:
  grid = asteroid_map.split('\n')
  asteroid_coords: List[Coord] = [(x, y) for (x, y) in itertools.product(range(len(grid[0])), range(len(grid)))
                                  if grid[y][x] == '#']
  asteroids_by_angle: Dict[Coord, List[Coord]] = {}
  for asteroid in asteroid_coords:
    if asteroid == home:
      continue
    key = calc_simple_vector(home, asteroid)
    if key not in asteroids_by_angle:
      asteroids_by_angle[key] = []
    asteroids_by_angle[key].append(asteroid)
  for key in asteroids_by_angle.keys():
    asteroids_by_angle[key] = sorted(asteroids_by_angle[key],
                                     key=lambda coord: (coord[0] - home[0]) ** 2 + (coord[1] - home[1]) ** 2)
  key_order = sorted(asteroids_by_angle.keys(), key=lambda coord: -math.atan2(coord[0], coord[1]))
  result = []
  while any(len(row) > 0 for row in asteroids_by_angle.values()):
    for key in key_order:
      row = asteroids_by_angle[key]
      if len(row) > 0:
        result.append(row.pop(0))
  return result


def calc_simple_vector(a: Coord, b: Coord) -> Coord:
  delta = (b[0] - a[0], b[1] - a[1])
  while True:
    factor = math.gcd(delta[0], delta[1])
    if factor == 1:
      return delta
    delta = (delta[0] // factor, delta[1] // factor)


class Test10(unittest.TestCase):

  def test_find_home_asteroid_example_1(self):
    self.assertEqual(((3, 4), 8), find_home_asteroid('''
.#..#
.....
#####
....#
...##'''[1:]))

  def test_find_home_asteroid_example_2(self):
    self.assertEqual(((5, 8), 33), find_home_asteroid('''
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####'''[1:]))

  def test_find_home_asteroid_example_3(self):
    self.assertEqual(((1, 2), 35), find_home_asteroid('''
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.'''[1:]))

  def test_find_home_asteroid_example_4(self):
    self.assertEqual(((6, 3), 41), find_home_asteroid('''
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..'''[1:]))

  def test_find_home_asteroid_example_5(self):
    self.assertEqual(((11, 13), 210), find_home_asteroid('''
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
###.##.####.##.#..##'''[1:]))

  def test_destroy_order_on_axis(self):
    self.assertListEqual([(1, 0), (2, 1), (1, 2), (0, 1)], get_destroy_order('''
.#.
###
.#.'''[1:], (1, 1)))

  def test_destroy_order_off_axis(self):
    self.assertListEqual([(2, 0), (2, 2), (0, 2), (0, 0)], get_destroy_order('''
#.#
.#.
#.#'''[1:], (1, 1)))

  def test_destroy_order_occlusion(self):
    self.assertListEqual([(1, 1), (1, 2)], get_destroy_order('''
.#.
.#.
.#.'''[1:], (1, 0)))

  def test_destroy_order_many(self):
    self.assertListEqual(
      [(2, 1), (3, 0), (3, 1), (4, 1), (3, 2), (4, 3), (3, 3), (3, 4), (2, 3), (1, 4), (1, 3), (0, 3), (1, 2), (0, 1),
       (1, 1), (1, 0), (2, 0), (4, 0), (4, 2), (4, 4), (2, 4), (0, 4), (0, 2), (0, 0)],
      get_destroy_order('''
#####
#####
#####
#####
#####'''[1:], (2, 2)))

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
###.##.####.##.#..##'''[1:]))


if __name__ == '__main__':
  with open('10.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
