# ref: https://adventofcode.com/2019/day/11
import unittest
from typing import Dict, Tuple, Optional


def main(inp: str) -> int:
  coords: Tuple[int, int] = (0,0)
  facing: int = 0
  grid: Dict[Tuple[int, int], int] = {}
  computer = IntcodeComputer(inp)
  while True:
    color = grid[coords] if coords in grid else 0
    try:
      grid[coords] = computer.run(color)
      facing = (facing + (computer.run(None) * 2 - 1)) % 4
    except HaltError:
      return len(grid)
    if facing == 0:
      coords = (coords[0], coords[1]-1)
    elif facing == 1:
      coords = (coords[0]+1, coords[1])
    elif facing == 2:
      coords = (coords[0], coords[1]+1)
    else:
      coords = (coords[0]-1, coords[1])


class IntcodeComputer:
  def __init__(self, program: str):
    self.data = [int(x) for x in program.split(',')]
    self.index = 0
    self.offset = 0
    self.memory = {}

  def run(self, inp: Optional[int]) -> int:
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
    has_read_input = False
    while True:
      opcode = self.data[self.index] % 100
      modes = list(int(x) for x in reversed(f'{self.data[self.index]:06}'))[2:]
      rule = [x for x in rules if x['opcode'] == opcode][0]
      is_jump = False
      this_output: Optional[int] = None
      def halt():
        raise HaltError
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
        nonlocal this_output
        mode = modes[pos-1]
        i = self.data[self.index+pos] if mode == 0 else self.index+pos if mode == 1 else self.data[self.index+pos]+self.offset
        if i > len(self.data):
          this_output = self.memory[i]
        else:
          this_output = self.data[i]
      def jump(pos):
        nonlocal is_jump
        is_jump = True
        self.index = pos
      def get_next_input():
        nonlocal has_read_input
        if has_read_input or inp is None:
          raise InputError
        has_read_input = True
        return inp
      def offset(val):
        self.offset += val
      args1 = {
        'halt': halt,
        'read': read,
        'write': write,
        'input': get_next_input,
        'output': output,
        'jump': jump,
        'offset': offset,
      }
      rule['fn'](args1)
      if not is_jump:
        self.index += rule['params']+1
      if this_output is not None:
        return this_output


class InputError(ValueError):
  pass


class HaltError(ValueError):
  pass


class Test11(unittest.TestCase):
  def test_box(self):
    self.assertEqual(4, main('3,50,104,1,104,1,1006,50,0,99'))


if __name__ == '__main__':
  with open('11.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
