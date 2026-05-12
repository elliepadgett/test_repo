"""
Name: cross_validation.py
Date: Apr 2025
Author: Ellie Padgett

Determines the consistency of the clustering scheme by cross-referencing all possible initializations from
all possible combinations of training sets. Each training set is composed of 4 datasets, one from
each design (7p, 2p, 0p, and np). After training a kmeans model using a training set, all other datasets
in the folder (12 total) are fed into it and placed into their predicted clusters. Finally, the program 
checks how consistent the different models are in determining which designs dominate which clusters.

"""

###
# IMPORTS
###
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import average_analysis as aa
import unique_runs as ur
from pathlib import Path
import pickle
from itertools import product, permutations
from collections import defaultdict

###
# FUNCTIONS
###
def collect_files_by_design(filepath):
  """
  Collects all files by path and organizes them into a dictionary, keyed by design

  Parameters:
    filepath (string):                  the name of the folder containing datasets to collect

  Returns:
    dict[design (string):list[string]]: a dictionary keyed by design (np-7p), where the values are lists of
                                        the filenames associated with that design
  """
  files = [f for f in Path(filepath).iterdir()]
  bydes = {'7p': [], '2p': [], '0p': [], 'np': []}
  for f in files:
    if "7p" in f.name:
      bydes["7p"].append(f"{filepath}/" + f.name)
    elif "2p" in f.name:
      bydes["2p"].append(f"{filepath}/" + f.name)
    elif "0p" in f.name:
      bydes["0p"].append(f"{filepath}/" + f.name)
    elif "np" in f.name:
      bydes["np"].append(f"{filepath}/" + f.name)
  return bydes

def get_groups(bydes):
  """
  Compiles a list of dictionaries, where each dictionary in the list represents a unique combination of
  four datasets, with one member from each design (81 dictionaries total)

  Parameters:
    bydes (dict[design (string):list[string]]): a dictionary keyed by design (np-7p), where the values are lists of
                                                the filenames associated with that design
  Returns:
    list[dict[design (string):string]]:         a list containing one dictionary per combination of 4 datasets
  """
  return [dict(zip(bydes.keys(), combo)) for combo in product(*bydes.values())]

def all_initializations(filepath, k=4):
  """
  Compiles a nested dictionary of all cluster placements/predictions for all 12 datasets,
  for all 81 combinations of training sets. Can take a while to run!

  Parameters:
    filepath (string): the name of the folder containing the datasets
    k (int):           the number of clusters to use (default k=4)
  
  Returns:
    None

  Output:
    Saves the nested dictionary with the following structure:
      dict[combination (int):dict[dataset name (string):cluster labels (np.ndarray)]]
    as a .pkl file for later loading and use.
  """
  files = collect_files_by_design(filepath)
  groups = get_groups(files)
  results = {}

  idx = 0
  for group in groups:
    idx += 1

    ## perform averaging analysis to collect vector data for clustering
    names = [x[17:-4] for x in group.values()]
    d = np.array(aa.average_analysis(names, f"4 designs g{idx}"))
    clusters = ur.all_kmeanspp_initializations(d, k)

    ## finding clustering realization with lowest overall coherence
    min = 100
    index = 0
    first_index = 0
    for i in clusters:
      index += 1
      overall = ur.clustering_L(pd.DataFrame(d), np.array(d), i, k, index, title="Four Designs")
      if overall < min:
        min = overall
        first_index = index
    print(f"Minimum overall coherence at index {first_index}: {min}")

    rng = np.random.default_rng(111)
    ## fix the first center based on the 
    centers_idx = [first_index-1]
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
            # o.w., convert distances to probabilities and sample the next center
            # points farther from existing centers are more likely to be chosen
            probs = dist_sq / total
            next_center = rng.choice(n, p=probs)
        
        # add the new center's idx to the list
        centers_idx.append(int(next_center))
        
    # return the vector form of each cluster's center
    centers = d[centers_idx]

    # use these centroids to train/fit the kmeans model
    df = pd.DataFrame(d)
    kmeans = KMeans(n_clusters=k, init=centers, n_init=1)
    kmeans.fit(df)
    # print(kmeans.labels_)

    # use the model to predict the fit for other datasets based on their avg analysis
    results[idx] = {}
    for title in Path("../reshaped_data").iterdir():
      # repeat target 4 times to match expected input shape, or redesign for single-file prediction
      avgs = pd.DataFrame(np.array(aa.average_analysis([title.name[:-4]], title.name[:-4])))
      predictions = kmeans.predict(avgs)
      results[idx][title.name[:-4]] = predictions

  with open("../results/all_results.pkl", "wb") as f:
    pickle.dump(results, f)

def get_design(fname):
  """
  Extracts the design name in the given filename for design identification

  Parameters:
    fname (string): the name of the file

  Returns:
    string:         an indicator of the design, or None if no design type is found
  """
  for d in ["7p", "2p", "0p", "np"]:
    if d in fname:
      return d
  return None

