#!/bin/bash

for i in `seq 1 25`
do
  j=`printf %02d $i`
  mkdir day${j}
  touch day${j}/day${j}.py
  touch day${j}/input
  touch day${j}/debug_input_1
  touch day${j}/debug_input_2
done
