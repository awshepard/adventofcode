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


def compute_distance(seconds, config):
    cur_seconds = 0
    cur_distance = 0
    is_rest = False
    while (cur_seconds + (config['rest'] if is_rest else config['time'])) < seconds:
        if is_rest:
            cur_seconds += config['rest']
        else:
            cur_seconds += config['time']
            cur_distance += config['speed'] * config['time']
        is_rest = not is_rest

    if not is_rest:
        cur_distance += (seconds - cur_seconds) * config['speed']

    return cur_distance


def new_scoring(seconds):
    for reindeer in reindeer_configs.iterkeys():
        reindeer_configs[reindeer]['score'] = 0
        reindeer_configs[reindeer]['distance'] = 0
        reindeer_configs[reindeer]['resting'] = False
    for i in range(0, seconds):
        # print "%d: " % (i)
        max_dist = -1
        max_reindeer = None
        for reindeer in reindeer_configs.iterkeys():
            # print "\tReindeer %s: dist=%d, score=%d" % (reindeer,
            # reindeer_configs[reindeer]['distance'],
            # reindeer_configs[reindeer]['score'])
            increment = reindeer_configs[reindeer][
                'time'] + reindeer_configs[reindeer]['rest']
            if i % increment >= reindeer_configs[reindeer]['time']:
                reindeer_configs[reindeer]['resting'] = True
            else:
                reindeer_configs[reindeer]['resting'] = False
            if not reindeer_configs[reindeer]['resting']:
                reindeer_configs[reindeer][
                    'distance'] += reindeer_configs[reindeer]['speed']
            if reindeer_configs[reindeer]['distance'] > max_dist:
                max_dist = reindeer_configs[reindeer]['distance']
                max_reindeer = reindeer
        # increment score for current winning reindeer
        reindeer_configs[max_reindeer]['score'] += 1
    print map(lambda(k, v): (k, v['distance'], v['score']), reindeer_configs.iteritems())


reindeer_configs = {}
reindeer_distances = {}


def main():
    open_file = "input"
    if args.debug_file:
        open_file = "debug_%s_%d" % (open_file, args.day)

    with open(open_file) as f:
        for line in f:
            m = re.search(
                '(.*) can fly (\d*) km\/s for (\d*) seconds, but then must rest for (\d*) seconds.', line)
            reindeer = {
                "speed": int(m.group(2)),
                "time": int(m.group(3)),
                "rest": int(m.group(4))
            }
            reindeer_configs[m.group(1)] = reindeer

    print reindeer_configs
    for reindeer, config in reindeer_configs.iteritems():
        reindeer_distances[reindeer] = compute_distance(2503, config)

    print reindeer_distances

    new_scoring(2503)

if __name__ == '__main__':
    main()
