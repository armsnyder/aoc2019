#!/usr/bin/env bash
set -e
id=$1
[[ -n "$id" ]] || (echo "puzzle id required" && exit 1)
day="${id::-1}"
level="${id: -1}"
case $level in
a)
  level=1
  ;;
b)
  level=2
  ;;
*)
  echo "invalid level $level"
  exit 1
  ;;
esac
./test.sh "$id"  # ensure tests pass before submitting
source env.sh  # contains private SESSION_ID credential
answer=$(python3 "$id.py")
echo "Answer: $answer"
echo "Submitting answer..."
resp=$(curl -s -b "session=$SESSION_ID" -d "level=$level&answer=$answer" "https://adventofcode.com/2019/day/$day/answer")
echo "$resp" | sed -n 's:.*<article>\(.*\)</article>.*:\1:p'
