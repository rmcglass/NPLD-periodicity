#!/bin/bash

for i in {0..33}
do
   sbatch --job-name=part1_NPLD${i} DTW_Sims1ToReal.sh 0 $i
   sbatch --job-name=part2_NPLD${i} DTW_Sims1ToReal.sh 25 $i
   sbatch --job-name=part3_NPLD${i} DTW_Sims1ToReal.sh 50 $i
   sbatch --job-name=part4_NPLD${i} DTW_Sims1ToReal.sh 75 $i
done
