# NPLD-periodicity

### Written by Riley McGlasson

##### A collection of Python functions and Jupyter Notebooks that quantitatively asses similarities between the radar stratigraphy of the Martian NPLD and Korolev crater.

---

![NPLDlocations](https://user-images.githubusercontent.com/34108989/156832352-bbfc1187-7a5d-40b7-8892-044fdcb08997.png)![Korolevlocations](https://user-images.githubusercontent.com/34108989/156836781-d7c40b29-2bc3-4161-8865-e8c086517cbc.png)  
Depth profile sites for NPLD and Korolev crater.

---

This repository contains everything, from the input data to the output files, needed to run this analysis.

#### Input data:
./data holds the .csv files that hold the depth profile data from the SHARAD radargrams extracted at the points on the maps above, sorted into NPLD and Korolev. Korolev and Korolev 2 are the same profiles, but Korolev2 is a slightly more zoomed version that I was experimenting with, and think is more accurate for the DTW algorithm. The folder DanSims1 contains the simulated waveforms constructed from modeled ice and dust stratigraphies.

#### Python Function Files:
radarfuncs.py: Holds three functions used for FFT and DTW analysis. 
- p2m_waterice converts depth in SHARAD pixels to depth in meters assuming a dielectric constant of water ice.
- fft_radar computes the wavelength power spectra of a radar depth profile
- ar1 produces an AR1 (Markov) series with the same length and lag-1 autocorrelation as the input depth profile, and fit to the same best fit skewed gaussian.

DTWfuncs.py: Holds 2 functions for running dynamic time warping algorithm
- normPH demeans and normalizes a given input function to unit std.
- dtw_mars takes one radar depth profile and tunes it to another using dynamic time warping. DTw computes a matrix (d) of squared differences between the two inputs, then computes a cost matrix from d, and finds the minimum cost path to traverse the cost matrix.

#### Jupyter Notebooks:
NPLDFFTradar_many-nosurface.ipynb, korolevFFTradar_many-nosurface.ipynb, and sims1-FFTradar_many-nosurface.ipynb: Computes FFTs of radar depth profiles for the NPLD, Korolev and the simulated stratigraphies, respectively. Also creates 20,000 randomly generated synthetic depth profiles with the same mean, standard deviation, lag 1 autocorrelation, and best fit skewed gaussian and computes FFTs of them as well. These are used to plot the mean wavelength power spectra.  

DynamicTimeWarping_KtoK.ipynb, DynamicTimeWarping_KtoNPLD.ipynb, and DynamicTimeWarping_RealToSims1.ipynb: Tunes depth profiles of Korolev to each other, Korolev to the NPLD, and NPLD to simulated stratigraphies using a dynamic time warping algorithm. Plots these tunings and computes cross correlations. For each tuning, this also tunes 1000 randomly generated depth profiles to assess the goodness of fit. Warning: these are pretty computationally intense, so I recommend only using the Jupyter notebooks for small numbers of model runs. To run DTW on all of the simulations, I used the version of the code in ./cluster.

#### Output files:
FFTplots: Holds plots of depth profiles, example random synthetic profile, and wavelength spectra for each data site.
DTW_outputs: Holds output plots from DTW tunings of Korolev to Korolev (KtoK_outputs), Korolev to NPLD (KtoNPLD_outputs), NPLD to Korolev (NPLDtoK_outputs), simulated stratigraphies to NPLD (Sims1toNPLD_outputs), NPLD to simulated stratigraphies (NPLDtoSims1_outputs), and NPLD to NPLD (NtoN_outputs).

#### cluster folder:
./cluster holds verisons of this code that were split up for parallel model runs on Purdue's Bell computing cluster.


