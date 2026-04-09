"""
Name: uniqueRuns.py
Date: Nov 2025
Author: Ellie Padgett

Performs k x len(L-range) many unique k++ initializations for running K-means clustering on the specified dataset.
The supporting functions kmeans_pp_with_fixed_first() and all_kmeanspp_initializations() were originally drafted with
support from Claude Sonnet 4.5 and tailored by the programmer to better fit the context of the problem.

Exp 1: choose an "ideal" window size, pool all 12 datasets and cluster k=4
Exp 2: after training on the sample 4 pooled, see how others of the same designs are placed into these clusters

!! update figures in slides to use appropriate axes and labels!
- avg analysis (old and new) ***
- overlaid square (old) ***
- timeline probing samples (new)
- clustering (new)


"""
###
# IMPORTS
###

## for silencing warnings about cpu core use; just using what we have available!
# may need to fix in command prompt if this doesn't work on your device, or ignore the warning for now (defaults to logical cores, 
# which is fine here, it just looks alarming)
import os
os.environ["LOKY_MAX_CPU_COUNT"] = str(os.cpu_count())

# computational libraries
import numpy as np
import averagingAnalysis
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd

###
# GLOBALS
###

# y-axes for  newer D17 datasets
ymin = -13.680035515970473e-01
ymax = 3.3261941377613874e-01


def clustering_L(data, d, centroids, k, idx, title):
    """
    Clustering for each dataset, cluster over L = 60:10:80 for specified dataset option and number of clusters
    
    Parameters:
      data (pd.DataFrame): the vectors to cluster (represent the y-axes computed in average analysis step)
      d (np.array): identical data, just in a different structure to help with compartmentalizing labels as I programmed --> plan to automate
      centroids (list[np.ndarray]): a length-n list of centroid arrays, each shape (k, m) where n = len(selected dataset)
      k (int): the specified number of clusters
      idx (int): the number of the current iteration/realization of the clustering scheme; used for labeling in plots and terminal output
      title (str): the name of the dataset/pooled dataset being clustered in this realization; used for labeling saved figures

    Returns:
      None

    Output:
      - Generates a 1xk subplot figure of all clusters for this iteration, displaying centroid and cluster elements
      - Terminal output (or redirected to a file --> plan to automate) includes:
        - cluster labels corresponding to each cluster element as a list; this information is used later to determine cluster membership by design
        - an indicator of the tightest cluster (determined by lowest intracluster coherence)
        - the intracluster coherence of each cluster, corresponding to its cluster label
        - this run's overall coherence (sum of intracluster coherences) for comparing cluster "tightness" across multiple runs
    """
    
    ## using scikit-learn's kmeans package
    kmeans = KMeans(n_clusters=k, init=centroids, n_init=1)
    kmeans.fit(data)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    ## prints the labels mapping each vector to the cluster it landed in
    print("Labels:")
    print(labels)

    ### CLUSTER COHERENCE MEASURES
    # Intra-cluster distance: distances between points in the same cluster
    ic_dists = []
    for i in range(k):
        c_pts = d[labels == i]
        cntr = centroids[i]
        # sum of squared euclidean distances
        ssd = np.sum((c_pts - cntr)**2)
        ic_dists.append(ssd)

    ic_dists = [float(x) for x in ic_dists]
    overall = sum(ic_dists) * 10**13

    ## print intracluster coherence for each cluster and overall
    # comment out any unused cluster labels --> plan to automate
    print("Tightest Cluster:\t", ic_dists.index(min(ic_dists)))
    print(f"Cluster 0:\t{ic_dists[0]}" +
        f"\nCluster 1:\t{ic_dists[1]}" +
        f"\nCluster 2:\t{ic_dists[2]}" +
        f"\nCluster 3:\t{ic_dists[3]}" +
        f"\nOverall:\t{overall : .5f}\n")
    
    ## construct subplots to display each cluster and its elements
    # need to comment out to avoid overpopulating figures when not using plots --> plan to automate
    if k == 2:
        fig, (ax1, ax2) = plt.subplots(1, k, sharex=True, sharey=True) 
    elif k == 3:   
        fig, (ax1, ax2, ax3) = plt.subplots(1, k, sharex=True, sharey=True)
    else:
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, k, sharex=True, sharey=True)
    
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
            ## plot each member of this cluster, cornflowerblue
            c_pts = d[labels == cluster] # each point in the corresoponding cluster
            labs.append(labels[labels == cluster])
            for point in c_pts:
                ax1.plot(x_axis, point, '--', color = 'cornflowerblue')
            
            ## plot this cluster's centroid, red
            cntr = centroids[cluster]
            ax1.plot(x_axis, cntr, color = 'red')
        if cluster == 1:
            c_pts = d[labels == cluster]
            labs.append(labels[labels == cluster])
            for point in c_pts:
                ax2.plot(x_axis, point, '--', color = 'cornflowerblue')
            
            cntr = centroids[cluster] 
            ax2.plot(x_axis, cntr, color = 'red')
        if cluster == 2:
            c_pts = d[labels == cluster]
            labs.append(labels[labels == cluster])
            for point in c_pts:
                ax3.plot(x_axis, point, '--', color = 'cornflowerblue')
            
            cntr = centroids[cluster]
            ax3.plot(x_axis, cntr, color = 'red')
        if cluster == 3:
            c_pts = d[labels == cluster]
            labs.append(labels[labels == cluster])
            for point in c_pts:
                ax4.plot(x_axis, point, '--', color = 'cornflowerblue')
            
            cntr = centroids[cluster]
            ax4.plot(x_axis, cntr, color = 'red')
        
    ## titling subplots by cluster label (comment out as needed) --> plan to automate
    ax1.set_title("k = 0")
    ax2.set_title("k = 1")
    ax3.set_title("k = 2")
    ax4.set_title("k = 3")

    ## ensure global y-axis
    plt.ylim(ymin, ymax)
    

    ## save to the specified filepath, given the dataset name and realization index (comment out as needed) --> plan to automate
    # plt.savefig("visualizations/new_data_clustering/" + title + "/" + "Run " + str(idx) + ".png")

    # show the figure (comment out as needed) --> plan to automate
    plt.show()


