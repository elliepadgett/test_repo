"""
Name: overlaySquare.py
Date: Apr 2025
Author: Ellie Padgett

This program provides a visualization to accompany the program averagingAnalysis.py. The produced
plot's first subplot displays a slice from the selected image (a square of the adjustable size L) 
beside a colorbar representing the spread in the slice. The second subplot contains the full image
with a red square overlaid on the area that represents the location of the L-square slice in the
first subplot.

This file is primarily relevant for the older, larger d*_50v_reshaped.npy files contained in the 
old_reshaped folder. The newer datasets from the D17 experiments were trimmed to match the expected
square size preemptively, so this visual comparison is not helpful for those datasets.

The data set consists of 119 images as arranged in the file d*_50v_reshaped.npy. Change the 
filepath in line 31 to pull from a different reshaped dataset.
"""

###
# IMPORTS
###
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

###
# MAIN PROGRAM
###
## change this filepath to work with another reshaped dataset!
data = np.load('../old_reshaped/d1_50v_reshaped.npy')

num, height, width = data.shape # 119, 5000, 471 (for d*_50)
scale = height/width # approx 10.6
scale_approx = round(scale) # need an integer for image slicing; 10 or 11 both seem to work fine, but I've not
                  # yet done any error analysis

l = 80 # dimensions of largest square; adjust as needed

# center and build the square; x,y represent left bottom corner
x, y = width/2 - l/2, height/2 - l*scale_approx/2
square = patches.Rectangle((x, y), l, l*scale_approx, facecolor='none', edgecolor='r')

# crop the chunk of the image we want (dependent on L-square, mult l by approx 10 on height to get scaled square)
t = 10 # image slice to visualize; change as needed
fig, ax = plt.subplots(1,2)
sq = data[t][height//2 - l*scale_approx//2 : height//2 + l*scale_approx//2, width//2 - l//2 : width//2 + l//2]
sq = [x*(10**6) for x in sq]
img = ax[1].imshow(sq, aspect = 0.1) # zoomed-in data
cmap = img.cmap
ax[1].axis('off')
ax[0].set_title(f"L-Square: {l}")
ax[0].imshow(data[t], aspect = 0.1) # original data
ax[0].axis('off')
ax[0].add_patch(square) # overlay square onto original image
cbar = plt.colorbar(img)
cbar.set_label("Displacement (\u03BCm)")

## show the figure!
plt.show()