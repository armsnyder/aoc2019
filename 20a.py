# ref: https://adventofcode.com/2019/day/20
import unittest


def main(inp: str) -> int:
  grid = inp.split('\n')
  def in_bounds(x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])
  def is_path(x, y):
    return in_bounds(x, y) and grid[y][x] == '.'
  def get_warps_by_name():
    def get_label(x, y):
      def is_letter(x, y):
        return in_bounds(x, y) and grid[y][x].isupper()
      if is_letter(x-1, y):
        return grid[y][x-2:x]
      if is_letter(x+1, y):
        return grid[y][x+1:x+3]
      if is_letter(x, y-1):
        return grid[y-2][x] + grid[y-1][x]
      if is_letter(x, y+1):
        return grid[y+1][x] + grid[y+2][x]
      return None
    warps = {}
    for y in range(len(grid)):
      for x in range(len(grid[0])):
        if is_path(x, y):
          label = get_label(x, y)
          if label is not None:
            if label not in warps:
              warps[label] = []
            warps[label].append((x, y))
    return warps
  warps_by_name = get_warps_by_name()
  def get_warp_map():
    warps = {}
    for cells in warps_by_name.values():
      if len(cells) == 2:
        warps[cells[0]] = cells[1]
        warps[cells[1]] = cells[0]
    return warps
  warp_map = get_warp_map()
  def get_adjacent_cells(x, y):
    cells = [(x2, y2) for x2, y2 in ((x-1,y), (x+1,y), (x,y-1), (x,y+1)) if is_path(x2, y2)]
    if (x, y) in warp_map:
      cells.append(warp_map[(x, y)])
    return cells
  queue = [(warps_by_name['AA'][0], 0)]
  visited = set()
  while len(queue) > 0:
    cell, dist = queue.pop(0)
    if cell in visited:
      continue
    visited.add(cell)
    if cell == warps_by_name['ZZ'][0]:
      return dist
    queue.extend((c, dist+1) for c in get_adjacent_cells(*cell))


class Test20(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual(23, main('''         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       '''))

  def test_example_2(self):
    self.assertEqual(58, main('''                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               '''))


if __name__ == '__main__':
  with open('20.txt', 'r') as f:
    contents = f.read()
  print(main(contents[:-1]))
