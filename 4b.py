# ref: https://adventofcode.com/2019/day/4
import unittest


def main(inp):
  def can_be_password(n):
    last = 0
    chain_count = 0
    has_double = False
    for c in str(n):
      c_int = int(c)
      if c_int < last:
        return False
      if c_int == last:
        chain_count += 1
      else:
        if chain_count == 1:
          has_double = True
        chain_count = 0
      last = c_int
    if chain_count == 1:
      has_double = True
    return has_double
  bot = int(inp.split('-')[0])
  top = int(inp.split('-')[1])
  count = 0
  for i in range(bot, top+1):
    if can_be_password(i):
      count += 1
  return count


class Test4(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual(0, main('111111-111111'))

  def test_example_2(self):
    self.assertEqual(0, main('223450-223450'))

  def test_example_3(self):
    self.assertEqual(0, main('123789-123789'))

  def test_example_4(self):
    self.assertEqual(1, main('112233-112233'))

  def test_example_5(self):
    self.assertEqual(0, main('123444-123444'))

  def test_example_6(self):
    self.assertEqual(1, main('111122-111122'))


if __name__ == '__main__':
  with open('4.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
