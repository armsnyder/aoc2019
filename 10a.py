# ref: https://adventofcode.com/2019/day/10
import unittest
import itertools


def main(inp):
  grid = inp.strip().split('\n')
  asteroid_coords = [(y,x) for (y,x) in itertools.product(range(len(grid)), range(len(grid[0]))) if grid[y][x] == '#']
  def get_common_factor(a, b):
    for i in range(2, max(abs(a), abs(b))+1):
      if a % i == 0 and b % i == 0:
        return i
    return None
  def count_visible(y, x):
    visible = set()
    for (ay, ax) in asteroid_coords:
      (dy, dx) = (y-ay, x-ax)
      if (dy, dx) == (0, 0):
        continue
      cf = 1
      while cf is not None:
        (dy, dx) = (int(dy/cf), int(dx/cf))
        cf = get_common_factor(dy, dx)
      visible.add((dy, dx))
    return len(visible)
  return max(count_visible(y,x) for (y,x) in asteroid_coords)


class Test10(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual(8, main('''
.#..#
.....
#####
....#
...##
'''))

  def test_example_2(self):
    self.assertEqual(33, main('''
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
'''))


if __name__ == '__main__':
  with open('10.txt', 'r') as f:
    contents = f.read()
  print(main(contents))
