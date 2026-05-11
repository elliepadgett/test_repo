"""
Name: testColorRange.py
Date: Feb 2026
Author: Ellie Padgett

This program determines the maximum and minimum y-values identified across the averages of each
image in each dataset. These two values are needed for accurate global scaling for all visualizations
(plots, images, and gifs) produced using these datasets; otherwise, the resulting plots are auto-scaled
and will not be globally aligned.

Each data set consists of 80 images contained in .npy files and should be stored in the 'reshaped_data'
folder. To change the location to search through, change the directory name on line 26.
"""

###
# IMPORTS
###
from pathlib import Path
import numpy as np
import average_analysis as aa

###
# FUNCTIONS
###
def colorRange(folder):
  folder_path = Path(folder)

  mx = []
  mn = []

  # currently checks for max/min element in each dataset;
  # want to find image with max/min average in each dataset!!
  for file_path in folder_path.iterdir():
      if file_path.is_file():
          data = np.load(file_path)

          y_axis = aa.average_analysis(data, file_path.name[-4:], plots=False)
          
          mx.append(np.max(y_axis))
          mn.append(np.min(y_axis))
  ## scaling back to counter the scaling in average_analysis
  return (np.max(mx)*(10**-5), np.min(mn)*(10**-5))

## printed in the format (Max y-value, min y-value)
print(colorRange("../reshaped_data"))
