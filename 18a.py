# ref: https://adventofcode.com/2019/day/18
import unittest


def main(inp: str) -> int:
  grid = inp.split('\n')
  def find_start():
    for y, line in enumerate(grid):
      for x, c in enumerate(line):
        if c == '@':
          return x, y
  def get_reachable_keys(global_state):
    passable_doors = set(x.upper() for x in global_state['inv'])
    reachable_keys = []
    visited = set()
    queue = [{'loc': global_state['loc'], 'dis': 0, 'inv': ()}]
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
        reachable_keys.append({'inv': next_inv, 'loc': search_state['loc'], 'dis': search_state['dis']})
      for delta in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        next_loc = (loc_x + delta[0], loc_y + delta[1])
        if 0 <= next_loc[1] < len(grid) and 0 <= next_loc[0] < len(grid[0]):
          queue.append({'inv': next_inv, 'loc': next_loc, 'dis': search_state['dis'] + 1})
    return reachable_keys
  visited = {}
  queue = [{'loc': find_start(), 'inv': (), 'tra': 0}]
  shortest_path = float("inf")
  while len(queue) > 0:
    state = queue.pop(0)
    visited_key = (state['loc'], state['inv'])
    if visited_key in visited and visited[visited_key] <= state['tra']:
      continue
    visited[visited_key] = state['tra']
    reachable_keys = get_reachable_keys(state)
    if len(reachable_keys) == 0:
      shortest_path = min(shortest_path, state['tra'])
    queue.extend({'loc': key['loc'], 'inv': tuple(sorted(state['inv'] + key['inv'])), 'tra': state['tra'] + key['dis']} for key in reachable_keys)
    queue = sorted(queue, key=lambda x: len(x['inv']) * -1000 + x['tra'])
  return shortest_path


class Test18(unittest.TestCase):
  def test_example_8(self):
    self.assertEqual(8, main('''#########
#b.A.@.a#
#########'''))

  def test_example_86(self):
    self.assertEqual(86, main('''########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################'''))

  def test_example_132(self):
    self.assertEqual(132, main('''########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################'''))

  def test_example_136(self):
    self.assertEqual(136, main('''#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################'''))

  def test_example_81(self):
    self.assertEqual(81, main('''########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################'''))


if __name__ == '__main__':
  with open('18.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
