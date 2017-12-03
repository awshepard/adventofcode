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
global directions
directions = ["r", "u", "l", "d"]
global coord_index
coord_index = {}
coord_index["0:0"] = 0
global values
values = [1]

logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)


def get_neighbors(x, y, direction):
    if directions[direction] == "r":
        return (
            {"x": x-1, "y": y},
            {"x": x-1, "y": y+1},
            {"x": x, "y": y+1},
            {"x": x+1, "y": y+1},
        )
    if directions[direction] == "u":
        return (
            {"x": x, "y": y-1},
            {"x": x-1, "y": y-1},
            {"x": x-1, "y": y},
            {"x": x-1, "y": y+1},
        )
    if directions[direction] == "l":
        return (
            {"x": x+1, "y": y},
            {"x": x+1, "y": y-1},
            {"x": x, "y": y-1},
            {"x": x-1, "y": y-1},
        )
    if directions[direction] == "d":
        return (
            {"x": x, "y": y+1},
            {"x": x+1, "y": y-1},
            {"x": x+1, "y": y},
            {"x": x+1, "y": y+1},
        )
    else:
        logging.warn("unknown direction: {}!".format(direction))
        return {}


def part_1(open_file):

    logging.info("part 1")
    input_val = 277678
    total = 0
    x = 1
    y = 0
    direction = 0
    num_moves = 1
    curr_moves = 1
    move_counter = 1
    while total < input_val:
        logging.debug("at position ({}, {})".format(x, y))
        indices = get_neighbors(x,y, direction)
        logging.debug(indices)
        vals = [get_value(item['x'], item['y']) for item in indices]
        logging.debug(vals)
        total = sum(vals)
        logging.debug("total is: ({}) = {}".format(' + '.join([str(val) for val in vals]), total))
        if total > 277678:
            logging.info("answer is: {}".format(total))
        values.append(total)
        coord_index["{}:{}".format(x,y)] = move_counter
        move_counter += 1
        logging.debug("values: {}".format(values))
        logging.debug("coord_index: {}".format(coord_index))
        logging.debug("move_counter: {}".format(move_counter))
        # now move like a turtle
        logging.debug("Begin move phase: curr_moves = {}, num_moves = {}, direction = {}, (x, y) = ({}, {})".format(
            curr_moves,
            num_moves,
            directions[direction],
            x,
            y))
        if curr_moves == num_moves:
            # change direction
            # reset curr_moves
            logging.debug("curr_moves = num_moves, changing direction from {} to {}".format(directions[direction], directions[(direction + 1) % 4]))
            direction = (direction + 1) % 4
            curr_moves = 0
            logging.debug("curr_moves = {}".format(curr_moves))
            if direction % 2 == 0: # even directions increment our num moves
                logging.debug("new direction is even, incrementing num_moves")
                num_moves += 1
        # execute move
        if (directions[direction] == "r"):
            x += 1
            curr_moves += 1
        elif (directions[direction] == "u"):
            y += 1
            curr_moves += 1
        elif (directions[direction] == "l"):
            x -= 1
            curr_moves += 1
        elif (directions[direction] == "d"):
            y -= 1
            curr_moves += 1
        else:
            logging.warn("unknown direction: {}!".format(direction))
        logging.debug("End move phase: curr_moves = {}, num_moves = {}, direction = {}, (x, y) = ({}, {})".format(
            curr_moves,
            num_moves,
            directions[direction],
            x,
            y))
        if args.interactive:
            raw_input("hit enter to continue")
    logging.info("answer is: {}".format(total))


def get_value(x, y):
    if "{}:{}".format(x,y) not in coord_index:
        return 0
    logging.debug("found ({},{}) with index: {}".format(x, y, coord_index["{}:{}".format(x,y)]))
    return values[coord_index["{}:{}".format(x,y)]]


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
