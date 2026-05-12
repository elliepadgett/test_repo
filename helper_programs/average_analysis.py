"""
Name: average_anaylysis.py
Date: Apr 2025
Author: Ellie Padgett

This program analyzes the initial pulse contained within the first 30 images. For each L = 60:10:80,
a square of width L is sliced from the center of each image and the average color is computed for that square 
section. Each L-square's behavior will be plotted over time. Currently able to plot up to four designs per figure.

The data set consists of 119 images as arranged in the file d*_50v_reshaped.npy. Change the 
filepaths in lines 60, 139, and/or 145 to pull from different reshaped datasets. 

"""

###
# IMPORTS
###
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

###
# GLOBALS
###
# for new d17 datasets, determined by check_displacement.py
ymin = (10**5)*(-1.1115019440364524e-06)
ymax = (10**5)*(2.3261941377613877e-07)


###
# FUNCTIONS
###
def average_analysis(datasets, title="Untitled", save = False, show=False, byL = False):
    """
    Computes the average color in a square of width L = 60:10:80 for images 0-29 in the
    provided dataset. The averages for this dataset are stored in a list for each L-square,
    and each of those lists is appended to a numpy array containing the totals for each
    L-square.

    Parameters:
        data ([string]): the filepath(s) of the reshaped dataset(s) to be analyzed
        title (string):  the name of the dataset to be worked with, in order to dynamically 
                         label the plot(s) correctly
        save (bool):     true to save the generated plots without showing; false otherwise
        show (bool):     true to show the generated plots; false otherwise
        byL (bool:)      true to plot the datasets organized by L-size; false to plot by design (default)
    
    Return:
        list: the 2D list containing the lists of averages computed for each L-square
    """
    length = np.linspace(60, 80, 11) # different values of L to check out
    x_axis = np.linspace(0, 29, 30) # indices of the images to analyze
  
    all_L = [] # collection array for L samples
    
    if save or show:
      plt.figure(figsize=(10, 9))

    for x in range(len(datasets)):
      data = np.load('../reshaped_data/' + datasets[x] + '.npy')[:30]
      height, width = data.shape[1:] # (119), 5000, 471 (for d*_50v experiments)
      scale = height/width # approx 10.6
      scale_approx = math.floor(scale) # need an integer for image slicing
      for l in length: # for each L
          y_axis = [] # average color value
          for i in x_axis: # analyze all images
              # need l to be an integer for image slicing
              l = int(l)
              
              # crop the chunk of the image we want (dependent on L-square, mult l by approx 10 on height to get scaled square)
              sq = data[int(i)][height//2 - l*scale_approx//2 : height//2 + l*scale_approx//2, width//2 - l//2 : width//2 + l//2]
              
              # average color of the L-square
              avg = np.mean(sq) # average over entire array of positive color values
              y_axis.append(avg*(10**5))
              
          if save or show:
            ## plot each L-trend by L size
            if byL:
              if l < 68:
                  plt.plot(x_axis, y_axis, color = 'lightseagreen')
              elif l < 76:
                  plt.plot(x_axis, y_axis, color = 'orange')
              else:
                  plt.plot(x_axis, y_axis, color = 'firebrick')
            else: 
              ## plot each L-trend by design
              if x == 0:
                  plt.plot(x_axis, y_axis, color = 'lightseagreen')
              elif x == 1:
                  plt.plot(x_axis, y_axis, color = 'orange')
              elif x == 2:
                plt.plot(x_axis, y_axis, color = 'teal')
              else:
                  plt.plot(x_axis, y_axis, color = 'firebrick')
            
          all_L.append(y_axis)
          y_axis = []
    
    if save or show:
      ## add legend, labels (handles), global axes, title
      if byL:
        ## create handles by L-range
        small = mpatches.Patch(color='lightseagreen', label="L: 60 - 66")
        med = mpatches.Patch(color='orange', label="L: 68 - 74")
        large = mpatches.Patch(color='firebrick', label="L: 76 - 80")
        handles = [small, med, large]
      else:
        ## create handles by design
        handles = []
        colors = ["darkturquoise", "orange", "teal", "firebrick"]
        for i in range(len(datasets)):
          handles.append(mpatches.Patch(color=colors[i], label=datasets[i]))

      if byL:
        des = "L-size"
      else:
        des = "Design"
      plt.legend(handles=handles, loc='lower right')
      plt.xlabel("Time (\u03BCs)")
      plt.ylabel("Average Displacement (\u03BCm)")
      plt.ylim(ymin, ymax)
      plt.title(f"{title}: Average Color Behavior over Time (Organized by {des})")
    
    ## save figure to specified file path (edit as needed)
    if save:
      plt.savefig("../premade_visuals/avg_behavior/" + title + ".png")
    if show:
      ## show the figure (without saving it)
      plt.show()

    ## returns the computed averages (y-axis values) for each time series
    return all_L


###
# MAIN PROGRAM
###
def main():
    ## to use the entire folder of datasets
    names = Path("../reshaped_data").iterdir()
    for name in names:
      name = name.name[:-4]
      average_analysis([name], name, byL=True, save=False, show=True)

    ## to plot multiple designs in the same figure, choose the set of up to four designs to work with --> these are the original four I chose
    names = ["D17_D1_7p", "D17_D8_2p", "D17_D2_0p", "D17_D1_np"]
    average_analysis(names, "four_designs_byL", byL=False, save=False, show=True)
    

if __name__ == "__main__":
    main()