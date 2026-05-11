"""
Name: reshape_data.py
Date: Mar 2025
Author: Ellie Padgett

This program loads sample image data from a .mat file and reshapes it into an
appropriately size numpy array (originally 119x5000x471, but this program is flexible
to changes in those dimensions).

The data set consists of n images, each measuring mxl, as arranged in the delivered .mat files. 
However, the dictionary loaded from this file has them organized into a 3D array of dimensions 
mxlxn, so it must be reshaped prior to visualization, clustering, and further analysis. Change 
the filepath in line 26/27 to pull from a different dataset, and change the filepath in line 50 to save 
to a file with a different name/location. (For the large, original datasets, don't be surprised if this
program takes up to 10 minutes to run.)

"""
###
# IMPORTS
###
import numpy as np
import scipy.io as scp
from pathlib import Path

# data file contains: n (119) images, each mxl (5000x471) in originals
for title in Path("../raw_data").iterdir():
  data = scp.loadmat('../raw_data/' + title.name)

  # here we're just just stacking the array elements from front to back until it fills everything in;
  # I want to rotate the 3D array and then slice it into images lengthwise from the base of n (119)
  data = data['filtered_dpl'] # 5000x471x119

  # set dimensions:
  h, w, n_images = data.shape

  # reshape iteratively
  dpl = np.zeros((n_images, h, w))
  for i in range(h):
    arr = data[i] # 471x119
    size = len(arr) # 471
    for j in range(size):
        vec = arr[j] # 119x1
        length = len(vec) # 119
        for k in range(length):
          dpl[k, i, j] = vec[k]

  ## save to a new .npy file for future use
  # --> !!!change destination filepath between datasets to avoid overriding data!!!
  print(title.name[:-4], "saving...")
  np.save('../reshaped_data/' + title.name[:-4] + '.npy', dpl)

print("\nFiles saved successfully!")
