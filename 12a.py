# ref: https://adventofcode.com/2019/day/12
import unittest
import re

def main(inp: str, steps: int) -> int:
  positions = [[int(c) for c in v] for v in re.findall(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', inp)]
  velocities = [[0, 0, 0] for _ in positions]
  for _ in range(steps):
    for c in range(len(positions[0])):
      for i in range(len(positions)):
        for j in range(len(positions)):
          if i != j:
            velocities[i][c] += 1 if positions[i][c] < positions[j][c] else -1 if positions[i][c] > positions[j][c] else 0
    positions = [[positions[i][c] + velocities[i][c] for c in range(len(positions[i]))] for i in range(len(positions))]
  return sum(sum(abs(c) for c in positions[i]) * sum(abs(c) for c in velocities[i]) for i in range(len(positions)))


class Test12(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual(179, main('''<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>''', 10))

  def test_example_2(self):
    self.assertEqual(1940, main('''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>''', 100))


if __name__ == '__main__':
  with open('12.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip(), 1000))
