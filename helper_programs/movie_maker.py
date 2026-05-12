"""
Name: movieMaker.py
Date: Apr 2025
Author: Ellie Padgett

This program creates and saves a movie animation of the selected reshaped dataset. 

IMPORTANT: Before running this program, make sure the loaded dataset is the appropriate .npy
file, AND that the name of the save file is not the same as an existing .gif in your directory!

The data set consists of 119 images as arranged in the file *reshaped.npy. Change the 
filepath in line 39 to pull from a different reshaped dataset.

Refs: 
    https://matplotlib.org/stable/users/explain/animations/animations.html
"""

###
# IMPORTS
###
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path
import check_displacement as cd

###
# GLOBALS
###

## change the path to the folder containing the data to inspect
ymax, ymin = cd.colorRange("../reshaped_data")

###
# FUNCTIONS
###
def make_movie(dataset, save=False):
  data = np.load(dataset)

  fig, ax = plt.subplots()

  # initiate an empty  list of "plotted" images 
  myimages = []

  # loops through provided images
  for p in range(data.shape[0]):
      # set the title text and image for each frame
      title = ax.text(0.5, 0.98, f"t = {p}", ha="center", va="top", transform=ax.transAxes, fontsize=16)
      title.set_bbox(dict(facecolor='white', alpha=1, edgecolor='darkturquoise'))
      img = ax.imshow(data[p], aspect = 0.1, vmin=ymin, vmax=ymax)
      plt.title(dataset.name[:-4])
      # add the plotted image object to the list with its title
      myimages.append([img, title])

  # create an instance of animation
  anim = animation.ArtistAnimation(fig, myimages, interval=10, blit=True, repeat_delay=10)

  ## change the name of this save destination as needed when creating a new GIF
  if save:
    print(f"Saving {dataset.name[:-4]} movie...")
    anim.save("../premade_visuals/gifs/" + str(dataset.name[:-4]) + ".gif")
    
  else:
    ## showtime! preview the GIF without saving a copy
    plt.show()

###
# MAIN PROGRAM
###
def main():
  ## change this filepath to work with a different reshaped dataset!
  path = Path("../reshaped_data")
  for dataset in path.iterdir():
    make_movie(dataset, save=True)

if __name__ == "__main__":
  main()
