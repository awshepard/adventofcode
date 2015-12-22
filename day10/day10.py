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


def look_and_say(num):
    to_return = ""
    curr_num = -1
    prev_num = -1
    how_many = 0
    for i in range(0, len(num)):
        curr_num = num[i]
        logging.debug("looking at "+curr_num)
        if curr_num != prev_num and i != 0:
            to_return += str(how_many) + str(prev_num)
            how_many = 1
        else:
            how_many += 1
        prev_num = curr_num
    to_return += str(how_many) + str(prev_num)
    return to_return


def main():
    # open_file = "input"
    # if args.debug_file:
    #     open_file = "debug_%s_%d" % (open_file, args.day)
    # with open(open_file) as f:
    #     for line in f:
    #         print look_and_say(str(line))
    answer = look_and_say("1113122113")
    for i in range(0, 39):
        answer = look_and_say(answer)
    # print answer
    print len(answer)

    answer = look_and_say("1113122113")
    for i in range(0, 49):
        answer = look_and_say(answer)
    # print answer
    print len(answer)

if __name__ == '__main__':
    main()
