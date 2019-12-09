# ref: https://adventofcode.com/2019/day/6
import unittest


def main(inp):
  def gen_graph(inp_local):
    graph_local = {}
    for line in inp_local.split('\n'):
      body = line.split(')')[0]
      sat = line.split(')')[1]
      graph_local[sat] = body
    return graph_local
  def get_path(graph_local, node):
    path = []
    cur = node
    while cur != 'COM':
      path.append(cur)
      cur = graph_local[cur]
    return path + ['COM']
  def find_common_parent(graph_local, a, b):
    path_a = reversed(get_path(graph_local, a))
    path_b = reversed(get_path(graph_local, b))
    prev = ''
    while True:
      cur_a = next(path_a)
      cur_b = next(path_b)
      if cur_a != cur_b:
        return prev
      prev = cur_a
  graph = gen_graph(inp)
  common_parent = find_common_parent(graph, 'YOU', 'SAN')
  common_parent_depth = len(get_path(graph, common_parent))
  you_depth = len(get_path(graph, 'YOU'))
  san_depth = len(get_path(graph, 'SAN'))
  return (you_depth - common_parent_depth) + (san_depth - common_parent_depth) - 2


class Test6(unittest.TestCase):
  def test_example(self):
    self.assertEqual(4, main('''
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
'''.strip()))


if __name__ == '__main__':
  with open('6.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
