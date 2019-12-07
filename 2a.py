# ref: https://adventofcode.com/2019/day/2
import unittest


def main(inp):
  vals = [int(x) for x in inp.strip().split(',')]
  i = 0
  while i < len(vals):
    v = vals[i]
    if v == 99:
      break
    elif v == 1:
      vals[vals[i+3]] = vals[vals[i+1]] + vals[vals[i+2]]
    elif v == 2:
      vals[vals[i+3]] = vals[vals[i+1]] * vals[vals[i+2]]
    else:
      raise ValueError(v)
    i += 4
  return vals[0]


class Test2(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual(3500, main('1,9,10,3,2,3,11,0,99,30,40,50\n'))

  def test_example_2(self):
    self.assertEqual(2, main('1,0,0,0,99\n'))

  def test_example_3(self):
    self.assertEqual(2, main('2,3,0,3,99\n'))

  def test_example_4(self):
    self.assertEqual(2, main('2,4,4,5,99,0\n'))

  def test_example_5(self):
    self.assertEqual(30, main('1,1,1,4,99,5,6,0,99\n'))


if __name__ == '__main__':
  with open('2.txt', 'r') as f:
    contents = f.read()
  nums = contents.strip().split(',')
  nums[1] = '12'
  nums[2] = '2'
  contents = ','.join(nums)
  print(main(contents))
