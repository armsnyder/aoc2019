# ref: https://adventofcode.com/2019/day/25
import sys
import re
import itertools
from typing import Callable, List, Dict, Tuple, Optional, Set

MODE_GATHER_ITEMS = 1
MODE_RETURN_TO_SECURITY = 2
MODE_FIND_CORRECT_ITEM_COMBINATION = 3


class Room:
  def __init__(self, name: str):
    self.name = name
    self.doors: Dict[str, Optional[Room]] = {}
    self.items = []


def main(inp: str, verbose: bool):
  # I/O buffers for the intcode program
  input_buffer: List[int] = []
  output_buffer = ''

  # High-level switch which controls how the robot is behaving currently:
  mode = MODE_GATHER_ITEMS

  # Variables which generally keep track of state for making decisions:
  current_room: Optional[Room] = None
  current_inventory: Set[str] = set()

  # Variables to track state while the robot is gathering items:
  path_history: List[Room] = []
  last_move: Optional[Tuple[Room, str]] = None

  # Cosmetic variable which controls whether the map is rendered after a move:
  last_action_was_move = True

  # Path used when navigating back to the security checkpoint:
  enqueued_path: List[str] = []

  # Variables used as memory for finding the correct combination of items:
  all_items: Set[str] = set()
  simultaneous_items = 0
  item_group_queue: List[Tuple[str, ...]] = []
  desired_item_group: Optional[Set[str]] = None

  def update_map_data():
    nonlocal current_room, last_move
    buffer_to_read = output_buffer
    if current_room is None:
      room_name_match = re.search(r'== (.+) ==', buffer_to_read)
      current_room_name = room_name_match.group(1)
      current_room = Room(current_room_name)
      if last_move is not None:
        last_move[0].doors[last_move[1]] = current_room
        current_room.doors[{'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}[last_move[1]]] = \
          last_move[0]
        last_move = None
    if 'you are ejected back to the checkpoint' in buffer_to_read:
      buffer_to_read = buffer_to_read[buffer_to_read.index('== Security Checkpoint =='):]
    if 'Doors here lead:' in buffer_to_read:
      for door in [x for x in ('north', 'south', 'east', 'west') if '- ' + x in buffer_to_read]:
        if door not in current_room.doors:
          current_room.doors[door] = None
    if 'Items here:' in buffer_to_read:
      items_search_text = buffer_to_read[buffer_to_read.index('Items here:'):buffer_to_read.index('Command?')]
      current_room.items = [item for item in re.findall(r'- (.+)', items_search_text)
                            if item not in {'escape pod', 'infinite loop', 'molten lava', 'giant electromagnet',
                                            'photons'}]

  def choose_next_input() -> str:
    nonlocal last_move, current_room, last_action_was_move, mode, enqueued_path, simultaneous_items, item_group_queue, all_items, desired_item_group

    if mode == MODE_GATHER_ITEMS:
      if current_room.name != 'Security Checkpoint':
        if len(current_room.items) > 0:
          item = current_room.items.pop()
          current_inventory.add(item)
          last_action_was_move = False
          return f'take {item}'
        for door, room in current_room.doors.items():
          if room is None:
            path_history.append(current_room)
            last_move = (current_room, door)
            current_room = None
            last_action_was_move = True
            return door
      if len(path_history) > 0:
        next_room = path_history.pop()
        door = [door for door, room in current_room.doors.items() if room == next_room][0]
        last_move = (current_room, door)
        current_room = next_room
        last_action_was_move = True
        return door
      all_items = current_inventory.copy()
      mode = MODE_RETURN_TO_SECURITY

    if mode == MODE_RETURN_TO_SECURITY:
      if current_room.name != 'Security Checkpoint':
        if len(enqueued_path) == 0:
          enqueued_path = find_path_to_security_checkpoint()
        door = enqueued_path.pop(0)
        current_room = current_room.doors[door]
        last_action_was_move = True
        return door
      mode = MODE_FIND_CORRECT_ITEM_COMBINATION

    if mode == MODE_FIND_CORRECT_ITEM_COMBINATION:
      if len(item_group_queue) == 0:
        simultaneous_items += 1
        item_group_queue = list(itertools.combinations(all_items, simultaneous_items))
      if desired_item_group is None:
        desired_item_group = set(item_group_queue.pop())
      if desired_item_group != current_inventory:
        items_to_drop = current_inventory - desired_item_group
        if len(items_to_drop) > 0:
          item_to_drop = items_to_drop.pop()
          current_inventory.remove(item_to_drop)
          last_action_was_move = False
          return f'drop {item_to_drop}'
        items_to_take = desired_item_group - current_inventory
        item_to_take = items_to_take.pop()
        current_inventory.add(item_to_take)
        last_action_was_move = False
        return f'take {item_to_take}'
      desired_item_group = None
      last_action_was_move = False  # Cosmetic decision since the robot is almost always booted back
      return [door for door, room in current_room.doors.items()
              if room is None or room.name == 'Pressure-Sensitive Floor'][0]

  def find_path_to_security_checkpoint() -> List[str]:
    queue: List[Tuple[Room, List[str]]] = [(current_room, [])]
    visited: Set[Room] = set()
    while len(queue) > 0:
      room, path = queue.pop(0)
      if room in visited:
        continue
      if room.name == 'Security Checkpoint':
        return path
      if any(door is None for door in room.doors.values()):
        raise Exception('Incomplete map')
      queue.extend([(next_room, path + [door, ]) for door, next_room in room.doors.items()])
    raise Exception('Not found')

  def render_map():
    def has_door(door: str):
      return door in current_room.doors

    def get_door_name(door: str):
      return '' if not has_door(door) else '?' if current_room.doors[door] is None else current_room.doors[door].name

    horiz_cells = sum((True, has_door('east'), has_door('west')))
    vert_cells = sum((1, 2 if has_door('north') else 0, 2 if has_door('south') else 0))
    cells = [['' for _ in range(horiz_cells)] for _ in range(vert_cells)]
    current_room_cell = (2 if has_door('north') else 0, 1 if has_door('west') else 0)
    cells[current_room_cell[0]][current_room_cell[1]] = f'[{current_room.name}]'
    if has_door('north'):
      cells[current_room_cell[0] - 1][current_room_cell[1]] = '|'
      cells[current_room_cell[0] - 2][current_room_cell[1]] = get_door_name('north')
    if has_door('south'):
      cells[current_room_cell[0] + 1][current_room_cell[1]] = '|'
      cells[current_room_cell[0] + 2][current_room_cell[1]] = get_door_name('south')
    if has_door('east'):
      cells[current_room_cell[0]][current_room_cell[1] + 1] = f" - {get_door_name('east')}"
    if has_door('west'):
      cells[current_room_cell[0]][current_room_cell[1] - 1] = f"{get_door_name('west')} - "
    cell_widths = [max(len(cells[i][j]) for i in range(vert_cells)) for j in range(horiz_cells)]
    lines = [''.join(cells[i][j].center(cell_widths[j]) for j in range(horiz_cells)) for i in range(vert_cells)]
    print('\n'.join(lines), file=sys.stderr)

  def handle_input() -> int:
    nonlocal input_buffer, output_buffer
    if len(input_buffer) == 0:
      update_map_data()
      if last_action_was_move and verbose:
        print('', file=sys.stderr)
        render_map()
      next_input = choose_next_input()
      if verbose:
        print(output_buffer, file=sys.stderr)
        print(next_input, file=sys.stderr)
      input_buffer = [ord(c) for c in next_input] + [10, ]
      output_buffer = ''
    return input_buffer.pop(0)

  def handle_output(value: int):
    nonlocal output_buffer
    output_buffer += chr(value)

  run_intcode_computer(inp, handle_input, handle_output)

  if verbose:
    print(output_buffer, file=sys.stderr)

  return re.search(r'\d+', output_buffer).group()


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


if __name__ == '__main__':
  with open('25.txt', 'r') as f:
    contents = f.read()
  verbose_flag = '-verbose' in sys.argv
  print(main(contents.strip(), verbose_flag))
