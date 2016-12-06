import sys
import os



visited = {'0.0':1}
x = 0
y = 0
robo_x = 0
robo_y = 0
robo = False
with open("input") as f:
  while True:
    c = f.read(1)
    if not c:
      break
    if not robo:
      if c == '<':
        x -= 1
      elif c == '>':
        x += 1
      elif c == '^':
        y += 1
      elif c == 'v':
        y -= 1
    else:
      if c == '<':
        robo_x -= 1
      elif c == '>':
        robo_x += 1
      elif c == '^':
        robo_y += 1
      elif c == 'v':
        robo_y -= 1
    key = "%d.%d" % (x, y) if not robo else "%d.%d" % (robo_x, robo_y)
    if key not in visited:
      visited[key] = 0
    visited[key] += 1
    robo = not robo


print len(visited)
