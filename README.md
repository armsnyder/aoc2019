# Advent of Code 2019 Solutions \[Complete]

Solutions to the coding puzzles here: https://adventofcode.com/2019

The use of intcode programs as puzzle inputs was very enjoyable and made for some very creative puzzles this year.

## Notable Problems

**Hardest day: Day 22 part 2.**

I had to do a lot of research about modular arithmetic and sum of a geometric series,
and the examples provided in the problem, unlike the real input,
did not work with the final method due to their using a modulus that was not always co-prime
when computing the modular inverse for the geometric series sum.

**Second hardest day: Day 16 part 2.**

For this one there were several "tricks" to notice in the problem,
like the fact that the offset was always near to the end of the input,
and that when near the end of the input the \[0, 1, 0, -1] pattern
essentially goes away and becomes trivial.

**Day that made me feel smart: Day 12 part 2.**

I don't usually find the trick as quickly as I did with this one,
that I could solve each axis independently and find the least-common-multiple
of the three to get the answer.

**Another good day: Day 14 part 2.**

I'm not sure if what I did is optimal, but running the simulation for different target fuels,
and doing a binary search to find the simulation which used the correct amount of ore,
seemed like a non-traditional use of binary search which proved useful.

**Fun day: Day 20 part 2.**

By the time I got to this problem I had implemented BFS a zillion times, so I had some fun with
this one and did a bi-directional BFS, starting from either end of the maze simultaneously.
The "recursive" nature of the maze wasn't too bad since I had already abstracted away the
notion of physical space in part 1.

**Another fun day: Day 21**

This was cool because it was a different kind of puzzle that involved more logic than programming.
It reminded me of playing Shenzhen I/O.

**It was all worth it: Day 25**

Day 25 was incredible. With a minor tweak to my existing intcode computer I was playing a full-blown
text-based adventure game. Initially I thought this would not require any programming and just playing the game
to discover the passcode. However, when I reached the security scanner in the game I had that itch that I could
automate the process of finding the correct combination of items to carry through the scanner.
In the end I had written an AI which played the game for me all the way to the end and outputted the passcode.
It was really enjoyable to write and involved many different strategies: NLP to interpret the game's outputs,
BFS to traverse the ship and collect the items, and DFS to make it back to the security scanner.
When finally at the security scanner I felt I could spend my time more wisely by brute forcing combinations of
items than actually interpreting the game's suggestions that I was "too heavy" or "too light". With the small
number of items in the game it was not an issue finding the combination this way. In the end it was incredibly
satisfying watching my AI play the game. I also programmed an ASCII-rendered map while debugging and left it in.
