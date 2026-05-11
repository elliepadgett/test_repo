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

from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import average_analysis as aa
import unique_runs as ur
from pathlib import Path
import pickle
from itertools import product, permutations
from collections import defaultdict

def collect_files_by_design():
  files = [f for f in Path("reshaped_data2").iterdir()]
  bydes = {'7p': [], '2p': [], '0p': [], 'np': []}
  for f in files:
    if "7p" in f.name:
      bydes["7p"].append("reshaped_data2/" + f.name)
    elif "2p" in f.name:
      bydes["2p"].append("reshaped_data2/" + f.name)
    elif "0p" in f.name:
      bydes["0p"].append("reshaped_data2/" + f.name)
    elif "np" in f.name:
      bydes["np"].append("reshaped_data2/" + f.name)
  return bydes

def get_groups(files_by_design):
    """
    files_by_design: {'design_A': [f1, f2, f3], 'design_B': [...], ...}
    returns: list of 4-tuples, one file per design
    """
    return [dict(zip(files_by_design.keys(), combo)) for combo in product(*files_by_design.values())]

def all_initializations():
  files = collect_files_by_design()
  groups = get_groups(files)
  results = {}
  # print(groups[0])
  idx = 0
  for group in groups:
    idx += 1
    # print(f"GROUP {idx}")
    # data = np.array([])
    ## pool all datasets
    # for title in group.values():
    #   ## grab this dataset and load its contents for plotting
    #   arrays = [np.load(title)[:30] for title in group.values()]
    #   data = np.concatenate(arrays, axis=0)

    data = [np.load(f) for f in group.values()]
    # print(data.shape)

    ## perform averaging analysis to collect vector data for clustering
    # title = f"four_designs_k4_g{idx}"
    d = np.array(aa.averageAnalysis(data, list(group.values()), f"4 designs g{idx}"))
    clusters = ur.all_kmeanspp_initializations(d, [], 1, 3)
    max = 0
    index = 0
    first_index = 0
    for i in clusters:
      index += 1
      overall = ur.clustering_L(pd.DataFrame(d), np.array(d), i, 3, index)
      if overall > max:
        max = overall
        first_index = index
    print(f"Iter {first_index} out of {index}: {max}")
    # break

    rng = np.random.default_rng(seed=15)
    k = 4
    ## fix the first center 
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
            # otherwise, convert distances to probabilities and sample the next center
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
    print(kmeans.labels_)

    # use the model to predict the fit for other datasets based on their avg analysis
    results[idx] = {}
    for title in Path("reshaped_data2").iterdir():
      target_data = np.load("reshaped_data2/" + title.name)[:30]
      # repeat target 4 times to match expected input shape, or redesign for single-file prediction
      avgs = pd.DataFrame(np.array(aa.averageAnalysis([target_data]*4, [], title.name[:-4])))
      predictions = kmeans.predict(avgs)
      results[idx][title.name[:-4]] = predictions

  with open("all_results.pkl", "wb") as f:
    pickle.dump(results, f)

def check_results(results):
  # after gathering all predictions
  files = [f for f in Path("reshaped_data2").iterdir()]
  for file in files:
    if "7p" in file.name:
      print(file.name[:-4])
      # break
      for group_idx, preds in results.items():
        # print(f"Group {group_idx}: {preds[file.name[:-4]]}")
        stuff = preds[file.name[:-4]]

    # # Which cluster a file belongs to in group 1
    # results[1]["some_filename"]  # e.g. array([2, 0, 1, ...])

    # Majority cluster per file per group
    # majority = {
    #     gidx: {fname: np.bincount(preds).argmax() for fname, preds in fpreds.items()}
    #     for gidx, fpreds in results.items()
    # }
    # majority[1]["some_filename"]  # single int — most common cluster label

def get_design(fname):
    for d in ["7p", "2p", "0p", "np"]:
        if d in fname:
            return d
    return None

def majority_label(predictions):
    return int(np.bincount(np.array(predictions, dtype=int)).argmax())

def best_label_mapping(labels_a, labels_b, k=4):
    best_acc, best_perm = 0, None
    for perm in permutations(range(k)):
        mapped = np.array([perm[l] for l in labels_b])
        acc = np.mean(mapped == labels_a)
        if acc > best_acc:
            best_acc, best_perm = acc, perm
    return best_acc, best_perm

def align_all_to_reference(per_experiment_majority, k=4):
    """Align all experiments' labels to experiment 1's label space."""
    exps = list(per_experiment_majority.keys())
    fnames = list(per_experiment_majority[exps[0]].keys())
    ref = exps[0]
    ref_labels = np.array([per_experiment_majority[ref][f] for f in fnames])

    aligned = {ref: per_experiment_majority[ref]}
    for gidx in exps[1:]:
        target_labels = np.array([per_experiment_majority[gidx][f] for f in fnames])
        _, perm = best_label_mapping(ref_labels, target_labels, k)
        aligned[gidx] = {f: perm[per_experiment_majority[gidx][f]] for f in fnames}
    return aligned

def check_cluster_consistency(results, k=4):
    # Step 1: majority label per file per experiment
    per_experiment_majority = {
        gidx: {fname: majority_label(arr) for fname, arr in preds.items()}
        for gidx, preds in results.items()
    }

    # Step 2: align all experiments to reference (exp 1)
    aligned = align_all_to_reference(per_experiment_majority, k)

    # Step 3: compute agreement rates
    fnames = list(next(iter(aligned.values())).keys())
    same_design_agreement = defaultdict(list)
    cross_design_agreement = defaultdict(list)

    for gidx, majority in aligned.items():
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
        print(f"  {d1} vs {d2}: {np.mean(agreements):.3f}  (n={len(agreements)})")

    return aligned, same_design_agreement, cross_design_agreement

###
# MAIN PROGRAM
###
def main():
  # create all 81 models and save their cluster labels 
  # (this part takes a while; comment out when done so it doesn't run every time)
  # all_initializations()

  # load the results dictionary
  with open("all_results.pkl", "rb") as f:
      loaded = pickle.load(f)

  # main analysis
  aligned, same, cross = check_cluster_consistency(loaded)

if __name__ == "__main__":
   main()
