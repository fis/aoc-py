#! /usr/bin/python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import intcode
import sys

def robot(prog, white=set()):
    painted = set()
    rpos, rdir = [0, 0], [0, -1]
    cycle = ['paint']  # or 'turn'

    def robot_in():
        return 1 if tuple(rpos) in white else 0

    def robot_out(n):
        if cycle[0] == 'paint':
            cycle[0] = 'turn'
            p = tuple(rpos)
            painted.add(p)
            if n == 0:   white.discard(p)
            elif n == 1: white.add(p)
            else: raise RuntimeError(f'bad paint: {n}')
        else:
            cycle[0] = 'paint'
            dx, dy = rdir[0], rdir[1]
            if n == 0:   dx, dy = dy, -dx
            elif n == 1: dx, dy = -dy, dx
            else: raise RuntimeError(f'bad turn: {n}')
            rpos[0] += dx
            rpos[1] += dy
            rdir[0] = dx
            rdir[1] = dy

    intcode.run(prog, stdin=robot_in, stdout=robot_out)

    return white, painted

# part 1

prog = intcode.load('day11-input.txt' if len(sys.argv) < 2 else sys.argv[1])

white, painted = robot(prog)
print(len(painted))

# part 2

white, painted = robot(prog, set([(0,0)]))

min_x, max_x = min(w[0] for w in white), max(w[0] for w in white)
min_y, max_y = min(w[1] for w in white), max(w[1] for w in white)
for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
        c = '#' if (x,y) in white else ' '
        print(c, end='')
    print('')
