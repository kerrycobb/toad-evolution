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

if test -d $outDir
  echo "Directory already exists"
  exit 1
else
  mkdir $outDir
end

# Filter sites with non-biallelic sites
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
  --out $outPrefix

# Generate bgc input files
vcf2bgc.py $filteredVCF $amerSamples $outDir/data-americanus.bgc 
vcf2bgc.py $filteredVCF $terrSamples $outDir/data-terrestris.bgc 
vcf2bgc.py $filteredVCF $admxSamples $outDir/data-admixed.bgc --parent_pop=False 