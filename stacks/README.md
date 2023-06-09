# Demux samples
```bash
./demultiplex-samples.fish
sbatch --job-name merge --output demux/%x-%j.out ./merge.fish
```

# Alignment
140 bp length reads
Percent sequence similarity
85%: M=21 
90%: M=14
95%: M=7

./run-denovo-map.sh popmap=$1 outdir=$2 M=$3 gaps=$5

## Bufonidae
```bash
./run-ustacks.fish ../popmap-all.txt out-all-M21-g7 21 7 
```

Modify config with popmap-all-subset.txt
```bash
**./run-cstacks.fish out-all-M21-g7
```

Change popmap back to original
```bash
./run-sstacks.fish out-all-M21-g7
./run-gstacks.fish out-all-M21-g7
./run-populations.fish out-all-M21-g7 ../popmap-all.txt all --vcf --phylip-var-all
```

## Americanus Group
```bash
./run-ustacks.fish ../popmap-americanus-group.txt out-americanus-group-M14-g7 14 7 
./run-cstacks.fish out-americanus-group-M14-g7
./run-sstacks.fish out-americanus-group-M14-g7
./run-gstacks.fish out-americanus-group-M14-g7
./run-populations.fish out-americanus-group-M14-g7 ../popmap-americanus-group.txt all --vcf --phylip-var-all
**Done
```

## Americanus
```bash
./run-ustacks.fish ../popmap-americanus.txt out-americanus-M7-g7 7 7 
./run-cstacks.fish out-americanus-M7-g7
./run-sstacks.fish out-americanus-M7-g7
./run-gstacks.fish out-americanus-M7-g7
./run-populations.fish out-americanus-M7-g7 ../popmap-americanus.txt all --vcf
**Done
```

## Fowleri
```bash
./run-ustacks.fish ../popmap-fowleri.txt out-fowleri-M7-g7 7 7 
./run-cstacks.fish out-fowleri-M7-g7
./run-sstacks.fish out-fowleri-M7-g7
./run-gstacks.fish out-fowleri-M7-g7
./run-populations.fish out-fowleri-M7-g7 ../popmap-fowleri.txt all --vcf
**Done
```

## Terrestris 
```bash
./run-ustacks.fish ../popmap-terrestris.txt out-terrestris-M7-g7 7 7 
./run-cstacks.fish out-terrestris-M7-g7
./run-sstacks.fish out-terrestris-M7-g7
./run-gstacks.fish out-terrestris-M7-g7
./run-populations.fish out-terrestris-M7-g7 ../popmap-terrestris.txt all --vcf
**Done
```

## Woodhousii 
```bash
./run-ustacks.fish ../popmap-woodhousii.txt out-woodhousii-M7-g7 7 7 
./run-cstacks.fish out-woodhousii-M7-g7
./run-sstacks.fish out-woodhousii-M7-g7
./run-gstacks.fish out-woodhousii-M7-g7
./run-populations.fish out-woodhousii-M7-g7 ../popmap-woodhousii.txt all --vcf
**Done
```

## Hybrid Zone
```bash
./run-ustacks.fish ../popmap-hybrid-zone.txt out-hybrid-zone-M14-g7 14 7 
./run-cstacks.fish out-hybrid-zone-M14-g7
./run-sstacks.fish out-hybrid-zone-M14-g7
./run-gstacks.fish out-hybrid-zone-M14-g7
./run-populations.fish out-hybrid-zone-M14-g7 ../popmap-hybrid-zone.txt all --vcf --hwe
**Done
```


# Filtering

<!-- *********************************************************************** -->
## Americanus
Best alignments
- minSamples1.0-mac3-popmap2: 219 loci, includes americanus from Oklahoma 
- minSamples99-mac3-popmap3: 2006 loci, no missing data 

```bash
./run-populations.fish \
  out-americanus-M7-g7 \
  ../popmap-americanus.txt \
  minSamples1.0-mac3 \
  --min-samples-overall 1.0 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-americanus-M7-g7 \
  ../popmap-americanus.txt \
  minSamples99-mac3 \
  --min-samples-overall 0.99 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-americanus-M7-g7 \
  ../popmap-americanus.txt \
  minSamples95-mac3 \
  --min-samples-overall 0.95 --min-mac 3 --write-random-snp --vcf --structure
```

