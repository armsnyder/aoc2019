# ref: https://adventofcode.com/2019/day/9
import unittest


def main(inp):
  return ','.join(str(x) for x in IntcodeComputer(inp).run(2))


class IntcodeComputer:
  def __init__(self, program: str):
    self.data = [int(x) for x in program.split(',')]
    self.index = 0
    self.offset = 0
    self.memory = {}

  def run(self, inp):
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
      is_halt = False
      is_jump = False
      this_output = None
      def halt():
        nonlocal is_halt
        is_halt = True
      def read(pos):
        mode = modes[pos-1]
        i = self.data[self.index+pos] if mode == 0 else self.index+pos if mode == 1 else self.data[self.index+pos]+self.offset
        if i > len(self.data):
          if i not in self.memory:
            return 0
          return self.memory[i]
        return self.data[i]
      def write(pos, value):
        mode = modes[pos-1]
        i = self.data[self.index+pos] if mode == 0 else self.index+pos if mode == 1 else self.data[self.index+pos]+self.offset
        if i > len(self.data):
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
      try:
        rule['fn'](args1)
      except InputError:
        return
      if is_halt:
        return
      if not is_jump:
        self.index += rule['params']+1
      if this_output is not None:
        yield this_output


class InputError(ValueError):
  pass


class Test9(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], list(IntcodeComputer('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99').run(None)))

  def test_example_2(self):
    self.assertEqual([1219070632396864], list(IntcodeComputer('1102,34915192,34915192,7,4,7,99,0').run(None)))

  def test_example_3(self):
    self.assertEqual([1125899906842624], list(IntcodeComputer('104,1125899906842624,99').run(None)))


if __name__ == '__main__':
  with open('9.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
