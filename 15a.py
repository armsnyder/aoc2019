# ref: https://adventofcode.com/2019/day/15
from typing import Dict, Tuple


def walk_maze(intcode_program: str) -> Tuple[Dict[Tuple[int, int],int], Tuple[int, int]]:
  computer = IntcodeComputer(intcode_program)
  visited = {(0,0):1}
  tail = []
  loc = (0,0)
  oxygen_loc = (0,0)
  def movable_locations():
    return {1: (loc[0],loc[1]+1), 2: (loc[0],loc[1]-1), 3: (loc[0]-1,loc[1]), 4: (loc[0]+1,loc[1])}
  def move() -> bool:
    nonlocal oxygen_loc, loc
    for direction, target_loc in movable_locations().items():
      if target_loc in visited:
        continue
      status = computer.run(direction)
      visited[target_loc] = status
      if status == 2:
        oxygen_loc = target_loc
      if status != 0:
        tail.append(direction)
        loc = target_loc
        return True
    return False
  def run():
    nonlocal loc
    if not move():
      direction = {1: 2, 2: 1, 3: 4, 4: 3}[tail.pop()]
      target_loc = movable_locations()[direction]
      if computer.run(direction) == 0:
        raise ValueError
      loc = target_loc
  run()
  while len(tail) > 0:
    run()
  return visited, oxygen_loc


def get_distance(maze: Dict[Tuple[int, int],int], loc1: Tuple[int, int], loc2: Tuple[int, int]) -> int:
  visited = set()
  queue = [(loc1, 0)]
  while len(queue) > 0:
    loc, distance = queue.pop(0)
    if loc in visited:
      continue
    visited.add(loc)
    if loc == loc2:
      return distance
    queue.extend([(x, distance+1) for x in [(loc[0],loc[1]+1), (loc[0],loc[1]-1), (loc[0]-1,loc[1]), (loc[0]+1,loc[1])] if x in maze and maze[x] != 0])
  raise ValueError


def main(inp):
  maze, oxygen_loc = walk_maze(inp)
  return get_distance(maze, (0,0), oxygen_loc)


class IntcodeComputer:
  def __init__(self, program: str):
    self.data = [int(x) for x in program.split(',')]
    self.index = 0
    self.offset = 0
    self.memory = {}

  def run(self, inp) -> int:
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
      this_output = None
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


if __name__ == '__main__':
  with open('15.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
