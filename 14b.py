# ref: https://adventofcode.com/2019/day/14
import unittest
import re
import math

def main(inp: str) -> int:
  recipes = {}
  for line in inp.split('\n'):
    [chemicals_in, chemical_out] = line.split('=>')
    chemicals_in_match = re.findall(r'(\d+) (\w+)', chemicals_in)
    chemical_out_match = re.search(r'(\d+) (\w+)', chemical_out).groups()
    recipes[chemical_out_match[1]] = (int(chemical_out_match[0]), [(int(x[0]), x[1]) for x in chemicals_in_match])
  def calc_ore_required(target_fuel):
    surplus = {}
    queue = [(target_fuel, 'FUEL')]
    total_ore = 0
    while len(queue) > 0:
      (amt_needed, elem) = queue.pop()
      if elem == 'ORE':
        total_ore += amt_needed
        continue
      if elem in surplus and surplus[elem] > 0:
        amt_removed = min(surplus[elem], amt_needed)
        surplus[elem] -= amt_removed
        amt_needed -= amt_removed
      if amt_needed <= 0:
        continue
      (amt_per_unit, elems) = recipes[elem]
      factor = math.ceil(amt_needed / amt_per_unit)
      amt_made = amt_per_unit * factor
      if amt_made > amt_needed:
        if elem not in surplus:
          surplus[elem] = 0
        surplus[elem] += (amt_made - amt_needed)
      queue.extend([(x[0]*factor, x[1]) for x in elems])
    return total_ore
  bs_min = 1
  bs_max = 1000000000000
  while bs_min < bs_max - 1:
    bs_middle = math.floor((bs_min + bs_max) / 2)
    ore_required = calc_ore_required(bs_middle)
    if ore_required < 1000000000000:
      bs_min = bs_middle
    else:
      bs_max = bs_middle
  return bs_min


class Test14(unittest.TestCase):

  def test_example_3(self):
    self.assertEqual(82892753, main('''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'''))

  def test_example_4(self):
    self.assertEqual(5586022, main('''2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF'''))

  def test_example_5(self):
    self.assertEqual(460664, main('''171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX'''))


if __name__ == '__main__':
  with open('14.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))
