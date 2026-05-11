
<h1 align="center">

  <br>

  Utility and Visualization Scripts

  <br>

</h1>

<p align="center">
  <a href="#purpose">Purpose</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#overview">Overview</a> •
  <a href="#visualization-programs">Visualization Programs</a> •
  <a href="#utility-scripts">Utility Scripts</a> •
  <a href="#existing-visuals-and-tables">Existing Visuals and Tables</a>
</p>

  
<!--  A gif to demonstrate what the program does -->

<div align=”center”>

</div>

## Purpose

This collection of scripts was developed to assist in determining an appropriate "window" size through which to further analyze the displacement of a tissue simulant over time after receiving a pulse from an ultrasound wave. 

## How To Use

To use these programs, you must have [Python](<https://www.python.org/downloads/release/python-3100/>) installed.

Then, clone this repository. Navigate to the folder you want to add the scripts to and run these commands on your [Git Bash](<https://git-scm.com/install/windows>) (**Note:** these instructions are for Windows devices only).

```bash

# Clone this repository  
$ git clone https://github.com/elliepadgett/test_repo.git

# Go into the repository  
$ cd test_repo

# Install the required libraries  
$ pip install -r requirements.txt

```

## Overview

```
📂 helper_programs           # Contains all utility and visualization scripts
├── average_analysis.py       # Average over a "square" area to generate the complete time series curve
├── movie_maker.py            # Generate GIFs from raw or reduced data
├── overlay_square.py         # Visualize square placement on the whole image
├── plot_samples.py           # Probe the timeline one image at a time
├── reshape_data.py           # Transform from .mat format to .npy
├── check_displacement.py     # Identify global y-axis limits for all datasets
└── unique_runs.py            # Generate all unique k++ initializations for the specified dataset(s) and perform Kmeans clustering
📂 premade_visuals           # Contains old/existing plots, images, samples 
├── 📂 avg_behavior          # Behavior of displacement averages over time by dataset
├── 📂 clusters              # Cluster membership for all realizations
├── 📂 gifs                  # Movies of raw data
└── 📂 pooled_experiments    # Behavior and supplemental visuals for pooled experiments
📂 raw_data                  # Contains all original .mat files
├── D17_D1_7p.mat
└── ...
📂 reshaped_data             # Contains all reshaped .npy files
├── D17_D1_7p.npy
└── ...
📂 results                   # Contains all tables and interpretations to date
└── membership_and_purity.pdf
```

## Visualization Programs
#### A collection of programs which exclusively produce various visuals (GIFs, snapshots, etc.) from the raw or reduced data.
- **movie_maker.py**: takes a .npy file representing the reshaped dataset and creates a .gif that plays the movie. This .gif can be saved or simply shown when the program is run, depending on if you want to keep the visual for later. Both .gif files in the **visualizations** folder were created from this script.
- **overlay_square.py**: takes a .npy file representing the reshaped dataset and creates a plot displaying the "zoomed-in" LxL square of an image, the corresponding colorbar, and the full image with a red square overlaid in the approximate region where the cropped square was taken from. The current form of this script will create a plot for one image at a time, the index of which may be user-determined according to comments in the code.
- **plot_samples.py**: takes a .npy file representing the reshaped dataset and plots stretched images of the user-determined samples. In its current form, the plot contains three images at roughly equidistant timesnaps in the chosen dataset, but these indices may be changed as needed to show a different set of images.

## Utility Scripts
#### A collection of programs that do the bulk of the analytical work for this project.
- **reshape_data.py**: the first step before working with any of the other files in this repository. This program takes in a .mat file of time-ordered images and reshapes them so they can be represented more appropriately as images in Python. The contents of the .mat file are reshaped and stored in a .npy file for later use. Use the reshaped .npy file instead of the original .mat for all other analysis purposes.
- **average_analysis.py**: takes a .npy file representing the reshaped dataset and generates a plot of the average color in an LxL square over time, where L is an integer. The number of images from the dataset and the range of Ls to analyze can be changed to alter the focus of the analysis. This script is also responsible for producing organized time-series plots of the specified dataset(s).
- **unique_runs.py**: Performs k x len(range of L) many unique k++ initializations for running K-means clustering on the specified dataset.
- **cross_validation.py**: Determines the consistency of the clustering scheme by cross-referencing all possible initializations from all possible combinations of training sets. Each training set is composed of 4 datasets, one from each design (7p, 2p, 0p, and np). After training a kmeans model using a training set, all other datasets in the folder (12 total) are fed into it and placed into their predicted clusters. Finally, the program checks how consistent the different models are in determining which designs dominate which clusters.

## Existing Visuals and Tables
#### Includes membership and purity tables as well as pre-made time series GIFs, cluster membership plots, and visuals showing average displacement over time for the included raw/reshaped datasets in this repository.
