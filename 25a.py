# ref: https://adventofcode.com/2019/day/25
import sys
import re
import time
from typing import Callable, Generator, Tuple, List, Dict, Any, Set

Coord = Tuple[int, int]


def main(inp):
  input_buffer: List[int] = []
  output_buffer = ''
  current_location = (0, 0)
  path_history: List[Coord] = []
  visited: Set[Coord] = {(0, 0)}
  bad_items = {'escape pod', 'infinite loop', 'molten lava'}
  direction_to_door = {(0, -1): 'north', (0, 1): 'south', (1, 0): 'east', (-1, 0): 'west'}
  door_to_direction = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}
  map_data: Dict[Coord, Dict[str, Any]] = {(0, 0): {'items': [], 'doors': []}}

  def add_coords(a: Coord, b: Coord) -> Coord:
    return a[0] + b[0], a[1] + b[1]

  def multiply_coord(a: Coord, m: int) -> Coord:
    return a[0] * m, a[1] * m

  def subtract_coords(a: Coord, b: Coord) -> Coord:
    return a[0] - b[0], a[1] - b[1]

  def update_map_data():
    room_name_match = re.search(r'== (.+) ==', output_buffer)
    if room_name_match is not None:
      map_data[current_location]['name'] = room_name_match.group(1)
    if 'Doors here lead:' in output_buffer:
      map_data[current_location]['doors'] = [x for x in ('north', 'south', 'east', 'west') if '- ' + x in output_buffer]
      for door in map_data[current_location]['doors']:
        next_room_location = add_coords(current_location, door_to_direction[door])
        if next_room_location not in map_data:
          map_data[next_room_location] = {'items': [], 'doors': []}
    if 'Items here:' in output_buffer:
      items_search_text = output_buffer[output_buffer.index('Items here:'):output_buffer.index('Command?')]
      map_data[current_location]['items'] = [item for item in re.findall(r'- (.+)', items_search_text)
                                             if item not in bad_items]

  def choose_next_input() -> str:
    nonlocal current_location, visited
    if len(map_data[current_location]['items']) > 0:
      item = map_data[current_location]['items'].pop()
      return f'take {item}'
    if len(path_history) == 0 and all(room in visited for room in map_data):
      visited = {(0, 0)}
    for door in map_data[current_location]['doors']:
      next_room_location = add_coords(current_location, door_to_direction[door])
      if next_room_location not in visited:
        path_history.append(current_location)
        current_location = next_room_location
        visited.add(next_room_location)
        return door
    next_room_location = path_history.pop()
    door = direction_to_door[subtract_coords(next_room_location, current_location)]
    current_location = next_room_location
    return door

  def render_map():
    min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')
    for coord in map_data.keys():
      min_x, min_y, max_x, max_y = min(min_x, coord[0]), min(min_y, coord[1]), max(max_x, coord[0]), max(max_y,
                                                                                                         coord[1])
    map_render = [[' '] * ((max_x - min_x + 1) * 10 - 1) for _ in range(((max_y - min_y + 1) * 2 - 1))]
    for y in range(min_y, max_y + 1):
      for x in range(min_x, max_x + 1):
        coord = (x, y)
        if coord not in map_data:
          continue
        center_in_render = ((x - min_x) * 10 + 4, (y - min_y) * 2)
        if 'name' not in map_data[coord]:
          map_render[center_in_render[1]][center_in_render[0]] = '?'
          continue
        map_render[center_in_render[1]][center_in_render[0] - 3:center_in_render[0] + 3] = map_data[coord]['name'][:7]
        if coord == current_location:
          map_render[center_in_render[1]][center_in_render[0] - 4] = '['
          map_render[center_in_render[1]][center_in_render[0] + 4] = ']'
        for door in map_data[coord]['doors']:
          if door in ('north', 'south'):
            render_loc = add_coords(door_to_direction[door], center_in_render)
            map_render[render_loc[1]][render_loc[0]] = '|'
          else:
            render_loc = add_coords(multiply_coord(door_to_direction[door], 5), center_in_render)
            map_render[render_loc[1]][render_loc[0]] = '-'
    print('\n'.join(''.join(row) for row in map_render), file=sys.stderr)

  def handle_input() -> int:
    nonlocal input_buffer, output_buffer
    if len(input_buffer) == 0:
      update_map_data()
      render_map()
      next_input = choose_next_input()
      print(output_buffer, file=sys.stderr)
      print(next_input, file=sys.stderr)
      time.sleep(0.5)
      input_buffer = [ord(c) for c in next_input] + [10, ]
      output_buffer = ''
    return input_buffer.pop(0)

  def handle_output(value: int):
    nonlocal output_buffer
    output_buffer += chr(value)

  for _ in run_controlled_execution_intcode_computer(inp, handle_input, handle_output):
    pass


def run_controlled_execution_intcode_computer(program: str, handle_input: Callable[[], int],
                                              handle_output: Callable[[int], None]) -> Generator[None, None, None]:
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
    {'opcode': 7, 'params': 3,
     'fn': lambda args: args['write'](3, 1) if args['read'](1) < args['read'](2) else args['write'](3, 0)},
    {'opcode': 8, 'params': 3,
     'fn': lambda args: args['write'](3, 1) if args['read'](1) == args['read'](2) else args['write'](3, 0)},
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
      mode = modes[pos - 1]
      i = data[index + pos] if mode == 0 else index + pos if mode == 1 else data[index + pos] + offset
      if i >= len(data):
        if i not in memory:
          return 0
        return memory[i]
      return data[i]

    def write(pos, value):
      mode = modes[pos - 1]
      i = data[index + pos] if mode == 0 else index + pos if mode == 1 else data[index + pos] + offset
      if i >= len(data):
        memory[i] = value
      else:
        data[i] = value

    def output(pos):
      mode = modes[pos - 1]
      i = data[index + pos] if mode == 0 else index + pos if mode == 1 else data[index + pos] + offset
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
      index += rule['params'] + 1
    if is_halt:
      return
    yield


if __name__ == '__main__':
  with open('25.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
