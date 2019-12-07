# ref: https://adventofcode.com/2019/day/1
import unittest


def main(inp):
  return sum(int(int(i)/3)-2 for i in inp.split('\n') if i != '')


class Test1(unittest.TestCase):
  def test_runs(self):
    main('')

  def test_example(self):
    self.assertEqual(34241, main('\n'.join(['12', '14', '1969', '100756'])))


if __name__ == '__main__':
  with open('1.txt', 'r') as f:
    contents = f.read()
  print(main(contents))
