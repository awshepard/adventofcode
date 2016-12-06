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

instructions = {}
instruction_list = [
    'RSHIFT', 'LSHIFT', 'OR', 'AND', 'NOT'
]


class TreeNode(object):

    def __init__(self, name, operator=None, operands=None):
        self.operator = operator
        self.operands = []
        if operands is not None:
            for operand in operands:
                self.operands.append(operand)
        self.value = None
        self.name = name

    def attempt_compute(self, tree_dict):
        # if len(operands) == 1 and operands[0].isdigit():
        #     self.value = int(operands[0])
        #     return self.value
        # else:
        # TODO: HANDLE CASE OF OPERAND BEING NUMBER FOR OPS
        logging.debug("attempting compute for %s" % self.name)

        if self.value is not None:
            return self.value

        # short cut for dynamic programming
        if tree_dict[self.name]['answer'] is not None:
            self.value = tree_dict[self.name]['answer']
            return self.value

        if self.operator == 'IS':
            # logging.debug('got IS for %s' % self.name)
            if len(self.operands) == 1:
                if self.operands[0].isdigit():
                    self.value = int(self.operands[0]) % 2 ** 16
                    # logging.debug('got val %s for %s' %
                    #              (self.name, str(self.value)))
                    return self.value
                else:
                    self.value = tree_dict[self.operands[0]][
                        'tree'].attempt_compute(tree_dict)
                    return self.value
        elif self.operator == 'RSHIFT':
            lhs = int(self.operands[0]) if self.operands[0].isdigit() else tree_dict[
                self.operands[0]]['tree'].attempt_compute(tree_dict)
            rhs = int(self.operands[1]) if self.operands[1].isdigit() else tree_dict[
                self.operands[1]]['tree'].attempt_compute(tree_dict)
            self.value = (lhs >> rhs) % 2 ** 16
            return self.value
        elif self.operator == 'LSHIFT':
            lhs = int(self.operands[0]) if self.operands[0].isdigit() else tree_dict[
                self.operands[0]]['tree'].attempt_compute(tree_dict)
            rhs = int(self.operands[1]) if self.operands[1].isdigit() else tree_dict[
                self.operands[1]]['tree'].attempt_compute(tree_dict)
            self.value = (lhs << rhs) % 2 ** 16
            return self.value
        elif self.operator == 'AND':
            lhs = int(self.operands[0]) if self.operands[0].isdigit() else tree_dict[
                self.operands[0]]['tree'].attempt_compute(tree_dict)
            rhs = int(self.operands[1]) if self.operands[1].isdigit() else tree_dict[
                self.operands[1]]['tree'].attempt_compute(tree_dict)
            self.value = (lhs & rhs) % 2 ** 16
            return self.value
        elif self.operator == 'OR':
            lhs = int(self.operands[0]) if self.operands[0].isdigit() else tree_dict[
                self.operands[0]]['tree'].attempt_compute(tree_dict)
            rhs = int(self.operands[1]) if self.operands[1].isdigit() else tree_dict[
                self.operands[1]]['tree'].attempt_compute(tree_dict)
            self.value = (lhs | rhs) % 2 ** 16
            return self.value
        elif self.operator == 'NOT':
            if len(self.operands) == 1 and self.operands[0].isdigit():
                self.value = (~(int(self.operands[0]))) % 2 ** 16
                return self.value
            else:
                self.value = (
                    ~(tree_dict[self.operands[0]]['tree'].attempt_compute(tree_dict))) % 2 ** 16
                return self.value

    def to_string(self):
        operator_string = ""
        if self.operator in ["NOT", "IS"]:
            operator_string = "%s %s" % (self.operator, self.operands[0])
        else:
            operator_string = (" %s " % self.operator).join(self.operands)
        return "%s = %s" % (self.name, operator_string)


