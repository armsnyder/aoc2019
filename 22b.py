# ref: https://adventofcode.com/2019/day/22
import unittest
from typing import List, Tuple

Deck = List[int]
ScaleShift = Tuple[int, int]


def locate_card_after_shuffle(directions: str, total_cards: int, card_index_to_return: int,
                              shuffle_iterations: int) -> int:
  scale, shift = operation_power(combine_directions_into_single_operation(directions), shuffle_iterations)
  return modinv(scale, total_cards) * (card_index_to_return - shift) % total_cards


def operation_power(operation: ScaleShift, n: int) -> ScaleShift:
  scale, shift = operation
  if scale != 1:
    return scale ** n, shift * (1 - scale ** n) / (1 - scale)  # Sum of a geometric series
  else:
    return combine_operations([operation] * n)


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

  return combine_operations([parse_direction(x) for x in directions.split('\n')])


def combine_operations(scale_shifts: List[ScaleShift]) -> ScaleShift:
  result = scale_shifts[0]
  for next_op in scale_shifts[1:]:
    result = result[0] * next_op[0], next_op[0] * result[1] + next_op[1]
  return result


def modinv(a, m):
  def egcd(a, b):
    if a == 0:
      return b, 0, 1
    else:
      g, y, x = egcd(b % a, a)
      return g, x - (b // a) * y, y

  g, x, y = egcd(a % m, m)
  if g != 1:
    raise Exception(f'modular inverse of {a} (mod {m}) does not exist')
  else:
    return x % m


class Test22(unittest.TestCase):
  def test_deal_into_new_stack(self):
    self.assertEqual(6, locate_card_after_shuffle('deal into new stack', 10, 3, 1))

  def test_cut(self):
    self.assertEqual(6, locate_card_after_shuffle('cut 3', 10, 3, 1))

  def test_cut_negative(self):
    self.assertEqual(9, locate_card_after_shuffle('cut -4', 10, 3, 1))

  def test_deal_with_increment(self):
    self.assertEqual(8, locate_card_after_shuffle('deal with increment 3', 10, 4, 1))

  def test_two_deal_with_increment(self):
    self.assertEqual(6, locate_card_after_shuffle('deal with increment 3\ndeal with increment 3', 10, 4, 1))

  def test_two_different_deal_with_increment(self):
    self.assertEqual(2, locate_card_after_shuffle('deal with increment 3\ndeal with increment 9', 10, 4, 1))

  def test_cut_then_deal(self):
    self.assertEqual(9, locate_card_after_shuffle('cut 3\ndeal into new stack', 10, 3, 1))

  def test_deal_then_cut(self):
    self.assertEqual(3, locate_card_after_shuffle('deal into new stack\ncut 3', 10, 3, 1))

  def test_example_1(self):
    self.assertEqual(9, locate_card_after_shuffle('''deal with increment 7
deal into new stack
deal into new stack''', 10, 3, 1))

  def test_example_2(self):
    self.assertEqual(4, locate_card_after_shuffle('''cut 6
deal with increment 7
deal into new stack''', 10, 3, 1))

  def test_example_3(self):
    self.assertEqual(7, locate_card_after_shuffle('''deal with increment 7
deal with increment 9
cut -2''', 10, 3, 1))

  def test_example_4(self):
    self.assertEqual(8, locate_card_after_shuffle('''deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1''', 10, 3, 1))

  def test_cut_twice(self):
    self.assertEqual(9, locate_card_after_shuffle('cut 3', 10, 3, 2))


if __name__ == '__main__':
  with open('22.txt', 'r') as f:
    contents = f.read()
  print(locate_card_after_shuffle(contents.strip(), 119315717514047, 2020, 101741582076661))