#### popmap-americanus-2
Dropped msb104571
```bash

./run-populations.fish \
  out-americanus-M7-g7 \
  ../popmap-americanus-2.txt \
  minSamples1.0-mac3-popmap2 \
  --min-samples-overall 1.0 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-americanus-M7-g7 \
  ../popmap-americanus-2.txt \
  minSamples99-mac3-popmap2 \
  --min-samples-overall 0.99 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-americanus-M7-g7 \
  ../popmap-americanus-2.txt \
  minSamples95-mac3-popmap2 \
  --min-samples-overall 0.95 --min-mac 3 --write-random-snp --vcf --structure
```

#### popmap-amerianus-3
Dropped msb104571, msb104608
```bash

./run-populations.fish \
  out-americanus-M7-g7 \
  ../popmap-americanus-3.txt \
  minSamples99-mac3-popmap3 \
  --min-samples-overall 0.99 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-americanus-M7-g7 \
  ../popmap-americanus-3.txt \
  minSamples95-mac3-popmap3 \
  --min-samples-overall 0.95 --min-mac 3 --write-random-snp --vcf --structure
```

<!-- *********************************************************************** -->
## Fowleri
Unfortunately hera13722 and inhs19127 have very low read counts

Best alignments
- minSamples1.0-mac3-popmap2: 4659 loci, missing important samples from KY and IL
- minSamples95-mac3-popmap2: 9185 loci, missing important samples from KY and IL, kac244 from northern LA missing 20% of data

```bash
./run-populations.fish \
  out-fowleri-M7-g7 \
  ../popmap-fowleri.txt \
  minSamples95-mac3 \
  --min-samples-overall 0.95 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-fowleri-M7-g7 \
  ../popmap-fowleri.txt \
  minSamples75-mac3 \
  --min-samples-overall 0.75 --min-mac 3 --write-random-snp --vcf --structure
```

#### popmap-fowleri-2
Dropped hera13722, inhs19127, kac053, kac178, msb104570, t3040, 

```bash
./run-populations.fish \
  out-fowleri-M7-g7 \
  ../popmap-fowleri-2.txt \
  minSamples1.0-mac3-popmap2 \
  --min-samples-overall 1.0 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-fowleri-M7-g7 \
  ../popmap-fowleri-2.txt \
  minSamples95-mac3-popmap2 \
  --min-samples-overall 0.95 --min-mac 3 --write-random-snp --vcf --structure
```

<!-- *********************************************************************** -->
## Terrestris 
Best alignments
- minSamples1.0-mac3-popmap2: 2479 loci
- minSamples1.0-mac3-popmap3: 4395 loci

```bash
./run-populations.fish \
  out-terrestris-M7-g7 \
  ../popmap-terrestris.txt \
  minSamples95-mac3 \
  --min-samples-overall 0.95 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-terrestris-M7-g7 \
  ../popmap-terrestris.txt \
  minSamples75-mac3 \
  --min-samples-overall 0.75 --min-mac 3 --write-random-snp --vcf --structure
```

#### popmap-terrestris-2
Dropped aht3813, aht5276, kac066, kac067, kac201808182

```bash
./run-populations.fish \
  out-terrestris-M7-g7 \
  ../popmap-terrestris-2.txt \
  minSamples1.0-mac3-popmap2 \
  --min-samples-overall 1.0 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-terrestris-M7-g7 \
  ../popmap-terrestris-2.txt \
  minSamples95-mac3-popmap2 \
  --min-samples-overall 0.95 --min-mac 3 --write-random-snp --vcf --structure
```

#### popmap-terrestris-3
Dropped aht3813, aht5276, kac065, kac066, kac067, kac201808182
```bash
./run-populations.fish \
  out-terrestris-M7-g7 \
  ../popmap-terrestris-3.txt \
  minSamples1.0-mac3-popmap3 \
  --min-samples-overall 1.0 --min-mac 3 --write-random-snp --vcf --structure
```

<!-- *********************************************************************** -->
## Woodhousii
Best alignments
- minSamples90-mac3: 511 loci, high missing data from two samples
- minSamples80-mac3-popmap2: 11521 loci, high missing data from 1 sample 
- minSamples1.0-mac3-popmap3: 11443 loci, 0 missing data

```bash
./run-populations.fish \
  out-woodhousii-M7-g7 \
  ../popmap-woodhousii.txt \
  minSamples90-mac3 \
  --min-samples-overall 0.90 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-woodhousii-M7-g7 \
  ../popmap-woodhousii.txt \
  minSamples80-mac3 \
  --min-samples-overall 0.8 --min-mac 3 --write-random-snp --vcf --structure

```

#### popmap-woodhousii-2
Dropped msb98058 

