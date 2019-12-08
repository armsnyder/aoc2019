#!/usr/bin/env bash
set -e
day=$1
[[ -n "$day" ]] || (echo "day required" && exit 1)
source env.sh  # contains private SESSION_ID credential
echo "Downloading puzzle input..."
curl -s -b "session=$SESSION_ID" -o "$day.txt" "https://adventofcode.com/2019/day/$day/input"
git add "$day.txt"
tpl="# ref: https://adventofcode.com/2019/day/$day
import unittest


def main(inp):
  pass


class Test$day(unittest.TestCase):
  def test_example(self):
    self.assertEqual('', main(''))


if __name__ == '__main__':
  with open('$day.txt', 'r') as f:
    contents = f.read()
  print(main(contents.strip()))"

echo "$tpl" > "${day}a.py"
echo "$tpl" > "${day}b.py"
git add "${day}a.py"
git add "${day}b.py"
echo "Done"
