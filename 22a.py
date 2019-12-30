# ref: https://adventofcode.com/2019/day/22
import unittest
from typing import List


Deck = List[int]


def main(inp: str) -> int:
  return shuffle(list(range(10007)), inp).index(2019)


def shuffle(deck: Deck, directions: str) -> Deck:
  def deal_with_increment(deck1: Deck, increment: int) -> Deck:
    result = [0]*len(deck1)
    for i in range(len(deck1)):
      result[(i * increment) % len(deck1)] = deck1[i]
    return result
  def deal_into_new_stack(deck1: Deck) -> Deck:
    return list(reversed(deck1))
  def cut(deck1: Deck, amount: int) -> Deck:
    return deck1[amount:] + deck1[:amount]
  for direction in directions.split('\n'):
    key_deal_with_increment = 'deal with increment '
    key_cut = 'cut '
    if direction.startswith(key_deal_with_increment):
      deck = deal_with_increment(deck, int(direction[len(key_deal_with_increment):]))
    elif direction.startswith(key_cut):
      deck = cut(deck, int(direction[len(key_cut):]))
    elif direction == 'deal into new stack':
      deck = deal_into_new_stack(deck)
    else:
      raise ValueError(direction)
  return deck


class Test22(unittest.TestCase):
  def test_deal_into_new_stack(self):
    self.assertEqual([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], shuffle(list(range(10)), 'deal into new stack'))

  def test_cut(self):
    self.assertEqual([3, 4, 5, 6, 7, 8, 9, 0, 1, 2], shuffle(list(range(10)), 'cut 3'))

  def test_cut_negative(self):
    self.assertEqual([6, 7, 8, 9, 0, 1, 2, 3, 4, 5], shuffle(list(range(10)), 'cut -4'))

  def test_deal_with_increment(self):
    self.assertEqual([0, 7, 4, 1, 8, 5, 2, 9, 6, 3], shuffle(list(range(10)), 'deal with increment 3'))

  def test_example_1(self):
    self.assertEqual(
      [0, 3, 6, 9, 2, 5, 8, 1, 4, 7],
      shuffle(list(range(10)), '''deal with increment 7
deal into new stack
deal into new stack'''))

  def test_example_2(self):
    self.assertEqual(
      [3, 0, 7, 4, 1, 8, 5, 2, 9, 6],
      shuffle(list(range(10)), '''cut 6
deal with increment 7
deal into new stack'''))

  def test_example_3(self):
    self.assertEqual(
      [6, 3, 0, 7, 4, 1, 8, 5, 2, 9],
      shuffle(list(range(10)), '''deal with increment 7
deal with increment 9
cut -2'''))

  def test_example_4(self):
    self.assertEqual(
      [9, 2, 5, 8, 1, 4, 7, 0, 3, 6],
      shuffle(list(range(10)), '''deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1'''))


if __name__ == '__main__':
  with open('22.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
