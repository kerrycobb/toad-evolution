#!/usr/bin/env python

import fire
import pandas as pd

def gen(qmatPath, name, cuttof, cluster1, cluster2):
    ## cuttof: miximum allowable alternative ancestry to be considered pure
    ## cluster1: cluster 1 species
    ## cluster2: cluster 2 species
    upper = 1.0 - cuttof
    qmat = pd.read_csv(qmatPath)
    c1 = qmat[qmat["Cluster1"].between(0, cuttof)] 
    c2 = qmat[qmat["Cluster1"].between(upper, 1)]
    adm = qmat[qmat["Cluster1"].between(cuttof, upper)]
    c1["Unnamed: 0"].to_csv(f"assign-{name}-{cluster1}.txt", header=None, index=None)
    c2["Unnamed: 0"].to_csv(f"assign-{name}-{cluster2}.txt", header=None, index=None)
    adm["Unnamed: 0"].to_csv(f"assign-{name}-admixed.txt", header=None, index=None)
    
if __name__ == "__main__":
    fire.Fire(gen)