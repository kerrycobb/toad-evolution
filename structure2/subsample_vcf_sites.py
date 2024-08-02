#!/usr/bin/env python

## Sample a single site from each RAD locus in VCF file

import fire
import pandas as pd
import allel

def run(vcf_path, seed=1234):
    vcf = allel.read_vcf(vcf_path)
    sites_df = pd.DataFrame({
        "CHR": vcf["variants/CHROM"],
        "POS": vcf["variants/POS"]})
    sampled_sites = sites_df.groupby("CHR").sample(random_state=seed).sort_index()
    sampled_sites.to_csv("sampled-vcf-sites.tsv", sep="\t", index=None, header=False)
    arr = allel.GenotypeArray(vcf["calldata/GT"])
    print("\n******************************\n")
    print("Sampled {} sites from {} original sites".format(len(sampled_sites), arr.n_variants))
    print("Subsampled sites written to sampled-vcf-sites.tsv")
    print("\n******************************\n")

if __name__ == "__main__":
    fire.Fire(run)