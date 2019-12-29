# ref: https://adventofcode.com/2019/day/19
import unittest


def main(inp: str) -> int:
  def bot_function(x, y):
    first_call = True
    output = None
    def handle_input():
      nonlocal first_call
      value = x if first_call else y
      first_call = False
      return value
    def handle_output(value):
      nonlocal output
      output = value
    run_intcode_computer(inp, handle_input, handle_output)
    return output
  return main_with_bot_function(bot_function)


def main_with_bot_function(bot_function) -> int:
  def find_linear(evaluate):
    i = 0
    while not evaluate(i):
      i += 1
    return i
  def find_bisect(evaluate):
    start = -1
    end = 10
    while not evaluate(end):
      start = end
      end *= 2
    while start < end - 1:
      middle = int((start + end) / 2)
      if evaluate(middle):
        end = middle
      else:
        start = middle
    return end
  def test(x, y, expect):
    return bot_function(x, y) == expect
  def find_end_x(y):
    start_x = find_linear(lambda x: test(x, y, 1))
    return start_x + find_bisect(lambda x_offset: test(start_x + x_offset, y, 0))
  width = 100
  y = find_bisect(lambda y: test(find_end_x(y) - width, y + width - 1, 1))
  x = find_end_x(y) - width
  return x * 10000 + y


def run_intcode_computer(program: str, handle_input: callable, handle_output: callable):
  data = [int(x) for x in program.split(',')]
  index = 0
  offset = 0
  memory = {}
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
  is_halt = False
  while not is_halt:
    opcode = data[index] % 100
    modes = list(int(x) for x in reversed(f'{data[index]:06}'))[2:]
    rule = [x for x in rules if x['opcode'] == opcode][0]
    is_jump = False
    def halt():
      nonlocal is_halt
      is_halt = True
    def read(pos):
      mode = modes[pos-1]
      i = data[index+pos] if mode == 0 else index+pos if mode == 1 else data[index+pos]+offset
      if i >= len(data):
        if i not in memory:
          return 0
        return memory[i]
      return data[i]
    def write(pos, value):
      mode = modes[pos-1]
      i = data[index+pos] if mode == 0 else index+pos if mode == 1 else data[index+pos]+offset
      if i >= len(data):
        memory[i] = value
      else:
        data[i] = value
    def output(pos):
      mode = modes[pos-1]
      i = data[index+pos] if mode == 0 else index+pos if mode == 1 else data[index+pos]+offset
      if i > len(data):
        this_output = memory[i]
      else:
        this_output = data[i]
      handle_output(this_output)
    def jump(pos):
      nonlocal is_jump, index
      is_jump = True
      index = pos
    def set_offset(val):
      nonlocal offset
      offset += val
    args1 = {
      'halt': halt,
      'read': read,
      'write': write,
      'input': handle_input,
      'output': output,
      'jump': jump,
      'offset': set_offset,
    }
    rule['fn'](args1)
    if not is_jump:
      index += rule['params']+1
    if is_halt:
      return


class Test19(unittest.TestCase):
  def test_square_at_origin(self):
    self.assertEqual(0, main_with_bot_function(lambda x, y: 1 if x < 100 else 0))

  def test_square_at_origin_plus_one(self):
    self.assertEqual(10001, main_with_bot_function(lambda x, y: 1 if (x == 0 and y == 0) or (1 <= x < 101 and y > 0) else 0))

  def test_cone_1(self):
    def bot_function(x, y):
      return 1 if y <= x < y * 2 else 0
    self.assertEqual(2980199, main_with_bot_function(bot_function))

  def test_cone_2(self):
    def bot_function(x, y):
      return 1 if y - 1 <= x < y * 2 else 0
    self.assertEqual(2960198, main_with_bot_function(bot_function))

  def test_cone_3(self):
    def bot_function(x, y):
      return 1 if y <= x < y * 2 + 1 else 0
    self.assertEqual(2970198, main_with_bot_function(bot_function))

if __name__ == '__main__':
  with open('19.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
