#!/usr/bin/env python

## Covnert vcf to structure format

import fire
import pandas as pd
import allel

def run(vcf_path, out_path):
    vcf = allel.read_vcf(vcf_path, fills=dict(GT=-9))
    samples = vcf["samples"]
    arr = allel.GenotypeArray(vcf["calldata/GT"])
    nSamples = len(samples)
    nLoci = arr.shape[0]
    with open(out_path, "w") as fh:
        for i in range(nSamples):
            for j in [0, 1]:
                fh.write(samples[i] + " ")
                for k in range(nLoci):
                    fh.write(arr[k, i, j].astype(str))    
                    if k < nLoci: 
                        fh.write(" ")
                if j == 0:
                    fh.write("\n")
            if i < len(samples):
                fh.write("\n")

    print("\n**********************************\n") 
    print("Structure file written to {}".format(out_path))
    print("\n**********************************\n") 

if __name__ == "__main__":
    fire.Fire(run)