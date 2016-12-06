import sys
import os
import itertools


total_paper = 0
total_ribbon = 0
with open("input") as f:
  for line in f:
    dims = line.strip().split("x")
    if len(dims) == 3:
      volume = int(dims[0]) * int(dims[1]) * int(dims[2])
      combo_it = itertools.combinations(dims,2)
      side_areas = []
      side_perimeters = []
      for combo in combo_it:
        side_areas.append(int(combo[0])*int(combo[1]))
        side_perimeters.append(2 * (int(combo[0])+int(combo[1])))
      s = sorted(side_areas)
      p = sorted(side_perimeters)[0]
      total_paper += 3 * s[0] + 2 * s[1] + 2 * s[2]
      total_ribbon += p + volume

print total_paper

print total_ribbon
