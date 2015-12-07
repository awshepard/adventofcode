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

lights = [[False for _ in xrange(1000)]
          for _ in xrange(1000)
          ]


def change_lights(instruction, first_coords, second_coords):
    big_x, small_x, big_y, small_y = -1, -1, -1, -1
    if first_coords[1] >= second_coords[1]:
        big_y = int(first_coords[1])
        small_y = int(second_coords[1])
    else:
        big_y = int(second_coords[1])
        small_y = int(first_coords[1])
    if first_coords[0] >= second_coords[0]:
        big_x = int(first_coords[0])
        small_x = int(second_coords[0])
    else:
        big_x = int(second_coords[0])
        small_x = int(first_coords[0])

    should_read = ((big_y - small_y + 1) * (big_x - small_x + 1))
    logging.debug("rows %s to %s, cols %s to %s, total %s" % (
        small_y, big_y, small_x, big_x, should_read))

    count_read = 0

    if instruction == 'turn on':
        logging.debug("running turn on")
        for row in range(small_y, big_y + 1):
            for col in range(small_x, big_x + 1):
                lights[row][col] = True
                count_read += 1
    if instruction == 'turn off':
        logging.debug("running turnoff")
        for row in range(small_y, big_y + 1):
            for col in range(small_x, big_x + 1):
                lights[row][col] = False
                count_read += 1
    if instruction == 'toggle':
        logging.debug("running toggle")
        for row in range(small_y, big_y + 1):
            for col in range(small_x, big_x + 1):
                lights[row][col] = False if lights[row][col] else True
                count_read += 1

    if count_read != should_read:
        logging.debug("Count read %d didn't equal should read %d!" %
                      (count_read, should_read))


def count_lights():
    total = 0
    for i in lights:
        total += i.count(True)
    return total


def main():
    open_file = "input"
    if args.debug_file:
        open_file = "debug_%s_%d" % (open_file, args.day)

    with open(open_file) as f:
        for line in f:
            line = line.strip()
            m = re.search("\d", line)
            instruction = line[0:m.start()].strip()
            coordinate_list = line[m.start():].split(" through ")
            first_coords = coordinate_list[0].strip().split(",")
            first_coords = [int(i) for i in first_coords]
            second_coords = coordinate_list[1].strip().split(",")
            second_coords = [int(i) for i in second_coords]
            # logging.debug(instruction)
            # logging.debug(coordinate_list)
            # logging.debug(first_coords)
            # logging.debug(second_coords)
            change_lights(instruction, first_coords, second_coords)

    lights = count_lights()
    print lights
    if args.debug_file:
        logging.debug("Expected: %s, got: %s, %s" % (
            args.expected, lights, "PASSED" if args.expected == lights else "FAILED"))

if __name__ == '__main__':
    main()
