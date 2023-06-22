#!/usr/bin/env python

import fire
import pandas as pd
import os

def make_latex(prefix, group, df):
    df.reset_index(inplace=True)
    df = df.sort_values("Sample ID")
    df["Latitude"] = df["Latitude"].apply(lambda x: '{0:.5f}'.format(x))
    df["Longitude"] = df["Longitude"].apply(lambda x: '{0:.5f}'.format(x))
    last_ix = len(df) - 1
    with open(f"{prefix}-{group}.tex", "w") as fh:
        for ix, row in df.iterrows():
            if row["Passed Filtering"]:
                passed_filter = "X"
            else:
                passed_filter = " "
            fh.write("{} & \\textit{{{}}} & {} & {} & {}".format(
                row["Sample ID"], 
                row["Species"], 
                row["Latitude"], 
                row["Longitude"],
                passed_filter))
            if ix < last_ix:
                fh.write(" \\\\ \n")

# def main(input, output):
#     df = pd.read_csv(input)
#     df.drop_duplicates(subset="sample_id", inplace=True)
#     df["species"] = df["genus"] + " " + df["species"]
#     df["prefix"] = df["id"].str.split(" ", n=1, expand=True)[0]
#     df = df.rename(columns={
#         "id": "Sample ID",
#         "species": "Species", 
#         "latitude": "Latitude",
#         "longitude": "Longitude"})
#     kac_df = df[df["prefix"] == "KAC"]
#     make_latex(output, "kac", kac_df)
#     other_df = df[df["prefix"] != "KAC"]
#     make_latex(output, "other", other_df)

def main(popmap, subpopmap, outPrefix):
    pm = pd.read_csv(popmap, header=None, sep="\t")
    spm = pd.read_csv(subpopmap, header=None, sep="\t")
    dt = pd.read_csv("../sample-data.csv")
    merged = pm.merge(dt, left_on=0, right_on="sample_id", how="left")
    merged = merged.drop_duplicates("id")
    merged["prefix"] = merged["id"].str.split(" ", n=1, expand=True)[0]
    merged["Passed Filtering"] = merged[0].isin(spm[0]).tolist()
    merged = merged.rename(columns={
        "id": "Sample ID",
        "species": "Species", 
        "latitude": "Latitude",
        "longitude": "Longitude"})
    kac_df = merged[merged["prefix"] == "KAC"] 
    other_df = merged[merged["prefix"] != "KAC"] 
    print(f"Total samples: {len(merged)}")
    print("Collected: {}".format(len(kac_df)))
    print("Loaned: {}".format(len(other_df)))
    print("Total americanus: {}".format(len(merged.loc[merged["Species"] == "americanus"])))
    print("Total terrestris: {}".format(len(merged.loc[merged["Species"] == "terrestris"])))
    print("Unfiltered total: {}".format(len(merged[merged["Passed Filtering"]])))
    print("Unfiltered americanus: {}".format(len(merged[merged["Passed Filtering"] & (merged["Species"] == "americanus")])))
    print("Unfiltered terrestris: {}".format(len(merged[merged["Passed Filtering"] & (merged["Species"] == "terrestris")])))

    make_latex(outPrefix, "kac", kac_df)
    make_latex(outPrefix, "other", other_df)

if __name__ == '__main__':
    fire.Fire(main)