"""
Name: unique_runs.py
Date: Nov 2025
Author: Ellie Padgett

Performs k x len(range of L) many unique k++ initializations for running K-means clustering on the specified dataset.
The supporting functions kmeans_pp_with_fixed_first() and all_kmeanspp_initializations() were originally drafted with
support from Claude Sonnet 4.5 and tailored by the programmer to better fit the context of the problem.

"""

###
# IMPORTS
###
import numpy as np
import average_analysis as aa
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import check_displacement as cd

###
# GLOBALS
###

# y-axes for the newer D17 datasets
ymax, ymin = cd.colorRange("../reshaped_data")


###
# FUNCTIONS
###

def clustering_L(data, d, centroids, k, idx, title, save=False, show=False, print=False):
  """
  Clustering for each dataset, cluster over L = 60:80:2 for specified dataset option and number of clusters
  
  Parameters:
    data (pd.DataFrame):          the vectors to cluster (represent the y-axes computed in average analysis step)
    d (np.ndarray):               identical data, just in a different structure to help with compartmentalizing labels
    centroids (list[np.ndarray]): a length-n list of centroid arrays, each shape (k, m) where n = len(selected dataset)
    k (int):                      the specified number of clusters
    idx (int):                    the number of the current iteration/realization of the clustering scheme (used for labeling in plots and terminal output)
    title (str):                  the name of the dataset/pooled dataset being clustered in this realization (used for labeling saved figures)
    save (bool):                  true to save the plots, false to not (default)
    show (bool):                  true to display the plots, false to not (default)
    print (bool):                 true to print iteration data; false to not (default)

  Returns:
    float:                        the overall coherence of this clustering realization

  Output:
    - Generates a kx1 subplot figure of all clusters for this iteration, displaying centroid and cluster elements
    - Terminal output (can redirect to a file to save for later) includes:
      - cluster labels corresponding to each cluster element as a list (this information is used later to determine cluster membership by design)
      - an indicator of the tightest cluster in each iteration (determined by lowest intracluster coherence)
      - the intracluster coherence of each cluster, corresponding to its cluster label
      - this iteration's overall coherence (sum of intracluster coherences) for comparing cluster "tightness" across multiple iterations
  """
  
  ## using scikit-learn's kmeans package
  kmeans = KMeans(n_clusters=k, init=centroids, n_init=1)
  kmeans.fit(data)
  labels = kmeans.labels_
  centroids = kmeans.cluster_centers_

  ## prints the labels mapping each vector to the cluster it landed in
  if print:
    print("Labels:")
    print(labels)

  # intra-cluster distance: distances between points in the same cluster
  ic_dists = []
  for i in range(k):
      c_pts = d[labels == i]
      cntr = centroids[i]
      # sum of squared euclidean distances
      ssd = np.sum((c_pts - cntr)**2)
      ic_dists.append(ssd*(10**2)) # scale for readability in terminal

  ic_dists = [float(x) for x in ic_dists]
  overall = sum(ic_dists)

  ## print intracluster coherence for each cluster and overall
  if print:
    print("Tightest Cluster:\t", ic_dists.index(min(ic_dists)))
    print(f"Overall:\t{overall}")
    prnt = f"Cluster {0}:\t{ic_dists[0]}"
    for x in range(1,k):
        prnt += f"\nCluster {x}:\t{ic_dists[x]}"
    print(prnt + "\n")
  
  ## construct subplots to display each cluster and its elements
  if save or show:
    fig, axs = plt.subplots(1, k, sharex=True, sharey=True) 

    ## set title, size, x-axis for this figure
    fig.suptitle('Run ' + str(idx))
    fig.set_figheight(5)
    fig.set_figwidth(12)
    fig.supylabel("Average Displacement (\u03BCm)")
    fig.supxlabel("Time (\u03BCs)")
    x_axis = np.linspace(5, 80, 76)[:30] # indices of the images to analyze
    labs = []

    ## plotting cluster elements to the corresponding subplot, and color-coding members vs centroids
    for cluster in range(k):
      if cluster == 0:
        # plot each member of this cluster, cornflowerblue
        c_pts = d[labels == cluster] # each point in the corresoponding cluster
        labs.append(labels[labels == cluster])
        for point in c_pts:
            axs[0].plot(x_axis, point, '--', color = 'cornflowerblue')

        # plot this cluster's centroid, red
        cntr = centroids[cluster]
        axs[0].plot(x_axis, cntr, color = 'red')
      
      if cluster == 1:
        c_pts = d[labels == cluster]
        labs.append(labels[labels == cluster])
        for point in c_pts:
            axs[1].plot(x_axis, point, '--', color = 'cornflowerblue')
        
        cntr = centroids[cluster] 
        axs[1].plot(x_axis, cntr, color = 'red')
      
      if cluster == 2:
        c_pts = d[labels == cluster]
        labs.append(labels[labels == cluster])
        for point in c_pts:
            axs[2].plot(x_axis, point, '--', color = 'cornflowerblue')
        
        cntr = centroids[cluster]
        axs[2].plot(x_axis, cntr, color = 'red')
      
      if cluster == 3:
        c_pts = d[labels == cluster]
        labs.append(labels[labels == cluster])
        for point in c_pts:
            axs[3].plot(x_axis, point, '--', color = 'cornflowerblue')
        
        cntr = centroids[cluster]
        axs[3].plot(x_axis, cntr, color = 'red')
        
    ## titling subplots by cluster label
    for i in range(k):
      axs[i].set_title(f"k = {i}")

    ## ensure global y-axis
    plt.ylim(ymin*(10**5), ymax*(10**5))
  

  ## save to the specified filepath, given the dataset name and realization index
  if save:
    plt.savefig("../premade_visuals/clusters/" + title + "/" + "Run " + str(idx) + ".png")

  # show the figure
  if show:
    plt.show()

  return overall


