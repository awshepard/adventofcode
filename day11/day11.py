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


def is_valid_1(password):
    # rule 2 shortcut
    if any(substring in password for substring in ["i", "o", "l"]):
        return False

    passes_rule_1 = False
    passes_rule_3 = False
    last_bigram = None
    last_bigram_pos = -1
    for i in range(0, len(password)):
        logging.debug("iter letter: "+password[i])
        if passes_rule_1 and passes_rule_3:
            return True
        if not passes_rule_1 and i < len(password)-3:
            # check rule 1
            logging.debug("checking rule 1 %s" % password[i:i+3])
            if ord(password[i]) == ord(password[i+1])-1 and ord(password[i+1]) == ord(password[i+2])-1:
                passes_rule_1 = True
        if not passes_rule_3 and i < len(password)-1:
            logging.debug("checking rule 3 %s" % password[i:i+2])
            if password[i] == password[i+1]:
                if i < len(password)-2 and password[i+1] == password[i+2]:
                    continue
                if last_bigram is not None:
                    passes_rule_3 = True
                else:
                    logging.debug("setting bigram!")
                    last_bigram = password[i] + password[i+1]

    if passes_rule_1 and passes_rule_3:
        return True
    return False


def increment_password(password):
    values = [ord(x)-97 for x in password]
    # print values
    carry = False
    firstPass = True
    i = len(values)-1
    while (firstPass or carry) and i >= 0:
        firstPass = False
        values[i] = (values[i] + 1)
        # if carry:
        #     values[i] += 1
        if values[i] >= 26:
            # print "hit carry!"
            values[i] = values[i] % 26
            carry = True
        else:
            carry = False
        i -= 1
    # print values
    return ''.join([chr(x+97) for x in values])


def main():
    open_file = "input"
    if args.debug_file:
        open_file = "debug_%s_%d" % (open_file, args.day)

    with open(open_file) as f:
        for line in f:
            print is_valid_1(line)

    # password = "abcdefgh"
    # #password = increment_password(password)
    # while not is_valid_1(password):
    #     password = increment_password(password)
    # # print password

    # print password

    # password = "ghijklmn"
    # while not is_valid_1(password):
    #     password = increment_password(password)

    # print password

    password = "hepxcrrq"
    while not is_valid_1(password):
        password = increment_password(password)

    print password

    password = "hepxxzaa"
    while not is_valid_1(password):
        password = increment_password(password)

    print password


if __name__ == '__main__':
    main()
