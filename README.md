# NPLD-periodicity

### Written by Riley McGlasson in Februrary 2022

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
NPLDFFTradar_many-nosurface.ipynb and korolevFFTradar_many-nosurface.ipynb: Computes FFTs of radar depth profiles fpr the NPLD and Korolev, respectively. Also creates 20,000 randomly generated synthetic depth profiles with the same mean, standard deviation, lag 1 autocorrelation, and best fit skewed gaussian and computes FFTs of them as well. These are used to plot the mean and +2 std wavelength power spectra.  

DynamicTimeWarping_KtoK.ipynb and DynamicTimeWarping_KtoNPLD.ipynb: Tunes depth profiles of Korolev to each other and Korolev to the NPLD, using a dynamic time warping algorithm. Plots these tunings and computes cross correlations. For each tuning, this also tunes 1000 randomly generated depth profiles to assess the goodness of fit.

#### Output files:
FFTplots: Holds plots of depth profiles, example random synthetic profile, and wavelength spectra for each data site.
KKplots: Holds output plots from tuning each of the 5 Korolev sites to each other
KNplots: Holds output plots from tuning each NPLD site to each Korolev site

#### ./cluster folder:
./cluster holds a verison of this code that was split up for parallel use on Purdue's Bell computing cluster.