def kmeans_pp_with_fixed_first(d, k, first_index): 
    """
    Runs k-means++ center selection with a user-selected fixed first center.
    Drafting of this function was assisted by Claude Sonnet 4.5 and revised by the programmer.

    Parameters:
        d (np.ndarray): the data matrix, shape (n, m) — n samples, m features
        k (int): the number of cluster centers to select
        first_index (int): the ndex in [0, n) of the forced first centroid

    Returns:
        np.ndarray: selected cluster centers, shape (k, m)
    """   
    ## specify random seed for reproducible clustering; defaulted to unpredictable seed 
    # while developing and testing the program --> plan to adjust
    rng = np.random.default_rng(None)

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

def all_kmeanspp_initializations(dataL1, dataL2=[], o=1, k=2):
    """
    Runs kmeans_pp_with_fixed_first for every possible first center index.
    Drafting of this function was assisted by Claude Sonnet 4.5 and revised by the programmer.

    Parameters:
        dataL1 (list): the first dataset, shape (n1, m)
        dataL2 (list): the second dataset, shape (n2, m)
        o (int): the option for which dataset(s) to run:
            1 - use dataL1 only
            2 - use dataL2 only
            else - concatenate both and treat as a whole, pooled dataset
        k (int): Number of cluster centers per initialization

    Returns:
        list[np.ndarray]: a length-n list of centroid arrays, each shape (k, m) where n = len(selected dataset)
    """
    ## select and convert the dataset to work with
    if o == 1:
        d = np.array(dataL1)
    elif o == 2:
        d = np.array(dataL2)
    else:
        d = np.concatenate([dataL1, dataL2], axis=0)

    ## grab all clustering realizations and save for later
    n = d.shape[0]
    all_sets = []
    for i in range(n):
        centers = kmeans_pp_with_fixed_first(d, k, first_index=i)
        all_sets.append(centers)
    
    return all_sets


def main():
    ## change these filepaths to work with other reshaped datasets
    # current version: for working with pooled data from all four D17 designs --> plan to automate
    names = ["D17_D8_2p", "D17_D2_0p", "D17_D1np"]
    data = np.load("reshaped_data/D17_D1_7p.npy")[:30] # only want first 30 images
    
    ## pool all datasets
    for title in names:
      ## grab this dataset and load its contents for plotting
      dpl = np.load('reshaped_data/'+ title + ".npy")[:30]
      data = np.append(data, dpl, axis=0)
    
    ## perform averaging analysis to collect vector data for clustering
    title = "four_designs_k2"
    all_L = averagingAnalysis.averageAnalysis(data, "4 designs")

    ## grab all clustering data for each iteration
    # already pooled dataset, so second param is a placeholder --> plan to automate
    clusters = all_kmeanspp_initializations(all_L, [], 1, 4)
    
    ## run all realizations of the clustering scheme, generating plots and terminal output
    idx = 0
    for i in clusters:
        idx += 1
        print("ITERATION ", idx)
        clustering_L(pd.DataFrame(all_L), np.array(all_L), i, 4, idx, title)

if __name__ == "__main__":
    main()

