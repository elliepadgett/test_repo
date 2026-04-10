
<h1 align="center">

  <br>

  Ellie’s Utility and Visualization Scripts

  <br>

</h1>

<p align="center">
  <a href="#purpose">Purpose</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#overview">Overview</a> •
  <a href="#">Visualization Programs</a> •
  <a href="#">Utility Functions</a> •
  <a href="#">Existing Visuals</a>
</p>

  
<!--  A gif to demonstrate what the program does -->

<div align=”center”>

</div>

## Purpose

<!--- Write a short paragraph / talk about some purpose here --->

## How To Use

To use these programs, you must have \[Python\](<https://www.python.org/downloads/release/python-3100/>) installed.

Then, clone this repository. Navigate to the folder you want to add the scripts to and run these commands on your \[Git Bash\](<https://git-scm.com/install/windows>) (**Note:** these instructions are for Windows devices only).

```bash

# Clone this repository  
$ git clone REPLACE_ME

# Go into the repository  
$ cd REPLACE_ME

# Install the required libraries  
$ pip install -r requirements.txt

```

## Overview

```
📂 helper_program
├── ...
├── docs                    # Documentation files (alternatively `doc`)
│   ├── 📄 TOC.md              # Table of contents
│   ├── faq.md              # Frequently asked questions
│   ├── misc.md             # Miscellaneous information
│   ├── usage.md            # Getting started guide
│   └── ...                 # etc.
└── ...
```

## Visualization Programs

- [Movie Maker](#movie_maker)
- [Overlay Square](#overlay_square)
- [Plot Samples](#plot_samples)

<!--- Replace these with your file names --->

### Movie Maker

```python
```

- **averagingAnalysis.py**: takes a .npy file representing the reshaped dataset and generates a plot of the average color in an LxL square over time, where L is an integer. The number of images from the dataset and the range of Ls to analyze can be changed to alter the focus of the analysis.
- **movieMaker.py**: takes a .npy file representing the reshaped dataset and creates a .gif that plays the movie. This .gif can be saved or simply shown when the program is run, depending on if you want to keep the visual for later. Both .gif files in the **visualizations** folder were created from this script.
- **overlaySquare.py**: takes a .npy file representing the reshaped dataset and creates a plot displaying the "zoomed-in" LxL square of an image, the corresponding colorbar, and the full image with a red square overlaid in the approximate region where the cropped square was taken from. The current form of this script will create a plot for one image at a time, the index of which may be user-determined according to comments in the code.
- **plotSamples.py**: takes a .npy file representing the reshaped dataset and plots stretched images of the user-determined samples. In its current form, the plot contains three images at roughly equidistant timesnaps in the chosen dataset, but these indices may be changed as needed to show a different set of images.
- **reshapeData.py**: the first step before working with any of the other files in this repository. This program takes in a .mat file of time-ordered images and reshapes them so they can be represented more appropriately as images in Python. The contents of the .mat file are reshaped and stored in a .npy file for later use. Use the reshaped .npy file instead of the original .mat for all other analysis purposes!!
- **uniqueRuns.py**: