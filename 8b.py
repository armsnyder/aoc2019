# ref: https://adventofcode.com/2019/day/8
import unittest


def main(inp, w, h):
  output = ['2']*w*h
  for i in range(len(inp)):
    if output[i%(w*h)] == '2':
      output[i%(w*h)] = inp[i]
  return '\n'.join([''.join(output[i:i+w]) for i in range(0, w*h, w)]).replace('1', '█').replace('0', ' ')


class Test8(unittest.TestCase):
  def test_example(self):
    self.assertEqual(' █\n█ ', main('0222112222120000', 2, 2))


if __name__ == '__main__':
  with open('8.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip(), 25, 6))
