# ref: https://adventofcode.com/2019/day/22
from typing import List, Tuple

Deck = List[int]
ScaleShift = Tuple[int, int]


def locate_card_after_shuffle(directions: str, total_cards: int, card_index_to_return: int,
                              shuffle_iterations: int) -> int:
  one_shuffle_operation = combine_directions_into_single_operation(directions, total_cards)
  all_shuffles_operation = operation_power(one_shuffle_operation, shuffle_iterations, total_cards)
  scale, shift = all_shuffles_operation
  # Inversion of scale * card_index_to_return + shift:
  return modinv(scale, total_cards) * (card_index_to_return - shift) % total_cards


def combine_directions_into_single_operation(directions: str, m: int) -> ScaleShift:
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

  return combine_operations([parse_direction(x) for x in directions.split('\n')], m)


def combine_operations(scale_shifts: List[ScaleShift], m: int) -> ScaleShift:
  result = scale_shifts[0]
  for next_op in scale_shifts[1:]:
    result = result[0] * next_op[0] % m, (next_op[0] * result[1] + next_op[1]) % m
  return result


def operation_power(operation: ScaleShift, n: int, m: int) -> ScaleShift:
  scale, shift = operation
  result_scale = pow(scale, n, m)
  result_shift = (shift % m) * (1 - pow(scale, n, m)) % m * modinv(1 - scale, m) % m  # Sum of a geometric series
  return result_scale, result_shift


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


if __name__ == '__main__':
  with open('22.txt', 'r') as f:
    contents = f.read()
  print(locate_card_after_shuffle(contents.strip(), 119315717514047, 2020, 101741582076661))
