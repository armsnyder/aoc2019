# ref: https://adventofcode.com/2019/day/25
import sys
from typing import Callable


def main(inp):
  input_buffer = []
  output_buffer = ''
  def handle_input() -> int:
    nonlocal input_buffer
    if len(input_buffer) == 0:
      next_line = input()
      input_buffer = [ord(c) for c in next_line] + [10,]
    return input_buffer.pop(0)
  def handle_output(value: int):
    nonlocal output_buffer
    if value == 10:
      print(output_buffer, file=sys.stderr)
      output_buffer = ''
    output_buffer += chr(value)
  run_intcode_computer(inp, handle_input, handle_output)


def run_intcode_computer(program: str, handle_input: Callable[[], int], handle_output: Callable[[int], None]):
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
    try:
      rule = [x for x in rules if x['opcode'] == opcode][0]
    except IndexError:
      raise ValueError(f'Illegal opcode {opcode} at index {index}')
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


if __name__ == '__main__':
  with open('25.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
