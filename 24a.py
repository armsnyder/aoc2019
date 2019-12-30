# ref: https://adventofcode.com/2019/day/24
import unittest
from typing import Set, Tuple

Board = Tuple[Tuple[bool, ...], ...]


def main(inp: str) -> int:
  board: Board = tuple(tuple(c == '#' for c in line) for line in inp.split('\n'))

  def count_adjacent(i: int, j: int) -> int:
    return sum(1 for i1, j1 in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)) if
               0 <= i1 < len(board) and 0 <= j1 < len(board[0]) and board[i1][j1])

  def is_alive(starts_alive: bool, adjacent: int) -> bool:
    return False if starts_alive and adjacent != 1 \
      else True if not starts_alive and 1 <= adjacent <= 2 \
      else starts_alive

  def update() -> Board:
    return tuple(tuple(is_alive(board[i][j], count_adjacent(i, j))
                       for j in range(len(board[i]))) for i in range(len(board)))

  def score() -> int:
    return sum(2 ** n
               for n, (i, j)
               in enumerate((i, j) for i in range(len(board)) for j in range(len(board)))
               if board[i][j])

  seen: Set[Board] = set()
  while True:
    board = update()
    if board in seen:
      return score()
    seen.add(board)


class Test24(unittest.TestCase):
  def test_example(self):
    self.assertEqual(2129920, main('''....#
#..#.
#..##
..#..
#....'''))


if __name__ == '__main__':
  with open('24.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
