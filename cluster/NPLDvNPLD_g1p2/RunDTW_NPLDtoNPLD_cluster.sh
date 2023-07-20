#!/bin/bash

for i in {0..33}
do
   sbatch --job-name=part1_NPLD${i} DTW_NPLDtoNPLD.sh 0 $i
   sbatch --job-name=part2_NPLD${i} DTW_NPLDtoNPLD.sh 17 $i
done
