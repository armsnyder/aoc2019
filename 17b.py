# ref: https://adventofcode.com/2019/day/17
import unittest
from typing import List, Tuple


def render_map(inp: str) -> List[str]:
  output = ''
  def handle_output(x):
    nonlocal output
    output += chr(x)
  IntcodeComputer(inp, None, handle_output).run()
  return output.split('\n')


def get_full_path(scaffold_map: List[str]) -> List[str]:
  UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
  # Find the current location of the bot
  cur_loc = (0, 0)
  for y in range(len(scaffold_map)):
    for x in range(len(scaffold_map[y])):
      if scaffold_map[y][x] == '^':
        cur_loc = (x, y)
  # Point the bot toward the path
  cur_dir = UP
  path = []
  def is_scaffold(x, y):
    return 0 <= y < len(scaffold_map) and 0 <= x < len(scaffold_map[y]) and scaffold_map[y][x] == '#'
  for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
    search_x, search_y = cur_loc[0] + dx, cur_loc[1] + dy
    if is_scaffold(search_x, search_y):
      if (dx, dy) == (-1, 0):
        path.append('L')
        cur_dir = LEFT
      elif (dx, dy) == (1, 0):
        path.append('R')
        cur_dir = RIGHT
      elif (dx, dy) == (0, 1):
        path.extend(['L', 'L'])
        cur_dir = DOWN
  # Traverse the scaffold
  def cast_loc(steps):
    if cur_dir == UP:
      return cur_loc[0], cur_loc[1] - steps
    elif cur_dir == RIGHT:
      return cur_loc[0] + steps, cur_loc[1]
    elif cur_dir == DOWN:
      return cur_loc[0], cur_loc[1] + steps
    else:
      return cur_loc[0] - steps, cur_loc[1]
  def calc_forward_steps():
    steps = 1
    while True:
      search_x, search_y = cast_loc(steps)
      if not is_scaffold(search_x, search_y):
        return steps - 1
      steps += 1
  def get_left_loc():
    if cur_dir == UP:
      return cur_loc[0] - 1, cur_loc[1]
    elif cur_dir == RIGHT:
      return cur_loc[0], cur_loc[1] - 1
    elif cur_dir == DOWN:
      return cur_loc[0] + 1, cur_loc[1]
    else: return cur_loc[0], cur_loc[1] + 1
  def get_right_loc():
    if cur_dir == UP:
      return cur_loc[0] + 1, cur_loc[1]
    elif cur_dir == RIGHT:
      return cur_loc[0], cur_loc[1] + 1
    elif cur_dir == DOWN:
      return cur_loc[0] - 1, cur_loc[1]
    else: return cur_loc[0], cur_loc[1] - 1
  def turn():
    nonlocal cur_dir, path
    turn_loc_x, turn_loc_y = get_left_loc()
    if is_scaffold(turn_loc_x, turn_loc_y):
      path.append('L')
      cur_dir = (cur_dir - 1) % 4
      return True
    turn_loc_x, turn_loc_y = get_right_loc()
    if is_scaffold(turn_loc_x, turn_loc_y):
      path.append('R')
      cur_dir = (cur_dir + 1) % 4
      return True
    return False
  while True:
    steps = calc_forward_steps()
    path.append(str(steps))
    cur_loc = cast_loc(steps)
    if not turn():
      return path


def get_directions(pattern: str, parts: List[List[str]]) -> str:
  return '\n'.join([','.join(part) for part in [pattern, *parts]]) + '\n'


def factorize_path(full_path: List[str]) -> Tuple[str, List[List[str]]]:
  def find_matches(sub_path: List[str]) -> List[int]:
    matches = []
    i = 0
    while i < len(full_path):
      if full_path[i] == sub_path[0] and full_path[i:i+len(sub_path)] == sub_path:
        matches.append(i)
        i += len(sub_path)
      else:
        i += 1
    return matches
  def extract_part_at_index(index: int) -> Tuple[List[str], List[int]]:
    size = 10  # Max size when not including commas
    while True:
      sub_path = full_path[index:index+size]
      if len(','.join(sub_path)) <= 20:
        matches = find_matches(sub_path)
        if len(matches) > 1:
          return sub_path, matches
      size -= 2  # Group by 2 for path aesthetic purposes only
  claimed_parts: List[Tuple[str, int, int]] = []
  result_parts: List[List[str]] = []
  def get_next_available_index() -> int:
    last_end = 0
    for _, start, end in claimed_parts:
      if start != last_end:
        break
      last_end = end
    return last_end
  for letter in 'ABC':
    next_available_index = get_next_available_index()
    part, indices = extract_part_at_index(next_available_index)
    result_parts.append(part)
    claimed_parts.extend((letter, x, x + len(part)) for x in indices)
    claimed_parts = sorted(claimed_parts, key=lambda x: x[1])
  return ''.join(x[0] for x in claimed_parts), result_parts


def collect_dust(program: str, directions: str) -> int:
  directions += 'n\n'
  output = 0
  def handle_output(x):
    nonlocal output
    output = x
  directions_index = 0
  def handle_input():
    nonlocal directions_index
    directions_index += 1
    return ord(directions[directions_index-1])
  IntcodeComputer('2' + program[1:], handle_input, handle_output).run()
  return output