def majority_label(predictions):
    """
    Identifies the most frequently occurring cluster label in an array of predictions

    Parameters:
      predictions (np.ndarray): an array of cluster predictions by label

    Returns:
      int:                      the most common cluster label
    """
    return int(np.bincount(np.array(predictions, dtype=int)).argmax())

def best_label_mapping(labels_a, labels_b, k=4):
    """
    Finds the permutation of labels_b that best agrees with labels_a

    Parameters:
      labels_a (np.ndarray): reference label array
      labels_b (np.ndarray): target label array that needs to be remapped
      k (int):               the number of clusters to use (default k=4)

    Returns:
      tuple[ints]:           the best-agreeing label permutation
    """
    best_acc, best_perm = 0, None
    for perm in permutations(range(k)):
        mapped = np.array([perm[l] for l in labels_b])
        acc = np.mean(mapped == labels_a)
        if acc > best_acc:
            best_acc, best_perm = acc, perm
    return best_perm

def align_all_to_reference(per_exp_maj, k=4):
    """
    Remaps the majority labels of each experiment to a shared label space, by aligning
    all subsequent experiments to experiment 1 via the best label permutation. This is
    meant to correct arbitrary cluster labeling assignments across experiments.
    
    Parameters:
      per_exp_maj (dict[int : dict[string : int]]): nested dictionary mapping experiment indices
                                                    to dictionaries of filename : majority label
      
      k (int):                                      number of clusters

    Returns:
      dict[int : dict[string : int]]:               nested dictionary with the same structure as
                                                    the parameter dictionary, but with the labels
                                                    remapped to experiment 1's label space
    """
    exps = list(per_exp_maj.keys())
    fnames = list(per_exp_maj[exps[0]].keys())
    ref = exps[0]
    ref_labels = np.array([per_exp_maj[ref][f] for f in fnames])

    aligned = {ref: per_exp_maj[ref]}
    for gidx in exps[1:]:
        target_labels = np.array([per_exp_maj[gidx][f] for f in fnames])
        perm = best_label_mapping(ref_labels, target_labels, k)
        aligned[gidx] = {f: perm[per_exp_maj[gidx][f]] for f in fnames}
    return aligned

def check_cluster_consistency(results, k=4):
    """
    Measures how consistently each dataset is dominantly mapped to the same cluster across
    all 81 experiments. Also determines whether same-design datasets cluster together.

    Parameters:
      results (dict[int : dict[string : np.ndarray]]): nested dictionary mapping experiment index to
                                                       dictionary of filename : cluster label array
      
      k (int):                                         number of clusters (default k=4)

    Returns:
      tuple: (aligned, same_des_agrmnt, cross_des_agrmnt), where
        aligned (dict[int : dict[string : int]]):    majority labels after alignment, by experiment
        same_des_agrmnt (dict[string : list[bool]]): pairwise agreement booleans for same-design pairs
        cross_des_agrmnt (dict[tuple : list[bool]]): pairwise agreement booleans for cross-design pairs (as tuples)
    """
    # majority label per file per experiment
    per_exp_maj = {
        gidx: {fname: majority_label(arr) for fname, arr in preds.items()}
        for gidx, preds in results.items()
    }

    # align all experiments to the label space of the first experiment (standardizing)
    aligned = align_all_to_reference(per_exp_maj, k)

    # compute agreement rates
    fnames = list(next(iter(aligned.values())).keys())
    same_design_agreement = defaultdict(list)
    cross_design_agreement = defaultdict(list)

    for _, majority in aligned.items():
        for i, fa in enumerate(fnames):
            for fb in fnames[i+1:]:
                da, db = get_design(fa), get_design(fb)
                agree = majority[fa] == majority[fb]
                if da == db:
                    same_design_agreement[da].append(agree)
                else:
                    cross_design_agreement[(da, db)].append(agree)

    print("Same-design label agreement (higher = better)")
    print("="*45)
    for design, agreements in sorted(same_design_agreement.items()):
        print(f"  {design}: {np.mean(agreements):.3f}  (n={len(agreements)})")

    print("\nCross-design label agreement (lower = better)")
    print("="*45)
    for (d1, d2), agreements in sorted(cross_design_agreement.items()):
        print(f"  {d1} vs {d2}: {np.mean(agreements):.3f}")

    return aligned, same_design_agreement, cross_design_agreement

###
# MAIN PROGRAM
###
def main():

  ## create all 81 models and save their cluster labels 
  # (this part takes a while; comment out when done so it doesn't run every time)
  # all_initializations("../reshaped_data")

  # load the results dictionary
  with open("../results/all_results.pkl", "rb") as f:
      loaded = pickle.load(f)
  
  # main analysis
  aligned, same, cross = check_cluster_consistency(loaded)

if __name__ == "__main__":
   main()
