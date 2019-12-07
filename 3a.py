# ref: https://adventofcode.com/2019/day/3
import unittest


def main(inp):
  def points(line):
    accum = set()
    cur = (0,0)
    for elem in line.split(','):
      if elem[0] == 'R':
        delta = (1,0)
      elif elem[0] == 'L':
        delta = (-1,0)
      elif elem[0] == 'U':
        delta = (0,1)
      elif elem[0] == 'D':
        delta = (0,-1)
      else:
        raise ValueError(elem)
      for i in range(int(elem[1:])):
        nex = (cur[0]+delta[0], cur[1]+delta[1])
        accum.add(nex)
        cur = nex
    return accum
  a = points(inp.split('\n')[0])
  b = points(inp.split('\n')[1])
  common = (p for p in a if p in b)
  return min(abs(p[0])+abs(p[1]) for p in common)


class Test3(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual(6, main('R8,U5,L5,D3\nU7,R6,D4,L4\n'))

  def test_example_2(self):
    self.assertEqual(159, main('R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83\n'))

  def test_example_3(self):
    self.assertEqual(135, main('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7\n'))


if __name__ == '__main__':
  with open('3.txt', 'r') as f:
    contents = f.read()
  print(main(contents))
