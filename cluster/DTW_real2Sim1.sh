#!/bin/bash                                                                 
#SBATCH -A bramsona                                                             
#SBATCH -t 8:00:00                                                              
#SBATCH --mem-per-cpu=500

cd '/home/rmcglass/NPLD_FFT_DTW/cluster'

#module load use.own
#module load conda-env/mypackages/py3.7.6


# run DTW with input 1, the starting sim to run (remember python zero indexing)

./DTW_RealtoSims1_cluster.py $1
                       
