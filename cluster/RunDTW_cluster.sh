#!/bin/bash
# requires bash 4.0+

for i in {0..98..2}
do
   nextSim=$((i+1))
   sbatch --job-name=Sim${i}_${nextSim}_vsRealNPLD DTW_real2Sim1.sh $i
done

