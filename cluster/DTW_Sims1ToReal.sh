#!/bin/bash                                                                 
#SBATCH -A bramsona                                                             
#SBATCH -t 8:00:00                                                              
#SBATCH --mem-per-cpu=4G


#module load use.own
#module load conda-env/mypackages/py3.7.6

cd '/home/rmcglass/NPLD_FFT_DTW/cluster'

# run DTW with input 1, the starting sim to run (remember python zero indexing)
# input 2 is the NPLD profile to run
python DTW_Sims1ToReal.py $1 $2
                       
