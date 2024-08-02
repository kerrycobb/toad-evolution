#!/usr/bin/env fish

module load vcftools

set vcf_input $argv[1]
set max_missing $argv[2]
set exclude_missing $argv[3] # Samples that have too much missing data after filtering 
set prefix $argv[4]

vcftools \
  --vcf $vcf_input \
  --remove-indels \
  --mac 3 \
  --max-alleles 2 \
  --max-missing $max_missing \
  --remove ../exclude-non-americanus-group.txt \
  --remove ../exclude-fowleri-woodhousii.txt \
  --remove ../exclude-outside-of-area.txt \
  --remove $exclude_missing \
  --recode \
  --recode-INFO-all \
  --out $prefix 

../list_vcf_samples.py $prefix.recode.vcf $prefix.samples.txt
../subsample_vcf_sites.py $prefix.recode.vcf 

vcftools \
  --vcf $prefix.recode.vcf \
  --positions sampled-vcf-sites.tsv \
  --recode \
  --recode-INFO-all \
  --out $prefix.subsampled

vcftools \
  --vcf $prefix.subsampled.recode.vcf \
  --missing-indv \
  --out $prefix.subsampled

../vcf_to_structure.py $prefix.subsampled.recode.vcf $prefix.str
