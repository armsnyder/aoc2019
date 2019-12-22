# ref: https://adventofcode.com/2019/day/12
import unittest
import re
import copy
import math

def main(inp: str) -> int:
  def lcm(a, b):
    return int(a * b / math.gcd(a, b))
  def do_axis(axis_positions: []) -> int:
    axis_velocities = [0 for _ in axis_positions]
    original_axis_positions = copy.copy(axis_positions)
    original_axis_velocities = copy.copy(axis_velocities)
    step = 0
    while step == 0 or axis_positions != original_axis_positions or axis_velocities != original_axis_velocities:
      for i in range(len(axis_positions)):
        for j in range(len(axis_positions)):
          if i != j:
            axis_velocities[i] += 1 if axis_positions[i] < axis_positions[j] else -1 if axis_positions[i] > axis_positions[j] else 0
      axis_positions = [axis_positions[i] + axis_velocities[i] for i in range(len(axis_positions))]
      step += 1
    return step
  positions = [[int(c) for c in v] for v in re.findall(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', inp)]
  return lcm(lcm(do_axis([v[0] for v in positions]), do_axis([v[1] for v in positions])), do_axis([v[2] for v in positions]))


class Test12(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual(2772, main('''<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>'''))

  def test_example_2(self):
    self.assertEqual(4686774924, main('''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''))

  # The rest of these tests could be useful later if I decide to further optimize the program.

  def test_small_0__1(self):
    self.assertEqual(1, main('''<x=0, y=0, z=0>
<x=0, y=0, z=0>
'''))

  def test_small_1__4(self):
    self.assertEqual(4, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
'''))

  def test_small_2__6(self):
    self.assertEqual(6, main('''<x=0, y=0, z=0>
<x=2, y=0, z=0>
'''))

  def test_small_3__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=3, y=0, z=0>
'''))

  def test_small_4__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=4, y=0, z=0>
'''))

  def test_small_5__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=5, y=0, z=0>
'''))

  def test_small_6__10(self):
    self.assertEqual(10, main('''<x=0, y=0, z=0>
<x=6, y=0, z=0>
'''))

  def test_small_7__12(self):
    self.assertEqual(12, main('''<x=0, y=0, z=0>
<x=7, y=0, z=0>
'''))

  def test_small_8__12(self):
    self.assertEqual(12, main('''<x=0, y=0, z=0>
<x=8, y=0, z=0>
'''))

  def test_small_9__12(self):
    self.assertEqual(12, main('''<x=0, y=0, z=0>
<x=9, y=0, z=0>
'''))

  def test_small_10__12(self):
    self.assertEqual(12, main('''<x=0, y=0, z=0>
<x=10, y=0, z=0>
'''))

  def test_small_11__12(self):
    self.assertEqual(12, main('''<x=0, y=0, z=0>
<x=11, y=0, z=0>
'''))

  def test_small_12__14(self):
    self.assertEqual(14, main('''<x=0, y=0, z=0>
<x=12, y=0, z=0>
'''))

  def test_small_13__16(self):
    self.assertEqual(16, main('''<x=0, y=0, z=0>
<x=13, y=0, z=0>
'''))

  def test_small_14__16(self):
    self.assertEqual(16, main('''<x=0, y=0, z=0>
<x=14, y=0, z=0>
'''))

  def test_small_15__16(self):
    self.assertEqual(16, main('''<x=0, y=0, z=0>
<x=15, y=0, z=0>
'''))

  def test_small_16__16(self):
    self.assertEqual(16, main('''<x=0, y=0, z=0>
<x=16, y=0, z=0>
'''))

  def test_small_17__16(self):
    self.assertEqual(16, main('''<x=0, y=0, z=0>
<x=17, y=0, z=0>
'''))

  def test_small_18__16(self):
    self.assertEqual(16, main('''<x=0, y=0, z=0>
<x=18, y=0, z=0>
'''))

  def test_small_19__16(self):
    self.assertEqual(16, main('''<x=0, y=0, z=0>
<x=19, y=0, z=0>
'''))

  def test_small_20__18(self):
    self.assertEqual(18, main('''<x=0, y=0, z=0>
<x=20, y=0, z=0>
'''))

  def test_small_21__18(self):
    self.assertEqual(20, main('''<x=0, y=0, z=0>
<x=21, y=0, z=0>
'''))

  def test_small_22__18(self):
    self.assertEqual(20, main('''<x=0, y=0, z=0>
<x=22, y=0, z=0>
'''))

  def test_small_23__18(self):
    self.assertEqual(20, main('''<x=0, y=0, z=0>
<x=23, y=0, z=0>
'''))

  def test_small_24__18(self):
    self.assertEqual(20, main('''<x=0, y=0, z=0>
<x=24, y=0, z=0>
'''))

  def test_small_25__18(self):
    self.assertEqual(20, main('''<x=0, y=0, z=0>
<x=25, y=0, z=0>
'''))

  def test_small_26__18(self):
    self.assertEqual(20, main('''<x=0, y=0, z=0>
<x=26, y=0, z=0>
'''))

  def test_small_27__18(self):
    self.assertEqual(20, main('''<x=0, y=0, z=0>
<x=27, y=0, z=0>
'''))

  def test_small_28__18(self):
    self.assertEqual(20, main('''<x=0, y=0, z=0>
<x=28, y=0, z=0>
'''))

  def test_small_29__18(self):
    self.assertEqual(20, main('''<x=0, y=0, z=0>
<x=29, y=0, z=0>
'''))

  def test_small_30__18(self):
    self.assertEqual(22, main('''<x=0, y=0, z=0>
<x=30, y=0, z=0>
'''))

  def test_small_0_0__1(self):
    self.assertEqual(1, main('''<x=0, y=0, z=0>
<x=0, y=0, z=0>
<x=0, y=0, z=0>
'''))

  def test_small_0_1__4(self):
    self.assertEqual(4, main('''<x=0, y=0, z=0>
<x=0, y=0, z=0>
<x=1, y=0, z=0>
'''))

  def test_small_0_2__4(self):
    self.assertEqual(4, main('''<x=0, y=0, z=0>
<x=0, y=0, z=0>
<x=2, y=0, z=0>
'''))

  def test_small_0_3__6(self):
    self.assertEqual(6, main('''<x=0, y=0, z=0>
<x=0, y=0, z=0>
<x=3, y=0, z=0>
'''))

  def test_small_0_4__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=0, y=0, z=0>
<x=4, y=0, z=0>
'''))

  def test_small_0_5__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=0, y=0, z=0>
