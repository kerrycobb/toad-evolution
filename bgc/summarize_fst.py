#!/usr/bin/env python

## Get mean fst for each locus and output to dataframe with locus index
## in order to associate bgc output with loci

import fire
import allel
import pandas as pd

def run(vcf_path, input_path, out_path):
    vcf = allel.read_vcf(vcf_path)
    df = pd.DataFrame.from_dict(dict(
        CHROM=vcf["variants/CHROM"],
        POS=vcf["variants/POS"])).astype(int)
    fst_df = pd.read_csv(input_path, sep="\t")
    duplicates = fst_df.duplicated(subset='col1', keep=False)
    if duplicates.any():
        quit("Found duplicated loci in Fst")
    merged = df.merge(fst_df, on="CHROM")
    merged.to_csv(out_path, index=False)
    assert len(df) == len(merged)

if __name__ == "__main__":
    fire.Fire(run)
