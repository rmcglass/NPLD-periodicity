#!/bin/bash                                                                 
#SBATCH -A bramsona                                                             
#SBATCH -t 8:00:00                                                              
#SBATCH --mem-per-cpu=4G


#module load use.own
#module load conda-env/mypackages/py3.7.6

cd '/home/rmcglass/NPLD_FFT_DTW/cluster/NPLDvNPLD_g1p2'

# run DTW with input 1, the first NPLD to run (of 17) (remember python zero indexing)
# input 2 is the NPLD profile to run (1 at a time)
python DTW_NPLDtoNPLD.py $1 $2
                       
