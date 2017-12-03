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
	with open(open_file) as f:
		for line in f:
			pass


def part_2(open_file):
	logging.info("part 2")
	with open(open_file) as f:
		for line in f:
			pass

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
