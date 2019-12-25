# ref: https://adventofcode.com/2019/day/16
import unittest


def gen_pattern(factor, total_length):
  base_pattern = [0, 1, 0, -1]
  index = 0
  remaining_yields = factor - 1
  for _ in range(total_length):
    if remaining_yields == 0:
      index = (index + 1) % len(base_pattern)
      remaining_yields = factor
    yield base_pattern[index]
    remaining_yields -= 1


def main(input_signal: str, total_phases: int) -> str:
  def calculate_digit(pattern_generator, signal):
    return str(sum(a*int(b) for a, b in zip(pattern_generator, signal)))[-1:]
  for _ in range(total_phases):
    pattern_generators = [gen_pattern(factor, len(input_signal)) for factor in range(1, len(input_signal)+1)]
    input_signal = ''.join(calculate_digit(pg, input_signal) for pg in pattern_generators)
  return input_signal[:8]


class Test16(unittest.TestCase):
  def test_gen_pattern_1(self):
    self.assertEqual([1, 0, -1, 0, 1, 0, -1, 0], list(gen_pattern(1, 8)))

  def test_gen_pattern_2(self):
    self.assertEqual([0, 1, 1, 0, 0, -1, -1, 0], list(gen_pattern(2, 8)))

  def test_example_1(self):
    self.assertEqual('48226158', main('12345678', 1))

  def test_example_2(self):
    self.assertEqual('34040438', main('12345678', 2))

  def test_example_3(self):
    self.assertEqual('03415518', main('12345678', 3))

  def test_example_4(self):
    self.assertEqual('01029498', main('12345678', 4))

  def test_example_5(self):
    self.assertEqual('24176176', main('80871224585914546619083218645595', 100))

  def test_example_6(self):
    self.assertEqual('73745418', main('19617804207202209144916044189917', 100))

  def test_example_7(self):
    self.assertEqual('52432133', main('69317163492948606335995924319873', 100))


if __name__ == '__main__':
  with open('16.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip(), 100))
