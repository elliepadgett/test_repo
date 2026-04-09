"""
Name: averagingAnaylysis.py
Date: Apr 2025
Author: Ellie Padgett

This program analyzes the initial pulse contained within the first 30 images. For each L = 60:10:80,
a square of width L is sliced from the center of each image and the average color is computed for that square 
section. Each L-square's behavior will be plotted over time.

The data set consists of 119 images as arranged in the file d*_50v_reshaped.npy. Change the 
filepath in the main function to pull from a different reshaped dataset. 

"""

###
# IMPORTS
###
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

###
# GLOBALS
###
# for new d17 datasets, determined by testColorRange.py
# ymin = -13.680035515970473e-01
# ymax = 3.3261941377613874e-01

# for old twoper datasets, determined by visual inspection but can be revised by testColorRange.py
ymax = 2
ymin = -2


###
# FUNCTIONS
###

def averageAnalysis(data=np.array([]), title="Untitled"):
    """
    Computes the average color in a square of width L = 60:10:80 for images 0-29 in the
    provided dataset. The averages for this dataset are stored in a list for each L-square,
    and each of those lists is appended to a numpy array containing the totals for each
    L-square.

    Parameters:
        data (np.array): the reshaped data to be analyzed
        title (string): the name of the dataset to be worked with, in order to dynamically 
        label the plot(s) correctly
    
    Return:
        list: the 2D list containing the lists of averages computed for each L-square
    """
    length = np.linspace(10, 100, 10) # different values of L to check out
    data_points = np.linspace(0, 29, 30) # indices of the images to analyze
    x_axis = data_points # the point in time
    
    all_L = [] # collection array for L samples
    plt.figure(figsize=(10, 9))

    ## for plotting average analysis of all datasets together (comment out when not needed) --> plan to automate
    # names = ["D17_D1_7p", "D17_D8_2p", "D17_D2_0p", "D17_D1np"] # newer D17 datasets
    # names = ["d1_50v_reshaped", "d2_50v_reshaped"] # older D1-2 datasets

    for x in range(2):
      ## for plotting average analysis of all datasets together --> plan to automate
      # data = np.load('old reshaped/' + names[x] + '.npy')[:30] # (comment out when not needed)
      height, width = data.shape[1:] # (119), 5000, 471 (for d*_50v experiments)
      scale = height/width # approx 10.6
      scale_approx = math.floor(scale) # need an integer for image slicing; 10 or 11 both seem to work fine, but I've not
                                       # yet done any error analysis
      for l in length: # for each L
          y_axis = [] # average color value
          for i in data_points: # analyze all images
              # need l to be an integer for image slicing
              l = int(l)
              
              # crop the chunk of the image we want (dependent on L-square, mult l by approx 10 on height to get scaled square)
              sq = data[int(i)][height//2 - l*scale_approx//2 : height//2 + l*scale_approx//2, width//2 - l//2 : width//2 + l//2]
              
              # average color of the L-square
              avg = np.mean(sq) # average over entire array of positive color values
              y_axis.append(avg*(10**5))
              

          ## plot each L-trend by L size --> plan to automate
          # if l < 68:
          #     plt.plot(x_axis, y_axis, color = 'lightseagreen')
          # elif l < 76:
          #     plt.plot(x_axis, y_axis, color = 'orange')
          # else:
          #     plt.plot(x_axis, y_axis, color = 'firebrick')

          ## plot each L-trend by design --> plan to automate
          # if x == 0:
          #     plt.plot(x_axis, y_axis, color = 'lightseagreen')
          # elif x == 1:
          #     plt.plot(x_axis, y_axis, color = 'orange')
          # elif x == 2:
          #   plt.plot(x_axis, y_axis, color = 'teal')
          # else:
          #     plt.plot(x_axis, y_axis, color = 'firebrick')
          
          plt.plot(x_axis, y_axis)


          all_L.append(y_axis)
          y_axis = []
          
    ## constructing legend for plot, organized by square size L --> plan to automate
    legend = []
    for i in range(0, length.size):
        legend.append('L = ' + str(int(length[i])))


    ## create handles by color (by design) --> plan to automate
    # d7p = mpatches.Patch(color='darkturquoise', label=names[0][-2:])
    # d2p = mpatches.Patch(color='orange', label=names[1][-2:])
    # d0p = mpatches.Patch(color='teal', label=names[2][-2:])
    # dnp = mpatches.Patch(color='firebrick', label=names[3][-2:])

    ## create handles by color (by L-range)
    # small = mpatches.Patch(color='lightseagreen', label="L: 60 - 66")
    # med = mpatches.Patch(color='orange', label="L: 68 - 74")
    # large = mpatches.Patch(color='firebrick', label="L: 76 - 80")
    
    ## add legend, labels (handles), global axes, title
    plt.legend(legend, loc='lower right')
    plt.xlabel("Time (\u03BCs)")
    plt.ylabel("Average Displacement (\u03BCm)")
    plt.ylim(ymin, ymax)
    plt.title(title + ": Average Color Behavior over Time (Organized by Design)")
    
    ## save figure to specified file path (edit as needed) --> plan to automate
    # plt.savefig("visualizations/prev_visuals/" + title + ".png")

    ## show figure (comment out as needed)
    # plt.show()

    ## returns the computed averages (y-axis values) for each line (either designs, L-sizes, or both)
    return all_L


###
# MAIN PROGRAM
###
def main():
    ## choose one set of designs to work with --> plan to automate
    # names = ["D17_D1_7p", "D17_D8_2p", "D17_D2_0p", "D17_D1np"]
    names = ["d1_50v_reshaped", "d2_50v_reshaped"]

    for title in names:
      data = np.load('old reshaped/' + title + '.npy')[:30]
      # title = "Four Designs"
      averageAnalysis(data, title)

      ## if we only want to run a specific design once; otherwise all in the list will generate visuals --> plan to automate
      # break
    

if __name__ == "__main__":
    main()