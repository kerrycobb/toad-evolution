#!/usr/bin/env python


import fire
import allel
import pandas as pd


def run(vcf_path, out_path):
    print("Outputting locus map file to {}".format(out_path))
    vcf = allel.read_vcf(vcf_path)
    df = pd.DataFrame(vcf["samples"])
    df.to_csv(out_path)

if __name__ == "__main__":
    fire.Fire(run)


