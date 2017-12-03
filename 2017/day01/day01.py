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
parser.add_argument('--expected', type=int, default=-1, help='expected output')
global args
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)


def main():
    open_file = "input"
    if args.debug_file:
        open_file = "debug_%s_%d" % (open_file, args.day)

    with open(open_file) as f:
        data=f.read().strip()
        print data
        # loop chars
        data_len = len(data)
        last_char = ""
        total = 0
        # second challenge
        for i in range(0, len(data)):
        	if data[i] == data[(i + (data_len/2)) % data_len]:
        		total += int(data[i%data_len])
      #  first challenge
      #   for i in range(0, len(data)+1):
      #   	if data[i%data_len] == last_char:
      #   		total += int(data[i%data_len])
    		# last_char = data[i%data_len]

    print total

if __name__ == '__main__':
    main()
