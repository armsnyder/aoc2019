# ref: https://adventofcode.com/2019/day/8
import unittest


def main(inp, w, h):
  return min(sorted((inp[i:i+w*h].count('0'), inp[i:i+w*h].count('1')*inp[i:i+w*h].count('2')) for i in range(0, len(inp), w*h)))[1]


class Test8(unittest.TestCase):
  def test_example(self):
    self.assertEqual(1, main('123456789012', 3, 2))


if __name__ == '__main__':
  with open('8.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip(), 25, 6))