def kmeans_pp_with_fixed_first(d, k, first_index): 
    """
    Runs k-means++ center selection with a user-selected fixed first center.
    Drafting of this function was assisted by Claude Sonnet 4.5 and revised by the programmer.

    Parameters:
        d (np.ndarray):    the data matrix, shape (n, m) — n samples, m features
        k (int):           the number of cluster centers to select
        first_index (int): the ndex in [0, n) of the forced first centroid

    Returns:
        np.ndarray:        selected cluster centers, shape (k, m)
    """   
    ## specify random seed for reproducible clustering
    rng = np.random.default_rng(111)

    ## fix the first center 
    centers_idx = [first_index]
    n = d.shape[0]

    ## select all remaining cluster centers
    for _ in range(1, k):
        centers = d[centers_idx]

        # compute squared euclidean distance and keep the one closest to the center
        dist_sq = np.min(np.sum((d[:, None, :] - centers[None, :, :])**2, axis=2), axis=1)
        
        # sum all minimum squared distances to normalize
        total = np.sum(dist_sq)


        if total == 0: # points are already centers; pick another
            next_center = rng.integers(n)
        else: 
            # otherwise, convert distances to probabilities and sample the next center
            # points farther from existing centers are more likely to be chosen
            probs = dist_sq / total
            next_center = rng.choice(n, p=probs)
        
        # add the new center's idx to the list
        centers_idx.append(int(next_center))
        
    # return the vector form of each cluster's center
    return d[centers_idx]

def all_kmeanspp_initializations(data, k=2):
    """
    Runs kmeans_pp_with_fixed_first for every possible first center index.
    Drafting of this function was assisted by Claude Sonnet 4.5 and revised by the programmer.

    Parameters:
        data (np.ndarray): the dataset, shape (n, m)
        k (int):           the number of cluster centers per initialization

    Returns:
        list[np.ndarray]:  a length-n list of centroid arrays, each shape (k, m) where n = len(selected dataset)
    """
  
    ## grab all clustering realizations and save for later
    n = data.shape[0]
    all_sets = []
    for i in range(n):
        centers = kmeans_pp_with_fixed_first(data, k, first_index=i)
        all_sets.append(centers)
    
    return all_sets

###
# MAIN PROGRAM
###
def main():
    ## collect average data for clustering the time series over the specified designs
    names = ["D17_D1_7p", "D17_D8_2p", "D17_D2_0p", "D17_D1_np"]
    all_L = np.array(aa.average_analysis(names))

    ## grab all clustering data for each iteration
    clusters = all_kmeanspp_initializations(all_L, 4)
    
    ## run all realizations of the clustering scheme, generating plots and terminal output
    idx = 0
    for i in clusters:
      idx += 1
      print("ITERATION ", idx)
      clustering_L(pd.DataFrame(all_L), all_L, i, 4, idx, title="Four Designs")

if __name__ == "__main__":
    main()
