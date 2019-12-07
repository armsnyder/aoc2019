# ref: https://adventofcode.com/2019/day/1
import unittest


def main(inp):
  def cost(module):
    fuel = max(0, int(int(module)/3)-2)
    if fuel > 0:
      fuel += cost(fuel)
    return fuel
  return sum(cost(int(i)) for i in inp.split('\n') if i != '')


class Test1(unittest.TestCase):
  def test_runs(self):
    main('')

  def test_example(self):
    self.assertEqual(51314, main('\n'.join(['14', '1969', '100756'])))


if __name__ == '__main__':
  with open('1.txt', 'r') as f:
    contents = f.read()
  print(main(contents))
