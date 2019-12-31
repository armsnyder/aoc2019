# ref: https://adventofcode.com/2019/day/22
import unittest
from typing import Tuple, List

ScaleShift = Tuple[int, int]


def main(inp: str) -> int:
  return shuffle(2019, 10007, combine_directions_into_single_operation(inp))


def shuffle(card_index: int, total_cards: int, operation: ScaleShift) -> int:
  return (card_index * operation[0] + operation[1]) % total_cards


def combine_directions_into_single_operation(directions: str) -> ScaleShift:
  def parse_direction(direction_text: str) -> ScaleShift:
    key_deal_with_increment = 'deal with increment '
    key_cut = 'cut '
    key_deal_into_new_stack = 'deal into new stack'
    if direction_text.startswith(key_cut):
      return 1, -int(direction_text[len(key_cut):])
    if direction_text == key_deal_into_new_stack:
      return -1, -1
    if direction_text.startswith(key_deal_with_increment):
      return int(direction_text[len(key_deal_with_increment):]), 0
    raise ValueError(direction_text)

  def combine_operations(scale_shifts: List[ScaleShift]) -> ScaleShift:
    result = scale_shifts[0]
    for next_op in scale_shifts[1:]:
      result = result[0] * next_op[0], next_op[0] * result[1] + next_op[1]
    return result

  return combine_operations([parse_direction(x) for x in directions.split('\n')])


class Test22(unittest.TestCase):
  def test_deal_into_new_stack(self):
    operation = combine_directions_into_single_operation('deal into new stack')
    self.assertEqual(0, shuffle(9, 10, operation))
    self.assertEqual(2, shuffle(7, 10, operation))
    self.assertEqual(7, shuffle(2, 10, operation))
    self.assertEqual(9, shuffle(0, 10, operation))

  def test_cut(self):
    operation = combine_directions_into_single_operation('cut 3')
    self.assertEqual(6, shuffle(9, 10, operation))
    self.assertEqual(4, shuffle(7, 10, operation))
    self.assertEqual(9, shuffle(2, 10, operation))
    self.assertEqual(7, shuffle(0, 10, operation))

  def test_cut_negative(self):
    operation = combine_directions_into_single_operation('cut -4')
    self.assertEqual(3, shuffle(9, 10, operation))
    self.assertEqual(1, shuffle(7, 10, operation))
    self.assertEqual(6, shuffle(2, 10, operation))
    self.assertEqual(4, shuffle(0, 10, operation))

  def test_deal_with_increment(self):
    operation = combine_directions_into_single_operation('deal with increment 3')
    self.assertEqual(0, shuffle(0, 10, operation))
    self.assertEqual(2, shuffle(4, 10, operation))
    self.assertEqual(7, shuffle(9, 10, operation))
    self.assertEqual(9, shuffle(3, 10, operation))

  def test_example_1(self):
    operation = combine_directions_into_single_operation('''deal with increment 7
deal into new stack
deal into new stack''')
    self.assertEqual(0, shuffle(0, 10, operation))
    self.assertEqual(2, shuffle(6, 10, operation))
    self.assertEqual(7, shuffle(1, 10, operation))
    self.assertEqual(9, shuffle(7, 10, operation))

  def test_example_2(self):
    operation = combine_directions_into_single_operation('''cut 6
deal with increment 7
deal into new stack''')
    self.assertEqual(0, shuffle(3, 10, operation))
    self.assertEqual(2, shuffle(7, 10, operation))
    self.assertEqual(7, shuffle(2, 10, operation))
    self.assertEqual(9, shuffle(6, 10, operation))

  def test_example_3(self):
    operation = combine_directions_into_single_operation('''deal with increment 7
deal with increment 9
cut -2''')
    self.assertEqual(0, shuffle(6, 10, operation))
    self.assertEqual(2, shuffle(0, 10, operation))
    self.assertEqual(7, shuffle(5, 10, operation))
    self.assertEqual(9, shuffle(9, 10, operation))

  def test_example_4(self):
    operation = combine_directions_into_single_operation('''deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1''')
    self.assertEqual(0, shuffle(9, 10, operation))
    self.assertEqual(2, shuffle(5, 10, operation))
    self.assertEqual(7, shuffle(0, 10, operation))
    self.assertEqual(9, shuffle(6, 10, operation))


if __name__ == '__main__':
  with open('22.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
