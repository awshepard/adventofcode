import sys
import os
import re
import itertools
import argparse
import logging
import operator


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

distance_matrix = {}


def get_distance(path):
    total_distance = 0
    for i in range(0, len(path)-1):
        total_distance += distance_matrix[path[i]][path[i+1]]
    return total_distance


def main():
    open_file = "input"
    if args.debug_file:
        open_file = "debug_%s_%d" % (open_file, args.day)

    with open(open_file) as f:
        for line in f:
            lhs, distance = line.split(" = ")
            locations = lhs.split(" to ")
            distance = int(distance.strip())
            if locations[0] not in distance_matrix:
                distance_matrix[locations[0]] = {}
            if locations[1] not in distance_matrix:
                distance_matrix[locations[1]] = {}
            distance_matrix[locations[0]][locations[1]] = distance
            distance_matrix[locations[1]][locations[0]] = distance

    print distance_matrix
    list_of_paths = itertools.permutations(distance_matrix.keys())

    path_distances = {}
    counter = 0
    for path in list_of_paths:
        if counter % 1000 == 0:
            print counter
        path_key = ' -> '.join(path)
        path_distances[path_key] = get_distance(path)
        counter += 1

    sorted_distances = sorted(
        path_distances.items(), key=operator.itemgetter(1))
    print sorted_distances[len(sorted_distances)-1]

if __name__ == '__main__':
    main()