```bash
./run-populations.fish \
  out-woodhousii-M7-g7 \
  ../popmap-woodhousii-2.txt \
  minSamples1.0-mac3-popmap2 \
  --min-samples-overall 1.0 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-woodhousii-M7-g7 \
  ../popmap-woodhousii-2.txt \
  minSamples90-mac3-popmap2 \
  --min-samples-overall 0.90 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-woodhousii-M7-g7 \
  ../popmap-woodhousii-2.txt \
  minSamples80-mac3-popmap2 \
  --min-samples-overall 0.80 --min-mac 3 --write-random-snp --vcf --structure
```

#### popmap-woodhousii-3
Dropped msb98058, msb104548

```bash
./run-populations.fish \
  out-woodhousii-M7-g7 \
  ../popmap-woodhousii-3.txt \
  minSamples1.0-mac3-popmap3 \
  --min-samples-overall 1.0 --min-mac 3 --write-random-snp --vcf --structure
```

<!-- *********************************************************************** -->
## Americanus Group 
Best alignments
- minSamples1.0-mac3-popmap2: 281 loci 
- minSamples95-mac3-popmap2: 1736 loci, kac244, t1020, utep19947, kac166, inhs16273 have more than 10% missing data. inhs16273 has almost 30% 

```bash
./run-populations.fish \
  out-americanus-group-M14-g7 \
  ../popmap-americanus-group.txt \
  minSamples75-mac3 \
  --min-samples-overall 0.75 --min-mac 3 --write-random-snp --vcf --structure
```

#### popmap-americanus-group-2
Dropped aht3813, aht5276, hera11976, hera13722, inhs19127, kac053, kac065, kac066, 
kac067, kac201808182, msb104548, msb104570, msb104571, msb104608 msb98058, t3040, 


```bash
./run-populations.fish \
  out-americanus-group-M14-g7 \
  ../popmap-americanus-group-2.txt \
  minSamples1.0-mac3-popmap2 \
  --min-samples-overall 1.0 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-americanus-group-M14-g7 \
  ../popmap-americanus-group-2.txt \
  minSamples95-mac3-popmap2 \
  --min-samples-overall 0.95 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-americanus-group-M14-g7 \
  ../popmap-americanus-group-2.txt \
  minSamples90-mac3-popmap2 \
  --min-samples-overall 0.9 --min-mac 3 --write-random-snp --vcf --structure

```


<!-- *********************************************************************** -->
## Hybrid Zone
Best alignments
- minSamples1.0-mac3-popmap2: 203 loci, 136 sites 
- minSamples95-mac3-popmap2: 1258 loci, 1194 sites
- minSamples1.0-mac3-popmap3: 239 loci, 173 sites 
- minSamples95-mac3-popmap3: 1370 loci, 1298 sites 

```bash
./run-populations.fish \
  out-hybrid-zone-M14-g7 \
  ../popmap-hybrid-zone.txt \
  minSamples75-mac3-single-snp \
  --min-samples-overall 0.75 --min-mac 3 --write-random-snp --vcf --structure

```

#### popmap-hybrid-zone-2

```bash

./run-populations.fish \
  out-hybrid-zone-M14-g7 \
  ../popmap-hybrid-zone-2.txt \
  minSamples1.0-mac3-popmap2-single-snp \
  --min-samples-overall 1.0 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-hybrid-zone-M14-g7 \
  ../popmap-hybrid-zone-2.txt \
  minSamples95-mac3-popmap2-single-snp \
  --min-samples-overall 0.95 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-hybrid-zone-M14-g7 \
  ../popmap-hybrid-zone-2.txt \
  minSamples95-mac3-popmap2 \
  --min-samples-overall 0.95 --min-mac 3 --vcf

./run-populations.fish \
  out-hybrid-zone-M14-g7 \
  ../popmap-hybrid-zone-2.txt \
  minSamples90-mac3-popmap2-single-snp \
  --min-samples-overall 0.90 --min-mac 3 --write-random-snp --vcf --structure

```

#### popmap-hybrid-zone-3
Dropped  

```bash

./run-populations.fish \
  out-hybrid-zone-M14-g7 \
  ../popmap-hybrid-zone-3.txt \
  minSamples1.0-mac3-popmap3-single-snp \
  --min-samples-overall 1.0 --min-mac 3 --write-random-snp --vcf --structure

./run-populations.fish \
  out-hybrid-zone-M14-g7 \
  ../popmap-hybrid-zone-3.txt \
  minSamples95-mac3-popmap3-single-snp \
  --min-samples-overall 0.95 --min-mac 3 --write-random-snp --vcf --structure

```