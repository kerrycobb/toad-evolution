#!/usr/bin/env fish

module load vcftools

set vcf $argv[1]
set name $argv[2]
set amerSamples $argv[3]
set terrSamples $argv[4]
set admxSamples $argv[5]

set outDir out-$name
set outPrefix out-$name/$name
set filteredPrefix $outPrefix.filtered
set filteredVCF $filteredPrefix.recode.vcf
set subsampledSites $outDir/subsampled.txt
set subsampledPrefix $outPrefix.subsampled
set subsampledVCF $subsampledPrefix.recode.vcf

if test -d $outDir
  echo "Directory already exists"
  exit 1
else
  mkdir $outDir
end

# Filter sites with non-biallelic sites and sites with MAC < 3
vcftools \
  --vcf $vcf \
  --max-alleles 2 \
  --recode \
  --recode-INFO-all \
  --out $filteredPrefix

# Compute locus fst
vcftools \
  --vcf $filteredVCF \
  --weir-fst-pop $amerSamples \
  --weir-fst-pop $terrSamples \
  --out $filteredPrefix

# # Produce list of samples from VCF, don't think I need this 
# ./list_vcf_samples.py $filteredVCF $filteredPrefix.samples.txt

# Get list of random sites to subsample
./subsample_vcf_sites.py $filteredVCF $subsampledSites 

# Generate subsampled vcf
vcftools \
  --vcf $filteredVCF \
  --positions $subsampledSites \
  --recode \
  --recode-INFO-all \
  --out $subsampledPrefix

# Get mean fst for the locus of each subsampled site
./summarize_fst.py $subsampledVCF $filteredPrefix.weir.fst $outPrefix-mean-fst.csv 

# Generate bgc input files
vcf2bgc.py $subsampledVCF $amerSamples $outDir/data-americanus.bgc 
vcf2bgc.py $subsampledVCF $terrSamples $outDir/data-terrestris.bgc 
vcf2bgc.py $subsampledVCF $admxSamples $outDir/data-admixed.bgc --parent_pop=False 