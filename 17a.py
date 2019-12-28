# ref: https://adventofcode.com/2019/day/17
import unittest


def main(inp):
  computer = IntcodeComputer(inp)
  output = ''
  try:
    while True:
      output += chr(computer.run(None))
  except HaltError:
    pass
  output = output.split('\n')
  def is_crossing(x,y):
    if x <= 0 or x >= len(output[0])-1 or y <= 0 or y >= len(output)-1:
      return False
    return output[y-1][x-1] == '.' and output[y-1][x] == '#' and output[y-1][x+1] == '.'\
           and output[y][x-1] == '#' and output[y][x] == '#' and output[y][x+1] == '#'\
           and output[y+1][x-1] == '.' and output[y+1][x] == '#' and output[y+1][x+1] == '.'
  result = 0
  for y1 in range(len(output)):
    for x1 in range(len(output[y1])):
      if is_crossing(x1, y1):
        result += x1 * y1
  return result


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


class Test17(unittest.TestCase):
  def test_example(self):
    self.assertEqual(1, main('104,46,104,35,104,46,104,10,104,35,104,35,104,35,104,10,104,46,104,35,104,46,99'))


if __name__ == '__main__':
  with open('17.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
