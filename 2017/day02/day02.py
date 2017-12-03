import sys
import os
import re
import itertools
import argparse
import logging


parser = argparse.ArgumentParser()
parser.add_argument(
    '--debug', action='store_true', default=False, help='debug mode')
parser.add_argument(
    '--debug-file', action='store_true', default=False, help='debug file')
parser.add_argument('--day', type=int, default=1, help='which day')
parser.add_argument('--part', type=int, default=1, help='which part')
parser.add_argument('--expected', type=int, default=-1, help='expected output')
global args
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)


def part_1(open_file):
	logging.info("part 1")
	total = 0
	with open(open_file) as f:
		for line in f:
			# tokenize
			line_arr = line.split("\t")
			smallest = int(line_arr[0])
			largest = int(line_arr[0])
			for i in line_arr:
				if int(i) < smallest:
					smallest = int(i)
				if int(i) > largest:
					largest = int(i)
			diff = largest - smallest
			total += diff
			logging.debug("line: {}, smallest: {}, largest: {}, diff: {}, total: {}".format(line, smallest, largest, diff, total))
	logging.info("answer is: {}".format(total))


def part_2(open_file):
	logging.info("part 2")
	total = 0
	with open(open_file) as f:
		for line in f:
			line_arr = [int(i) for i in line.split("\t")]
			len_arr = len(line_arr)
			for i in range(0, len_arr - 1):
				for j in range(i+1, len_arr):
					# check if i divides j
					if line_arr[i] % line_arr[j] == 0:
						result = line_arr[i] / line_arr[j]
						total += result
						continue
					# check if j divides i
					if line_arr[j] % line_arr[i] == 0:
						result = line_arr[j] / line_arr[i]
						total += result
						continue
	logging.info("answer is: {}".format(total))

def main():
    open_file = "input"
    if args.debug_file:
        open_file = "debug_%s_%d" % (open_file, args.day)
    if args.part == 1:
    	part_1(open_file)
    elif args.part == 2:
    	part_2(open_file)
    else:
    	logging.warn("unknown part: {}".format(args.part))
    

if __name__ == '__main__':
    main()
