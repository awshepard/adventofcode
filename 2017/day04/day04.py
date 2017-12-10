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
parser.add_argument('--interactive', action='store_true', default=False, help='run in interactive (pause) mode')
parser.add_argument('--expected', type=int, default=-1, help='expected output')
global args
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)


def part_1(open_file):
    logging.info("part 1")
    total_valid = 0
    with open(open_file) as f:
        for line in f:
            line_list = sorted(line.strip().split(' '))
            logging.debug("line_list = {}".format(line_list))
            line_set_list = sorted(list(set(line_list)))
            logging.debug("line_set_list = {}".format(line_list))
            if line_list == line_set_list:
                logging.debug("lists are equal!")
                total_valid += 1
            else:
                logging.debug('lists are not equal!')
            if args.interactive:
                raw_input("hit enter to continue")
    logging.info("total_valid = {}".format(total_valid))


def part_2(open_file):
    logging.info("part 2")
    with open(open_file) as f:
        invalid = {}
        total = 0
        for line in f:
            total += 1
            line_list = line.strip().split(' ')
            logging.debug("processing line: {}".format(line))
            letter_map = {}
            for word in line_list:
                key = ':'.join(["{}{}".format(item[0],item[1]) for item in sorted(dict((letter,word.count(letter)) for letter in set(word)).items())])
                logging.debug("word = {}, key map = {}".format(word, key))
                if key not in letter_map:
                    letter_map[key] = 1
                else:
                    logging.debug("Found duplicate: word = {}".format(word))
                    invalid[line] = 1
                    continue
            if args.interactive:
                raw_input("hit enter to continue")
    logging.info("total invalid = {}".format(len(invalid)))
    logging.info("total valid = {}".format(total - len(invalid)))



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
