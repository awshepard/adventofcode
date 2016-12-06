import sys
import os

import hashlib




input_str = "iwrupvqb"
match = "000000"
counter = 0
matched = hashlib.md5(input_str + str(counter)).hexdigest()[0:len(match)] == match
while not matched:
  if counter%100000 == 0:
    print "%d..." % counter
  counter += 1
  matched = hashlib.md5(input_str + str(counter)).hexdigest()[0:len(match)] == match

print counter