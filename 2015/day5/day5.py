import sys
import os
import itertools
import argparse
import logging



parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true', default = False, help='debug mode')
parser.add_argument('--day', type=int, default = 1, help='which day')
parser.add_argument('--expected', type=int, default = -1, help='expected output')
global args
args = parser.parse_args()

logging.basicConfig(level = logging.DEBUG if args.debug else logging.INFO)

global naughty_filter
naughty_filter = ["ab", "cd", "pq", "xy"]
global vowel_list
vowel_list = ["a","e","i","o","u"]

def is_nice_2(word):
  logging.debug("\nChecking word %s" % word)
  digram_map = {}
  digram_list = []
  trigram_list = []
  passed_triple = False
  passed_double = False
  for i in range(0, len(word)-1):
    digram = word[i:i+2]
    if digram not in digram_map and len(digram)>1:
      logging.debug("adding %s to digram_map" % digram)
      digram_map[digram] = 0
    if len(digram)>1:
      if digram != word[i+1:i+3]:
        logging.debug("incrementing %s because %s is next" % (digram, word[i+1:i+3]))
        digram_map[digram] += 1
      else:
        logging.debug("Not incrementing %s because %s is next" % (digram, word[i:i+3]))
      if digram_map[digram] >= 2:
        digram_list.append(digram)
        logging.debug("got two %s, %s" % (digram, digram_map))
        passed_double = True
    trigram = word[i:i+3]
    if (i < (len(word) - 2)) and word[i] == word[i+2] and word[i] != word[i+1]:
      logging.debug("Found non-overlapping palindrome: %s" % trigram)
      trigram_list.append(trigram)
      passed_triple = True
    if passed_double and passed_triple:
      logging.info("Word %s -> passed_double = %s (%s), passed_triple = %s (%s)" % (word, passed_double, ','.join(set(digram_list)), passed_triple, ','.join(trigram_list)))
      return True
  return False

def is_nice(word):
  logging.debug("Checking word %s" % word)
  for seq in naughty_filter:
    if seq in word:
      logging.debug( "found %s in %s at pos %d" % (seq, word, word.find(seq)))
      return False

  # now test nice
  last_letter = ''
  nice_double = False
  vowel_count = 0
  nice_triggered = False
  for i in range(0,len(word)):
    letter = word[i]
    if letter == last_letter:
      logging.debug( "last letter %s == this letter %s" % (last_letter, letter))
      nice_double = True
    if letter in vowel_list:
      vowel_count += 1
      logging.debug( "got vowel %s, count = %d" % (letter, vowel_count))
    if vowel_count >= 3 and nice_double == True:
      return True
    last_letter = letter


def main():
  naughty = 0
  nice = 0
  open_file = "input"
  if args.debug:
    open_file = "debug_%s_%d" % ( open_file , args.day)
  with open(open_file) as f:
    for line in f:
      word = line.strip()
      if args.day == 1:
        was_nice = is_nice(word)
      else:
        was_nice = is_nice_2(word)
      if was_nice:
        nice += 1
      else:
        naughty += 1
      
      if args.debug:
          logging.debug( "Word %s was: %s" % (word, "nice" if was_nice else "naughty"))

  print nice
  if args.debug:
    logging.debug("Expected: %s, got: %s, %s" % (args.expected, nice, "PASSED" if args.expected == nice else "FAILED"))


if __name__ == '__main__':
  main()