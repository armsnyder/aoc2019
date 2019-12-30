# ref: https://adventofcode.com/2019/day/22
import unittest
from typing import List, Callable


Deck = List[int]


def locate_card_after_shuffle(directions: str, total_cards: int, card_index_to_return: int, shuffle_iterations: int) -> int:
  def parse_into_transform_function(direction_text: str) -> Callable[[int], int]:
    key_deal_with_increment = 'deal with increment '
    key_cut = 'cut '
    key_deal_into_new_stack = 'deal into new stack'
    if direction_text.startswith(key_deal_with_increment):
      def egcd(a, b):
        if a == 0:
          return b, 0, 1
        else:
          g, y, x = egcd(b % a, a)
          return g, x - (b // a) * y, y
      def modinv(a, m):
        g, x, y = egcd(a, m)
        if g != 1:
          raise Exception('modular inverse does not exist')
        else:
          return x % m
      increment = int(direction_text[len(key_deal_with_increment):])
      special_k = modinv(total_cards, increment)
      return lambda x: (-x * special_k % increment * total_cards + x) // increment
    elif direction_text.startswith(key_cut):
      increment = int(direction_text[len(key_cut):])
      return lambda x: (x + increment) % total_cards
    elif direction_text == key_deal_into_new_stack:
      return lambda x: total_cards - x - 1
    else:
      raise ValueError(direction_text)
  transform_functions = list(reversed([parse_into_transform_function(d) for d in directions.split('\n')]))
  result = card_index_to_return
  for i in range(shuffle_iterations):
    for transform in transform_functions:
      result = transform(result)
  return result


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
