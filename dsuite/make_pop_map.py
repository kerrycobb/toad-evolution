#!/usr/bin/env python

import fire
import allel
import pandas as pd


def main(vcf_path, pop_map, outgroup, ignore=None):
    sample_data = pd.read_csv("~/toad-phyl/sample-data-phyl.csv")
    ignore = pd.read_csv(ignore, header=None)[0].to_list()
    vcf = allel.read_vcf(vcf_path)
    samples = vcf["samples"]
    selected = sample_data[sample_data["sample_id"].isin(samples)]
    selected.loc[selected["species"] == outgroup, "species"] = "Outgroup"
    selected.loc[selected["sample_id"].isin(ignore), "species"] = "xxx"
    selected.to_csv(pop_map, columns=["sample_id", "species"], sep="\t", header=None, index=None)

if __name__ == "__main__":
    fire.Fire(main)