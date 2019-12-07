# ref: https://adventofcode.com/2019/day/2
import unittest
import copy


def main(inp):
  def inner(noun, verb, codes):
    codes = copy.copy(codes)
    codes[1] = noun
    codes[2] = verb
    i = 0
    while i < len(codes):
      v = codes[i]
      if v == 99:
        break
      elif v == 1:
        codes[codes[i+3]] = codes[codes[i+1]] + codes[codes[i+2]]
      elif v == 2:
        codes[codes[i+3]] = codes[codes[i+1]] * codes[codes[i+2]]
      else:
        raise ValueError(v)
      i += 4
    return codes[0]

  vals = [int(x) for x in inp.strip().split(',')]
  for i in range(100):
    for j in range(100):
      if inner(i, j, vals) == 19690720:
        return 100 * i + j
  raise ValueError


if __name__ == '__main__':
  with open('2.txt', 'r') as f:
    contents = f.read()
  print(main(contents))
