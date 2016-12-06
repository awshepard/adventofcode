import sys
import os



floor = 0
with open("input") as f:
	while True:
		c = f.read(1)
		if not c:
			break
		if c == "(":
			floor += 1
		if c == ")":
			floor -= 1

print floor
