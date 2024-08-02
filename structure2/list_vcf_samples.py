#!/usr/bin/env python

import fire
import allel
import pandas as pd

def run(vcf_path, out_path):
    vcf = allel.read_vcf(vcf_path)
    samples_df = pd.DataFrame({"samples": vcf["samples"]})
    samples_df.to_csv(out_path, index=False, header=False) 

if __name__ == "__main__":
    fire.Fire(run)