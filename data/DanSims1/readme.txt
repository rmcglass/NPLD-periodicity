Test Simulations Batch 1
sent by Dan Lalich on 9/7/2022

**signal_tot.txt**: a csv file containing the simulated waveforms (each column is one simulation). I truncated them so that they begin ~25 samples before the surface reflection and are 600 samples long total. If you would prefer I could just give you the full 3600 sample waveform in the future but this helps keep file size down.

**eps_tot.txt**: csv file containing the dielectric profile used as input for each simulation.

**sep_and_dust.txt**: csv file with two columns containing input parameters for the simulations. The first column is the approximate average separation distance between dusty layers in the corresponding simulation, and the second column is the maximum dust content for the dusty layers.

From Dan: For each simulation, I randomly selected an average layer separation distance between 1-100 m, and a maximum dust content between 0-50%. Each dielectric profile is 1510 m thick, and dusty layers were allowed to be 1-10 m thick. Random values were drawn from uniform distributions. In practice what this means is that each simulated stratigraphy should have a dominant layer spacing, but that dominant spacing will be different from profile to profile. 
