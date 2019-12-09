# ref: https://adventofcode.com/2019/day/6
import unittest


def main(inp):
  def gen_graph(inp_local):
    graph = {}
    for line in inp_local.split('\n'):
      body = line.split(')')[0]
      sat = line.split(')')[1]
      if body not in graph:
        graph[body] = []
      graph[body] += [sat]
    return graph
  def count_orbits(graph):
    stack = [('COM', 0)]
    total = 0
    while len(stack) > 0:
      cur = stack.pop()
      total += cur[1]
      if cur[0] in graph:
        for child in graph[cur[0]]:
          stack.append((child, cur[1]+1))
    return total
  return count_orbits(gen_graph(inp))


class Test6(unittest.TestCase):
  def test_example(self):
    self.assertEqual(42, main('''
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
'''.strip()))


if __name__ == '__main__':
  with open('6.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
