# ref: https://adventofcode.com/2019/day/18
import unittest


def main(inp: str) -> int:
  grid = inp.split('\n')
  def init_and_find_starts():
    nonlocal grid
    for y, line in enumerate(grid):
      for x, c in enumerate(line):
        if c == '@':
          grid[y-1] = grid[y-1][:x-1] + '@#@' + grid[y-1][x+2:]
          grid[y] = grid[y][:x-1] + '###' + grid[y][x+2:]
          grid[y+1] = grid[y+1][:x-1] + '@#@' + grid[y+1][x+2:]
          return (x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)
  def get_next_states(global_state):
    passable_doors = set(x.upper() for x in global_state['inv'])
    next_states = []
    for robot in range(4):
      visited = set()
      queue = [{'loc': global_state['loc'][robot], 'dis': 0, 'inv': ()}]
      while len(queue) > 0:
        search_state = queue.pop(0)
        if search_state['loc'] in visited:
          continue
        visited.add(search_state['loc'])
        loc_x, loc_y = search_state['loc']
        value = grid[loc_y][loc_x]
        next_inv = search_state['inv']
        if value == '#':
          continue
        if value.isupper() and value not in passable_doors:
          continue
        if value.islower() and value not in global_state['inv']:
          next_inv = search_state['inv'] + (value,)
          next_states.append({
            'inv': tuple(sorted(global_state['inv'] + next_inv)),
            'loc': tuple(global_state['loc'][:robot] + (search_state['loc'],) + global_state['loc'][robot+1:]),
            'tra': global_state['tra'] + search_state['dis']})
        for delta in ((-1, 0), (1, 0), (0, -1), (0, 1)):
          next_loc = (loc_x + delta[0], loc_y + delta[1])
          if 0 <= next_loc[1] < len(grid) and 0 <= next_loc[0] < len(grid[0]):
            queue.append({'inv': next_inv, 'loc': next_loc, 'dis': search_state['dis'] + 1})
    return next_states
  visited = {}
  queue = [{'loc': init_and_find_starts(), 'inv': (), 'tra': 0}]
  shortest_path = float("inf")
  while len(queue) > 0:
    state = queue.pop(0)
    visited_key = (state['loc'], state['inv'])
    if visited_key in visited and visited[visited_key] <= state['tra']:
      continue
    visited[visited_key] = state['tra']
    next_states = get_next_states(state)
    if len(next_states) == 0:
      shortest_path = min(shortest_path, state['tra'])
    queue.extend(next_states)
    queue = sorted(queue, key=lambda x: len(x['inv']) * -1000 + x['tra'])
  return shortest_path


class Test18(unittest.TestCase):
  def test_example_8(self):
    self.assertEqual(8, main('''#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######'''))

  def test_example_24(self):
    self.assertEqual(24, main('''###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############'''))

  def test_example_32(self):
    self.assertEqual(32, main('''#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############'''))

  def test_example_72(self):
    self.assertEqual(72, main('''#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############'''))


if __name__ == '__main__':
  with open('18.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
