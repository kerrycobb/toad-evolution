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

# Compute locus fst
vcftools \
  --vcf $vcf \
  --weir-fst-pop $amerSamples \
  --weir-fst-pop $terrSamples \
  --out $outPrefix

# Get mean fst for the locus of each subsampled site
./summarize_fst.py $vcf $outPrefix.weir.fst $outPrefix-mean-fst.csv 

# Generate bgc input files
vcf2bgc.py $vcf $amerSamples $outDir/data-americanus.bgc 
vcf2bgc.py $vcf $terrSamples $outDir/data-terrestris.bgc 
vcf2bgc.py $vcf $admxSamples $outDir/data-admixed.bgc --parent_pop=False 