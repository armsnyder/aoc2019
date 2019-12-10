# ref: https://adventofcode.com/2019/day/7
import unittest
import itertools


def main(inp):
  def run_with_config(inp1, phase_settings):
    amps = [IntcodeComputer(inp1) for _ in range(len(phase_settings))]
    for i in range(len(phase_settings)):
      amps[i].input(phase_settings[i])
    prev_output = 0
    while True:
      for amp in amps:
        amp.input(prev_output)
        cur_output = amp.output()
        if cur_output is None:
          return prev_output
        prev_output = cur_output
  return max(run_with_config(inp, configs) for configs in itertools.permutations(range(5, 10), 5))


class IntcodeComputer:
  def __init__(self, program: str):
    self.data = [int(x) for x in program.split(',')]
    self.index = 0
    self.input_queue = []

  def input(self, value):
    self.input_queue.append(value)

  def output(self):
    rules = [
      {'opcode': 99, 'params': 0, 'fn': lambda args: args['halt']()},
      {'opcode': 1, 'params': 3, 'fn': lambda args: args['write'](3, args['read'](1) + args['read'](2))},
      {'opcode': 2, 'params': 3, 'fn': lambda args: args['write'](3, args['read'](1) * args['read'](2))},
      {'opcode': 3, 'params': 1, 'fn': lambda args: args['write'](1, args['input']())},
      {'opcode': 4, 'params': 1, 'fn': lambda args: args['output'](1)},
      {'opcode': 5, 'params': 2, 'fn': lambda args: args['jump'](args['read'](2)) if args['read'](1) != 0 else None},
      {'opcode': 6, 'params': 2, 'fn': lambda args: args['jump'](args['read'](2)) if args['read'](1) == 0 else None},
      {'opcode': 7, 'params': 3, 'fn': lambda args: args['write'](3, 1) if args['read'](1) < args['read'](2) else args['write'](3, 0)},
      {'opcode': 8, 'params': 3, 'fn': lambda args: args['write'](3, 1) if args['read'](1) == args['read'](2) else args['write'](3, 0)}
    ]
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
        if modes[pos-1] == 0:
          return self.data[self.data[self.index+pos]]
        else:
          return self.data[self.index+pos]
      def write(pos, value):
        self.data[self.data[self.index+pos]] = value
      def output(pos):
        nonlocal this_output
        if modes[pos-1] == 0:
          this_output = self.data[self.data[self.index+pos]]
        else:
          this_output = self.data[self.index+pos]
      def jump(pos):
        nonlocal is_jump
        is_jump = True
        self.index = pos
      def get_next_input():
        return self.input_queue.pop(0)
      rule['fn']({'halt': halt, 'read': read, 'write': write, 'input': get_next_input, 'output': output, 'jump': jump})
      if is_halt:
        return None
      if not is_jump:
        self.index += rule['params']+1
      if this_output is not None:
        return this_output


class Test7(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual(139629729, main('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'))

  def test_example_2(self):
    self.assertEqual(18216, main('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'))


if __name__ == '__main__':
  with open('7.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