<x=5, y=0, z=0>
'''))

  def test_small_1_1__4(self):
    self.assertEqual(4, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=2, y=0, z=0>
'''))

  def test_small_1_2__10(self):
    self.assertEqual(10, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=3, y=0, z=0>
'''))

  def test_small_1_3__7(self):
    self.assertEqual(7, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=4, y=0, z=0>
'''))

  def test_small_1_4__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=5, y=0, z=0>
'''))

  def test_small_1_5__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=6, y=0, z=0>
'''))

  def test_small_2_2__6(self):
    self.assertEqual(6, main('''<x=0, y=0, z=0>
<x=2, y=0, z=0>
<x=4, y=0, z=0>
'''))

  def test_small_2_3__17(self):
    self.assertEqual(17, main('''<x=0, y=0, z=0>
<x=2, y=0, z=0>
<x=5, y=0, z=0>
'''))

  def test_small_2_4__24(self):
    self.assertEqual(24, main('''<x=0, y=0, z=0>
<x=2, y=0, z=0>
<x=6, y=0, z=0>
'''))

  def test_small_2_5__24(self):
    self.assertEqual(24, main('''<x=0, y=0, z=0>
<x=2, y=0, z=0>
<x=7, y=0, z=0>
'''))

  def test_small_3_3__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=3, y=0, z=0>