def main(inp):
  return collect_dust(inp, get_directions(*factorize_path(get_full_path(render_map(inp)))))


class IntcodeComputer:
  def __init__(self, program: str, handle_input, handle_output):
    self.data = [int(x) for x in program.split(',')]
    self.index = 0
    self.offset = 0
    self.memory = {}
    self.handle_input = handle_input
    self.handle_output = handle_output

  def run(self):
    rules = [
      {'opcode': 99, 'params': 0, 'fn': lambda args: args['halt']()},
      {'opcode': 1, 'params': 3, 'fn': lambda args: args['write'](3, args['read'](1) + args['read'](2))},
      {'opcode': 2, 'params': 3, 'fn': lambda args: args['write'](3, args['read'](1) * args['read'](2))},
      {'opcode': 3, 'params': 1, 'fn': lambda args: args['write'](1, args['input']())},
      {'opcode': 4, 'params': 1, 'fn': lambda args: args['output'](1)},
      {'opcode': 5, 'params': 2, 'fn': lambda args: args['jump'](args['read'](2)) if args['read'](1) != 0 else None},
      {'opcode': 6, 'params': 2, 'fn': lambda args: args['jump'](args['read'](2)) if args['read'](1) == 0 else None},
      {'opcode': 7, 'params': 3, 'fn': lambda args: args['write'](3, 1) if args['read'](1) < args['read'](2) else args['write'](3, 0)},
      {'opcode': 8, 'params': 3, 'fn': lambda args: args['write'](3, 1) if args['read'](1) == args['read'](2) else args['write'](3, 0)},
      {'opcode': 9, 'params': 1, 'fn': lambda args: args['offset'](args['read'](1))}
    ]
    while True:
      opcode = self.data[self.index] % 100
      modes = list(int(x) for x in reversed(f'{self.data[self.index]:06}'))[2:]
      rule = [x for x in rules if x['opcode'] == opcode][0]
      is_jump = False
      is_halt = False
      def halt():
        nonlocal is_halt
        is_halt = True
      def read(pos):
        mode = modes[pos-1]
        i = self.data[self.index+pos] if mode == 0 else self.index+pos if mode == 1 else self.data[self.index+pos]+self.offset
        if i >= len(self.data):
          if i not in self.memory:
            return 0
          return self.memory[i]
        return self.data[i]
      def write(pos, value):
        mode = modes[pos-1]
        i = self.data[self.index+pos] if mode == 0 else self.index+pos if mode == 1 else self.data[self.index+pos]+self.offset
        if i >= len(self.data):
          self.memory[i] = value
        else:
          self.data[i] = value
      def output(pos):
        mode = modes[pos-1]
        i = self.data[self.index+pos] if mode == 0 else self.index+pos if mode == 1 else self.data[self.index+pos]+self.offset
        if i > len(self.data):
          this_output = self.memory[i]
        else:
          this_output = self.data[i]
        self.handle_output(this_output)
      def jump(pos):
        nonlocal is_jump
        is_jump = True
        self.index = pos
      def offset(val):
        self.offset += val
      args1 = {
        'halt': halt,
        'read': read,
        'write': write,
        'input': self.handle_input,
        'output': output,
        'jump': jump,
        'offset': offset,
      }
      rule['fn'](args1)
      if not is_jump:
        self.index += rule['params']+1
      if is_halt:
        return


class Test17(unittest.TestCase):
  def test_render_map(self):
    self.assertEqual(['.#.', '###', '.#.'], render_map('104,46,104,35,104,46,104,10,104,35,104,35,104,35,104,10,104,46,104,35,104,46,99'))

  def test_get_full_path(self):
    self.assertEqual(['R','8','R','8','R','4','R','4','R','8','L','6','L','2','R','4','R','4','R','8','R','8','R','8','L','6','L','2'],
      get_full_path('''#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......'''.split('\n')))

  def test_get_directions(self):
    self.assertEqual('''A,B,C,B,A,C
R,8,R,8
R,4,R,4,R,8
L,6,L,2
''', get_directions('ABCBAC', [['R','8','R','8'],['R','4','R','4','R','8'],['L','6','L','2']]))

  def test_factorize_path(self):
    self.assertEqual(('ABCBAC', [['R','8','R','8'],['R','4','R','4','R','8'],['L','6','L','2']]), factorize_path(['R','8','R','8','R','4','R','4','R','8','L','6','L','2','R','4','R','4','R','8','R','8','R','8','L','6','L','2']))

  def test_factorize_path_with_real_thing(self):
    full_path = ['L','10','L','6','R','10','R','6','R','8','R','8','L','6','R','8','L','10','L','6','R','10','L','10','R','8','R','8','L','10','R','6','R','8','R','8','L','6','R','8','L','10','R','8','R','8','L','10','R','6','R','8','R','8','L','6','R','8','L','10','L','6','R','10','L','10','R','8','R','8','L','10','R','6','R','8','R','8','L','6','R','8']
    pattern, parts = factorize_path(full_path)
    self.assertLessEqual(len(','.join(pattern)), 20)
    for part in parts:
      self.assertLessEqual(len(','.join(part)), 20)
    reconstructed_path = []
    for c in pattern:
      reconstructed_path.extend(parts[{'A':0,'B':1,'C':2}[c]])
    self.assertEqual(reconstructed_path, full_path)


if __name__ == '__main__':
  with open('17.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
