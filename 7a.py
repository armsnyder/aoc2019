# ref: https://adventofcode.com/2019/day/7
import unittest
import itertools


def main(inp):
  def compute(program, inputs):
    rules = [
      {'opcode': 99, 'params': 0, 'fn': lambda args: args['halt']()},
      {'opcode': 1, 'params': 3, 'fn': lambda args: args['write'](3, args['read'](1) + args['read'](2))},
      {'opcode': 2, 'params': 3, 'fn': lambda args: args['write'](3, args['read'](1) * args['read'](2))},
      {'opcode': 3, 'params': 1, 'fn': lambda args: args['write'](1, args['input']())},
      {'opcode': 4, 'params': 1, 'fn': lambda args: args['output'](1)},
      {'opcode': 5, 'params': 2, 'fn': lambda args: args['jump'](args['read'](2)) if args['read'](1) != 0 else None},
      {'opcode': 6, 'params': 2, 'fn': lambda args: args['jump'](args['read'](2)) if args['read'](1) == 0 else None},
      {'opcode': 7, 'params': 3, 'fn': lambda args: args['write_abs'](args['read_immediate'](3), 1) if args['read'](1) < args['read'](2) else args['write_abs'](args['read_immediate'](3), 0)},
      {'opcode': 8, 'params': 3, 'fn': lambda args: args['write_abs'](args['read_immediate'](3), 1) if args['read'](1) == args['read'](2) else args['write_abs'](args['read_immediate'](3), 0)}
    ]
    data = [int(x) for x in program.split(',')]
    i = 0
    last_output = 0
    input_index = 0
    while True:
      opcode = data[i] % 100
      modes = list(int(x) for x in reversed(f'{data[i]:06}'))[2:]
      rule = [x for x in rules if x['opcode'] == opcode][0]
      is_halt = False
      is_jump = False
      def halt():
        nonlocal is_halt
        is_halt = True
      def read(pos):
        if modes[pos-1] == 0:
          return data[data[i+pos]]
        else:
          return data[i+pos]
      def read_immediate(pos):
        return data[i+pos]
      def write(pos, value):
        nonlocal data
        data[data[i+pos]] = value
      def write_abs(pos, value):
        nonlocal data
        data[pos] = value
      def output(pos):
        nonlocal last_output
        if modes[pos-1] == 0:
          last_output = data[data[i+pos]]
        else:
          last_output = data[i+pos]
      def jump(pos):
        nonlocal is_jump, i
        is_jump = True
        i = pos
      def get_next_input():
        nonlocal input_index
        next_input = inputs[input_index]
        input_index += 1
        return next_input
      rule['fn']({'halt': halt, 'read': read, 'write': write, 'input': get_next_input, 'output': output, 'jump': jump, 'read_immediate': read_immediate, 'write_abs': write_abs})
      if is_halt:
        break
      if not is_jump:
        i += rule['params']+1
    return last_output
  def run_with_config(inp1, phase_settings):
    prev_output = 0
    for p in phase_settings:
      prev_output = compute(inp1, [p, prev_output])
    return prev_output
  return max(run_with_config(inp, configs) for configs in itertools.permutations(range(5), 5))


class Test7(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual(43210, main('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'))

  def test_example_2(self):
    self.assertEqual(54321, main('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'))

  def test_example_3(self):
    self.assertEqual(65210, main('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'))


if __name__ == '__main__':
  with open('7.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
