# ref: https://adventofcode.com/2019/day/5
import unittest


def main(program, inp):
  rules = [
    {'opcode': 99, 'params': 0, 'fn': lambda args: args['halt']()},
    {'opcode': 1, 'params': 3, 'fn': lambda args: args['write'](3, args['read'](1) + args['read'](2))},
    {'opcode': 2, 'params': 3, 'fn': lambda args: args['write'](3, args['read'](1) * args['read'](2))},
    {'opcode': 3, 'params': 1, 'fn': lambda args: args['write'](1, args['input'])},
    {'opcode': 4, 'params': 1, 'fn': lambda args: args['output'](1)},
    {'opcode': 5, 'params': 2, 'fn': lambda args: args['jump'](args['read'](2)) if args['read'](1) != 0 else None},
    {'opcode': 6, 'params': 2, 'fn': lambda args: args['jump'](args['read'](2)) if args['read'](1) == 0 else None},
    {'opcode': 7, 'params': 3, 'fn': lambda args: args['write_abs'](args['read_immediate'](3), 1) if args['read'](1) < args['read'](2) else args['write_abs'](args['read_immediate'](3), 0)},
    {'opcode': 8, 'params': 3, 'fn': lambda args: args['write_abs'](args['read_immediate'](3), 1) if args['read'](1) == args['read'](2) else args['write_abs'](args['read_immediate'](3), 0)}
  ]
  data = [int(x) for x in program.split(',')]
  i = 0
  last_output = 0
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
    rule['fn']({'halt': halt, 'read': read, 'write': write, 'input': inp, 'output': output, 'jump': jump, 'read_immediate': read_immediate, 'write_abs': write_abs})
    if is_halt:
      break
    if not is_jump:
      i += rule['params']+1
  return last_output


class Test5(unittest.TestCase):
  def __init__(self, x):
    super().__init__(x)
    self.long_program = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'

  def test_example_1(self):
    self.assertEqual(999, main(self.long_program, 7))

  def test_example_2(self):
    self.assertEqual(1000, main(self.long_program, 8))

  def test_example_3(self):
    self.assertEqual(1001, main(self.long_program, 9))

  def test_example_short_1(self):
    self.assertEqual(1, main('3,9,8,9,10,9,4,9,99,-1,8', 8))

  def test_example_short_2(self):
    self.assertEqual(0, main('3,9,7,9,10,9,4,9,99,-1,8', 8))

  def test_example_short_3(self):
    self.assertEqual(1, main('3,3,1108,-1,8,3,4,3,99', 8))

  def test_example_short_4(self):
    self.assertEqual(0, main('3,3,1107,-1,8,3,4,3,99', 8))

  def test_example_jump_1(self):
    self.assertEqual(1, main('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', -1))

  def test_example_jump_2(self):
    self.assertEqual(0, main('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', 0))

  def test_example_jump_3(self):
    self.assertEqual(1, main('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', 1))

  def test_example_jump_4(self):
    self.assertEqual(1, main('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', -1))

  def test_example_jump_5(self):
    self.assertEqual(0, main('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', 0))

  def test_example_jump_6(self):
    self.assertEqual(1, main('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', 1))


if __name__ == '__main__':
  with open('5.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip(), 5))