<x=6, y=0, z=0>
'''))

  def test_small_3_4__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=3, y=0, z=0>
<x=7, y=0, z=0>
'''))

  def test_small_3_5__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=3, y=0, z=0>
<x=8, y=0, z=0>
'''))

  def test_small_4_4__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=4, y=0, z=0>
<x=8, y=0, z=0>
'''))

  def test_small_4_5__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=4, y=0, z=0>
<x=9, y=0, z=0>
'''))

  def test_small_4_6__18(self):
    self.assertEqual(18, main('''<x=0, y=0, z=0>
<x=4, y=0, z=0>
<x=10, y=0, z=0>
'''))

  def test_small_5_5__8(self):
    self.assertEqual(8, main('''<x=0, y=0, z=0>
<x=5, y=0, z=0>
<x=10, y=0, z=0>
'''))

  def test_small_5_6__70(self):
    self.assertEqual(70, main('''<x=0, y=0, z=0>
<x=5, y=0, z=0>
<x=11, y=0, z=0>
'''))

  def test_small_6_6__10(self):
    self.assertEqual(10, main('''<x=0, y=0, z=0>
<x=6, y=0, z=0>
<x=12, y=0, z=0>
'''))

  def test_small_1_2_3__4(self):
    self.assertEqual(4, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=2, y=0, z=0>
<x=3, y=0, z=0>
'''))

  def test_small_2_4_6__6(self):
    self.assertEqual(6, main('''<x=0, y=0, z=0>
<x=2, y=0, z=0>
<x=4, y=0, z=0>
<x=6, y=0, z=0>
'''))

  def test_small_2_3_4__56(self):
    self.assertEqual(56, main('''<x=0, y=0, z=0>
<x=2, y=0, z=0>
<x=3, y=0, z=0>
<x=4, y=0, z=0>
'''))

  def test_small_1_2_4__56(self):
    self.assertEqual(56, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=2, y=0, z=0>
<x=4, y=0, z=0>
'''))

  def test_small_1_2_5__18(self):
    self.assertEqual(18, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=2, y=0, z=0>
<x=5, y=0, z=0>
'''))

  def test_small_1_1_1__4(self):
    self.assertEqual(4, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=1, y=0, z=0>
<x=1, y=0, z=0>
'''))

  def test_small_1_2_2__4(self):
    self.assertEqual(4, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=2, y=0, z=0>
<x=2, y=0, z=0>
'''))

  def test_small_1_1_2__4(self):
    self.assertEqual(4, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=1, y=0, z=0>
<x=2, y=0, z=0>
'''))

  def test_small_2_2_2__4(self):
    self.assertEqual(4, main('''<x=0, y=0, z=0>
<x=2, y=0, z=0>
<x=2, y=0, z=0>
<x=2, y=0, z=0>
'''))

  def test_small_2_4_2__4(self):
    self.assertEqual(4, main('''<x=0, y=0, z=0>
<x=2, y=0, z=0>
<x=4, y=0, z=0>
<x=2, y=0, z=0>
'''))

  def test_small_2_3_2__4(self):
    self.assertEqual(4, main('''<x=0, y=0, z=0>
<x=2, y=0, z=0>
<x=3, y=0, z=0>
<x=2, y=0, z=0>
'''))

  def test_small_2_5_2__1500(self):
    self.assertEqual(1500, main('''<x=0, y=0, z=0>
<x=2, y=0, z=0>
<x=5, y=0, z=0>
<x=2, y=0, z=0>
'''))

  def test_small_1_5_1__52(self):
    self.assertEqual(52, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=5, y=0, z=0>
<x=1, y=0, z=0>
'''))

  def test_small_1_5_4__6(self):
    self.assertEqual(6, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=5, y=0, z=0>
<x=4, y=0, z=0>
'''))

  def test_small_1_5_5__52(self):
    self.assertEqual(52, main('''<x=0, y=0, z=0>
<x=1, y=0, z=0>
<x=5, y=0, z=0>
<x=5, y=0, z=0>
'''))


if __name__ == '__main__':
  with open('12.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
