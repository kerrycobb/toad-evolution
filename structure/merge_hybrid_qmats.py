import pandas as pd
from functools import reduce

dfs =[ 
    pd.read_csv("qmats/hybrid-zone-minSamples1.0-mac3-popmap2-K-2.csv"),
    pd.read_csv("qmats/hybrid-zone-minSamples1.0-mac3-popmap3-K-2.csv"),
    pd.read_csv("qmats/hybrid-zone-minSamples95-mac3-popmap2-K-2.csv"),
    pd.read_csv("qmats/hybrid-zone-minSamples95-mac3-popmap3-K-2.csv")]

for i in range(len(dfs)):
    new_col_name = {}
    for j in range(1, len(dfs[i].columns)):
        col = dfs[i].columns[j] 
        new_col_name[col] = f"{col}_{i+1}"
    dfs[i] = dfs[i].rename(columns=new_col_name)

merged = reduce(lambda left, right: 
        pd.merge(left, right, left_on=left.columns[0], right_on=right.columns[0], 
        how="outer"), dfs)

merged.to_csv("merged-hybrid-qmats.csv")