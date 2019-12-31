# ref: https://adventofcode.com/2019/day/16
import unittest


def main(input_signal: str, total_phases: int) -> str:
  offset = int(input_signal[:7])
  meaningful_length = len(input_signal) * 10000 - offset
  meaningful_input_signal = input_signal[-(meaningful_length % len(input_signal)):] + input_signal * (
      meaningful_length // len(input_signal))
  working_signal = [int(x) for x in meaningful_input_signal]
  for _ in range(total_phases):
    for i in reversed(range(meaningful_length - 1)):
      working_signal[i] += working_signal[i + 1]
    for i in range(meaningful_length):
      working_signal[i] %= 10
  return ''.join(str(x) for x in working_signal[:8])


class Test16(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual('84462026', main('03036732577212944063491565474664', 100))

  def test_example_2(self):
    self.assertEqual('78725270', main('02935109699940807407585447034323', 100))

  def test_example_3(self):
    self.assertEqual('53553731', main('03081770884921959731165446850517', 100))


if __name__ == '__main__':
  with open('16.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip(), 100))
