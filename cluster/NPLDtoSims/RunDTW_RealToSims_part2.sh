#!/bin/bash

for i in {0..99}
do
   sbatch --job-name=Sim${i} DTW_real2Sim1_part2.sh $i
done