def process_wire(instruction, first=False):
    logging.debug("processing instruction %s" % instruction)
    vals = instruction.split(" -> ")
    # if vals[1].strip() not in instructions:
    #     logging.debug("couldn't find %s in instructions" % vals[1].strip())
    #     return False
    # check if vals[0] has an instruction
    instructions[vals[1].strip()] = vals[0].strip()
    if not first:
        logging.debug("entering not first")
        if any(substring in vals[0] for substring in instruction_list):
            logging.debug("found instruction in list")
            for item in instruction_list:
                logging.debug("checking %s" % item)
                m = re.search(item, vals[0].strip())
                if m is None:
                    logging.debug("wait - couldn't find it with re search")
                    continue
                else:
                    logging.debug("found instruction %s" % item)
                    inputs = vals[0].strip().split("%s " % item)
                    inputs = filter(None, inputs)
                    logging.debug("split line into: " + str(inputs))
                    processed = True
                    for i in inputs:
                        if not i.isdigit() and i.strip() not in instructions:
                            logging.debug(
                                "couldn't find %s in instructions" % i.strip())
                            logging.debug(instructions)
                            processed = False
                    if not processed:
                        return False
                    # valid instruction, do something
                    if item == 'RSHIFT' and inputs[0].strip() in instructions:
                        try:
                            instructions[vals[1].strip()] = (instructions[
                                inputs[0].strip()] >> int(inputs[1])) % 2**16
                            return True
                        except Exception as e:
                            print e
                            print inputs, vals
                            print instruction
                    elif item == 'LSHIFT' and inputs[0].strip() in instructions:
                        instructions[vals[1].strip()] = (instructions[
                            inputs[0].strip()] << int(inputs[1])) % 2**16
                        return True
                    elif item == 'AND' and inputs[0].strip() in instructions:
                        instructions[vals[1].strip()] = (instructions[
                            inputs[0].strip()] & instructions[inputs[1]]) % 2**16
                        return True
                    elif item == 'OR' and inputs[0].strip() in instructions:
                        instructions[vals[1].strip()] = (instructions[
                            inputs[0].strip()] | instructions[inputs[1]]) % 2**16
                        return True
                    elif item == 'NOT' and inputs[0].strip() in instructions:
                        instructions[
                            vals[1].strip()] = (~instructions[inputs[len(inputs)-1]]) % 2**16
                        return True
                    else:
                        return False
        else:
            logging.debug("no instruction found, checking for scalars")
            if re.search("\d", vals[0].strip()) is not None:
                logging.debug("found digit, doing direct assignment")
                instructions[vals[1].strip()] = int(vals[0].strip())
                return True
            else:
                # variable, so check for instructions or else queue
                if vals[0].strip() in instructions:
                    instructions[
                        vals[1].strip()] = instructions[vals[0].strip()]
                else:
                    return False
    return False


def main():
    open_file = "input"
    if args.debug_file:
        open_file = "debug_%s_%d" % (open_file, args.day)

    queue = []

    with open(open_file) as f:
        for line in f:
            lhs, rhs = line.strip().split(' -> ')
            operands = []
            if lhs.isdigit():
                lhs_operator = 'IS'
                operands.append(lhs)
            else:
                lhs_operator = None
                for operator in instruction_list:
                    m = re.search(operator, lhs)
                    if m is not None:
                        lhs_operator = lhs[m.start():m.start() + len(operator)]
                        break
                if lhs_operator is None:
                    # just do is assignment
                    # logging.debug("Bad input string = %s" % line)
                    # continue
                    lhs_operator = 'IS'
                # now identify operands
                operands_temp = filter(None, lhs.split(operator + " "))
                operands = []
                for operand in operands_temp:
                    operands.append(operand.strip())

            tree_node = TreeNode(rhs.strip(), lhs_operator, operands)
            instructions[tree_node.name] = {"tree": tree_node, "answer": None}
            logging.debug(tree_node.to_string())
    # for wire in instructions:
    #     print wire + ": "
    #     instructions[wire]['answer'] = instructions[
    #         wire]['tree'].attempt_compute(instructions)
    #     print str(instructions[wire]['answer'])

    print instructions['a']['tree'].attempt_compute(instructions)

    # print instructions['a'].attempt_compute(instructions)
    # result = process_wire(line, first=True)
    # if not result:
    #     queue.append(line)

    # print "finished reading file, now processing queue"
    # print instructions
    # print queue

    # test = len(queue)
    # while len(queue) > 0 and test > 0:
    #     logging.debug("processign queue at length %d" % len(queue))
    #     for i in queue:
    #         queue = queue[1:]
    #         result = process_wire(i)
    #         if not result:
    #             queue.append(i)
    #         test -= 1

    # print instructions
    # print queue
    # # if args.debug_file:
    # #     logging.debug("Expected: %s, got: %s, %s" % (
    # # args.expected, lights, "PASSED" if args.expected == lights else
    # # "FAILED"))

if __name__ == '__main__':
    main()
