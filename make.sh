#!/bin/bash

for i in `seq 6 30`
do
  mkdir day${i}
  touch day${i}/day${i}.py
  touch day${i}/input
  touch day${i}/debug_input_1
  touch day${i}/debug_input_2
done