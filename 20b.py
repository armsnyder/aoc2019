# ref: https://adventofcode.com/2019/day/20
import unittest
from typing import Tuple, List, Dict, Optional, Generator


Cell = Tuple[int, int, int]
Portal = Tuple[int, int, bool]


class Maze:
  def __init__(self, inp: str):
    self.__grid = inp.split('\n')
    self.__portal_map: Dict[Portal, Portal] = {}
    self.__portals_by_name: Dict[str, List[Portal]] = {}
    def is_inner_portal(x1, y1) -> bool:
      return 3 <= y1 < len(self.__grid) - 3 and 3 <= x1 < len(self.__grid[y1]) - 3
    def get_label(x1, y1) -> Optional[str]:
      def is_letter(x2, y2):
        return self.__in_bounds(x2, y2) and self.__grid[y2][x2].isupper()
      if is_letter(x1 - 1, y1):
        return self.__grid[y1][x1 - 2:x1]
      if is_letter(x1 + 1, y1):
        return self.__grid[y1][x1 + 1:x1 + 3]
      if is_letter(x1, y1 - 1):
        return self.__grid[y1 - 2][x1] + self.__grid[y1 - 1][x1]
      if is_letter(x1, y1 + 1):
        return self.__grid[y1 + 1][x1] + self.__grid[y1 + 2][x1]
      return None
    for y in range(len(self.__grid)):
      for x in range(len(self.__grid[y])):
        if self.__is_path(x, y):
          label = get_label(x, y)
          if label is not None:
            if label not in self.__portals_by_name:
              self.__portals_by_name[label] = []
            self.__portals_by_name[label].append((x, y, is_inner_portal(x, y)))
    for portal_name, portal_pair in self.__portals_by_name.items():
      if len(portal_pair) == 2:
        if portal_pair[0][2] == portal_pair[1][2]:
          raise ValueError(portal_name, portal_pair)
        self.__portal_map[portal_pair[0]] = portal_pair[1]
        self.__portal_map[portal_pair[1]] = portal_pair[0]

  @property
  def start_cell(self) -> Cell:
    x, y, _ = self.__portals_by_name['AA'][0]
    return x, y, 0

  @property
  def end_cell(self) -> Cell:
    x, y, _ = self.__portals_by_name['ZZ'][0]
    return x, y, 0

  def __in_bounds(self, x: int, y: int) -> bool:
    return 0 <= y < len(self.__grid) and 0 <= x < len(self.__grid[y])

  def __is_path(self, x: int, y: int) -> bool:
    return self.__in_bounds(x, y) and self.__grid[y][x] == '.'

  def get_adjacent_cells(self, cell: Cell) -> List[Cell]:
    x, y, layer = cell
    if not self.__is_path(x, y):
      raise ValueError
    cells = [(x2, y2, layer) for x2, y2 in ((x-1,y), (x+1,y), (x,y-1), (x,y+1)) if self.__is_path(x2, y2)]
    if layer > 0 and (x, y, False) in self.__portal_map:
      target_x, target_y, _ = self.__portal_map[(x, y, False)]
      cells.append((target_x, target_y, layer-1))
    elif (x, y, True) in self.__portal_map:
      target_x, target_y, _ = self.__portal_map[(x, y, True)]
      cells.append((target_x, target_y, layer+1))
    return cells


def main(inp: str) -> int:
  maze = Maze(inp)
  def search(start: Cell, my_visited: Dict[Cell, int], their_visited: Dict[Cell, int]) -> Generator[int, None, None]:
    queue: List[Tuple[Cell, int]] = [(start, 0)]
    while len(queue) > 0:
      cell, dist = queue.pop(0)
      if cell in my_visited:
        continue
      my_visited[cell] = dist
      queue.extend((c, dist+1) for c in maze.get_adjacent_cells(cell))
      yield dist + their_visited[cell] if cell in their_visited else None
  def race(gen_a: Generator[Optional[int], None, None], gen_b: Generator[Optional[int], None, None]) -> int:
    while True:
      for gen in (gen_a, gen_b):
        value = next(gen)
        if value is not None:
          return value
  visited_a: Dict[Cell, int] = {}
  visited_b: Dict[Cell, int] = {}
  # Find the minimum path length by performing a bi-directional breadth-first-search:
  return race(search(maze.start_cell, visited_a, visited_b), search(maze.end_cell, visited_b, visited_a))


class Test20(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual(1, main('''AA..ZZ'''))

  def test_example_6(self):
    self.assertEqual(6, main('''
             
             
  #########  
AA..BC   #.ZZ
  ##   DE..BC
  ##     #.DE
  #########  
             
             '''[1:]))

  def test_example_12(self):
    self.assertEqual(12, main('''
             
             
  #########  
AA..BC   #.ZZ
  ##     #.FG
BC..DE FG..DE
  #########  
             
             '''[1:]))

  def test_example_16(self):
    self.assertEqual(16, main('''
          D   
          E   
  ########.#  
AA..BC   #..ZZ
  ##     #.#  
  #.DE FG...FG
  #.########  
   B          
   C          '''[1:]))

  def test_example_396(self):
    self.assertEqual(396, main('''
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     '''[1:]))


if __name__ == '__main__':
  with open('20.txt', 'r') as f:
    contents = f.read()
  print(main(contents[:-1]))
