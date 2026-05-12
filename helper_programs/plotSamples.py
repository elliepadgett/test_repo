"""
Name: plotSamples.py
Date: Feb 2026
Author: Ellie Padgett

This program visualizes some of the raw image data in a sample data set at different
points in time. These visualizations are used for the purpose of determining that the
data has been appropriately reshaped and scaled by the program contained in reshapeData.py. 
The selected figures have also been adjusted to display with an aspect ratio of 0.1, for 
better viewing.

The data set consists of 119 images as arranged in a reshaped D17_D*_*p.py file. Change the 
path in line 32 to pull from a different reshaped dataset.
"""

###
# IMPORTS
###
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
# from sklearn import metrics
# from scipy.spatial.distance import cdist
from pathlib import Path
import average_analysis as aa
import check_displacement as cd


###
# GLOBALS
###
folderpath = "../reshaped_data"
ymax, ymin = cd.colorRange(folderpath)
ymin2 = round(ymin*(10**6), 2)
ymax2 = round(ymax*(10**6), 2)

###
# MAIN PROGRAM 
###
for title in Path(folderpath).iterdir():
  ## plotting images for the specified dataset (plan to automate), square-like for better visualization
  dpl = np.load(folderpath + "/" + title.name)[:30]
  dpl = dpl*(10**6)
  plt.figure(figsize=(10, 8))
  plt.subplots_adjust(wspace=0.6, hspace=0.6)

  ## plot and title each image 0-29 in the same figure
  rng = np.linspace(0, 29, 30)
  for i in range(1, 31):
    plt.subplot(5, 6, i)
    plt.title("Image " + str(int(rng[i-1])), pad=15)
    img = plt.imshow(dpl[int(rng[i-1])], aspect = 0.1, vmin=ymin*(10**6), vmax=ymax*(10**6))
    plt.axis('off')
    cbar = plt.colorbar(img)
    cbar.set_ticks([ymin2, 0, ymax2])
  
  plt.suptitle(f"{title.name[:-4]}")

  ## save when done and/or show, comment out as needed!
  # plt.savefig("premade_visuals/samples/" + title.name[:-4] + ".png")
  plt.show()