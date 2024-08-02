#!/usr/bin/env python

import allel
import fire
import pandas as pd

def run(vcf_path, sample_data):
    vcf = allel.read_vcf(vcf_path)
    samples = vcf["samples"]
    df = pd.read_csv(sample_data)
    df = df[df["sample_id2"].isin(samples)] 
    for species, data in df.groupby("reassign"): 
        data.to_csv("filtered-vcf-{}-samples.txt".format(species), columns=["sample_id2"], header=False, index=False)

if __name__ == "__main__":
    fire.Fire(run)


