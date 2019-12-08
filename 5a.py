# ref: https://adventofcode.com/2019/day/5
import unittest


def main(inp):
  rules = [
    {'opcode': 99, 'params': 0, 'fn': lambda args: args['halt']()},
    {'opcode': 1, 'params': 3, 'fn': lambda args: args['write'](3, args['read'](1) + args['read'](2))},
    {'opcode': 2, 'params': 3, 'fn': lambda args: args['write'](3, args['read'](1) * args['read'](2))},
    {'opcode': 3, 'params': 1, 'fn': lambda args: args['write'](1, args['input'])},
    {'opcode': 4, 'params': 1, 'fn': lambda args: args['output'](1)}
  ]
  data = [int(x) for x in inp.split(',')]
  i = 0
  last_output = 0
  while True:
    opcode = data[i] % 100
    modes = list(int(x) for x in reversed(f'{data[i]:06}'))[2:]
    rule = [x for x in rules if x['opcode'] == opcode][0]
    is_halt = False
    def halt():
      nonlocal is_halt
      is_halt = True
    def read(pos):
      if modes[pos-1] == 0:
        return data[data[i+pos]]
      else:
        return data[i+pos]
    def write(pos, value):
      nonlocal data
      data[data[i+pos]] = value
    def output(pos):
      nonlocal last_output
      last_output = data[data[i+pos]]
    rule['fn']({'halt': halt, 'read': read, 'write': write, 'input': 1, 'output': output})
    if is_halt:
      break
    i += rule['params']+1
  return last_output


class Test5(unittest.TestCase):
  def test_example_1(self):
    self.assertEqual(1, main('3,0,4,0,99'))

  def test_example_2(self):
    self.assertEqual(12, main('1002,4,3,1,4,1,99'))


if __name__ == '__main__':
  with open('5.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
