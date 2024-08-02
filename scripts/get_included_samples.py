#!/usr/bin/env python

import fire
import pandas as pd

def get(path, output):
    ids = []
    with open(path, "r") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("#"):
                if len(line) > 0:
                    ids.append(line)
    df = pd.read_csv("../data/sample-data.csv")  
    df["species"] = df["species"].replace("fowleri / woodhousii intergrade", "fowleri-woodhousii")
    df["sample_id"] = df["sample_id"] + "_" + df["species"]
    df = df.drop_duplicates("sample_id")
    filtered = df[~df["sample_id"].isin(ids)]
    filtered.to_csv(output, index=False, header=False, columns=["sample_id2"])

if __name__ == "__main__":
    fire.Fire(get)