# ref: https://adventofcode.com/2019/day/24
import unittest
from typing import Tuple, Dict

BoardLevel = Tuple[Tuple[bool, ...], ...]
Board = Dict[int, BoardLevel]


def main(inp: str, minutes: int) -> int:
  board: Board = {
    -1: tuple([tuple([False] * 5)] * 5),
    0: tuple(tuple(c == '#' for c in line) for line in inp.split('\n')),
    1: tuple([tuple([False] * 5)] * 5)
  }

  def count_adjacent(level: int, i: int, j: int) -> int:
    if i == 2 and j == 2:
      return 0  # Center is discounted

    def count_inner(i_offset1, j_offset1):
      if level - 1 not in board:
        return 0
      if i_offset1 == 1:
        return sum(board[level - 1][0])
      elif i_offset1 == -1:
        return sum(board[level - 1][4])
      elif j_offset1 == 1:
        return sum(board[level - 1][i1][0] for i1 in range(5))
      elif j_offset1 == -1:
        return sum(board[level - 1][i1][4] for i1 in range(5))
      else:
        raise ValueError(i_offset1, j_offset1)

    def count_outer(i_offset1, j_offset1):
      if level + 1 not in board:
        return 0
      if i_offset1 == 1:
        return board[level + 1][3][2]
      elif i_offset1 == -1:
        return board[level + 1][1][2]
      elif j_offset1 == 1:
        return board[level + 1][2][3]
      elif j_offset1 == -1:
        return board[level + 1][2][1]
      else:
        raise ValueError(i_offset1, j_offset1)

    total = 0
    for i_offset, j_offset in ((-1, 0), (1, 0), (0, -1), (0, 1)):
      target_i = i + i_offset
      target_j = j + j_offset
      if target_i == 2 and target_j == 2:
        total += count_inner(i_offset, j_offset)
      elif 0 <= target_i < 5 and 0 <= target_j < 5:
        total += int(board[level][target_i][target_j])
      else:
        total += count_outer(i_offset, j_offset)
    return total

  def is_alive(starts_alive: bool, adjacent: int) -> bool:
    return False if starts_alive and adjacent != 1 \
      else True if not starts_alive and 1 <= adjacent <= 2 \
      else starts_alive

  def update() -> Board:
    next_board = {}
    min_level, max_level = 0, 0
    for level, board_level in board.items():
      min_level = min(min_level, level)
      max_level = max(max_level, level)
      next_board[level] = tuple(tuple(is_alive(board_level[i][j], count_adjacent(level, i, j))
                                      for j in range(5)) for i in range(5))
    if any(any(row) for row in board[min_level]):
      next_board[min_level - 1] = tuple([tuple([False] * 5)] * 5)
    if any(any(row) for row in board[max_level]):
      next_board[max_level + 1] = tuple([tuple([False] * 5)] * 5)
    return next_board

  for _ in range(minutes):
    board = update()

  return sum(sum(sum(level[i][j] and not (i == 2 and j == 2) for j in range(5)) for i in range(5))
             for level in board.values())


class Test24(unittest.TestCase):
  def test_example(self):
    self.assertEqual(99, main('''....#
#..#.
#..##
..#..
#....''', 10))


if __name__ == '__main__':
  with open('24.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip(), 200))
