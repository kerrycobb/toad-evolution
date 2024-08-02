# Toad Evolution

This repository has the scripts used to process and analyze 3RAD data collected
to study phylogeography and hybridization in North American toads.

## Raw Data
Backed up at mars.auburn.edu:/home/phyletica/indigo-toads


## Demultiplex i7 indexes
```bash
module load stacks

./scripts/i7-demux.sh \
  raw-data/oaks_june_2022_CKDL220014323-1A_HHM3TBBXX_L4_1.fq.gz \
  raw-data/oaks_june_2022_CKDL220014323-1A_HHM3TBBXX_L4_2.fq.gz \
  data/i7-indexes.tsv \
  demux/ \
  L4

./scripts/i7-demux.sh \
  raw-data/oaks_june_2022_CKDL220014323-1A_HHM3TBBXX_L5_1.fq.gz \
  raw-data/oaks_june_2022_CKDL220014323-1A_HHM3TBBXX_L5_2.fq.gz \
  data/i7-indexes.tsv \
  demux/ \
  L5

./scripts/i7-demux.sh \
  raw-data/oaks_june_2022_CKDL220014323-1A_HHM3TBBXX_L6_1.fq.gz \
  raw-data/oaks_june_2022_CKDL220014323-1A_HHM3TBBXX_L6_2.fq.gz \
  data/i7-indexes.tsv \
  demux/ \
  L6
```


## Concatenate
Concatenate samples from the same plates

```bash
sbatch --job-name concatenate --output demux/%x-%j.out \
  scripts/concatenate.fish \
    data/plate-names.txt \
    demux/ \
    demux/L4 \
    demux/L5 \
    demux/L6
``` 


## Rename files
Make file names compatible with Pyrad

```bash
mv demux/toad-1.1.fq.gz demux/toad-1_R1_.fq.gz
mv demux/toad-1.2.fq.gz demux/toad-1_R2_.fq.gz
mv demux/toad-2.1.fq.gz demux/toad-2_R1_.fq.gz
mv demux/toad-2.2.fq.gz demux/toad-2_R2_.fq.gz
mv demux/toad-3.1.fq.gz demux/toad-3_R1_.fq.gz
mv demux/toad-3.2.fq.gz demux/toad-3_R2_.fq.gz
```

## ipyrad

### Demultiplex

```fish
for i in 1 2 3
  sbatch -J demux-toad-$i -o %x-%j.out \
     -t 1-00:00:00 -c 5 --mem 20G --partition jro0014_amd \
     --wrap "ipyrad -p params-toad-$i.txt -s 1 -c 5"
end
```

### Merge
`ipyrad -m toad-merge params-toad-1.txt params-toad-2.txt params-toad-3.txt`
Move toad-merge.json and replace two instances of project directory path 
Replace project directory path with correct path in params file


### Branching

```bash
ipyrad -p params-toad-merge.txt -b clust-80-defaults
ipyrad -p params-toad-merge.txt -b clust-85-defaults 
ipyrad -p params-toad-merge.txt -b clust-90-defaults

ipyrad -p params-clust-80-defaults.txt -b clust-80-indel-16-snps-0p3-samples-140 
ipyrad -p params-clust-85-defaults.txt -b clust-85-indel-16-snps-0p3-samples-140 
ipyrad -p params-clust-90-defaults.txt -b clust-90-indel-16-snps-samples-140 

```


### Assemble 
```bash
sbatch -J clust-85-defaults -o %x-%j.out --mail-type END -t 6-00:00:00 -c 10 \
  --mem 50G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-85-defaults.txt -s 234567 -c 10"

sbatch -J clust-80-defaults -o %x-%j.out --mail-type END -t 6-00:00:00 -c 10 \
  --mem 50G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-defaults.txt -s 234567 -c 10"

sbatch -J clust-90-defaults -o %x-%j.out --mail-type END -t 6-00:00:00 -c 10 \
  --mem 50G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-90-defaults.txt -s 234567 -c 10"

```


## Filter

```bash
sbatch -J clust-80-indel-16-snps-0p3 -o %x-%j.out --mail-type END -t 2-00:00:00 -c 10 \
  --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-140.txt -s 7 -c 10"

sbatch -J clust-85-indel-16 -o %x-%j.out --mail-type END -t 2-00:00:00 -c 10 \
  --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-85-indel-16-samples-140.txt -s 7 -c 10"

sbatch -J clust-90-indel-16 -o %x-%j.out --mail-type END -t 2-00:00:00 -c 10 \
  --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-samples-140.txt -s 7 -c 10"

```


### Drop samples

#### Exclude 1
Drop samples that don't fall within a plausible grouping and samples with mostly
missing data. Used for ML
```bash

../scripts/ipyrad-branch-exclude.fish \
  params-clust-80-indel-16-snps-0p3-samples-140.txt \
  clust-80-indel-16-snps-0p3-samples-140-exclude-1 \
  ../data/exclude-samples-1.txt

./get_included_samples.py \
  ../data/exclude-samples-1.txt \
  ../data/exclude-1-included-samples.txt 

sbatch -J clust-80-indel-16-snps-0p3-samples-140-exclude-1 -o %x-%j.out \
  -t 1:00:00 --mem 30G 
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-140-exclude-1.txt -s 7"

```

#### Exclude 2
Exclude samples that have only a high degree of missing data
```bash

../scripts/ipyrad-branch-exclude.fish \
  params-clust-80-indel-16-snps-0p3-samples-140.txt \
  clust-80-indel-16-snps-0p3-samples-140-exclude-2 \
  ../data/exclude-samples-2.txt

../scripts/get_included_samples.py \
  ../data/exclude-samples-2.txt \
  ../data/exclude-2-included-samples.txt 

sbatch -J clust-80-indel-16-snps-0p3-samples-140-exclude-2 -o %x-%j.out \
  -t 1:00:00 --mem 30G \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-140-exclude-2.txt -s 7"

```


#### phyco-1 
Reduce data set to at most 4 individuals per species for PhycoEval, Excludes nebulifer and HERA10484

##### 75% locus coverage
```bash

../scripts/ipyrad-branch-include.fish \
  params-clust-80-indel-16-snps-0p3-samples-140.txt \
  clust-80-indel-16-snps-0p3-samples-24-include-phyco-1 \
  ../data/include-phyco-1.txt

```

Edit params file locus coverage.

```bash

sbatch -J clust-80-indel-16-snps-0p3-samples-24-include-phyco-1 -o %x-%j.out \
  -t 2:00:00 --mem 10G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-24-include-phyco-1.txt -s 7 -c 10"

```

#### phyco-neb-1 
Reduce data set to at most 4 individuals per species for PhycoEval, excludes HERA10484, includes nebulifer

##### 75% locus coverage
```bash

../scripts/ipyrad-branch-include.fish \
  params-clust-80-indel-16-snps-0p3-samples-140.txt \
  clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1 \
  ../data/include-phyco-neb-1.txt

```

Edit params file locus coverage.

```bash

sbatch -J clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1 -o %x-%j.out \
  -t 2:00:00 --mem 10G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1.txt -s 7 -c 10"

```


#### phyco-neb-unkn-1 
Reduce data set to at most 4 individuals per species for PhycoEval, includes nebulifer and HERA10484

##### 75% locus coverage
```bash

../scripts/ipyrad-branch-include.fish \
  params-clust-80-indel-16-snps-0p3-samples-140.txt \
  clust-80-indel-16-snps-0p3-samples-26-include-phyco-neb-unkn-1 \
  ../data/include-phyco-neb-unkn-1.txt

```

Edit params file locus coverage.

```bash

sbatch -J clust-80-indel-16-snps-0p3-samples-26-include-phyco-neb-unkn-1 -o %x-%j.out \
  -t 2:00:00 --mem 10G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-26-include-phyco-neb-unkn-1.txt -s 7 -c 10"

```



##### Include 1
Reduce data set to evenly distributed subset with high quality data to run with PhycoEval
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-80-indel-16-snps-0p3-samples-140.txt \
  clust-80-indel-16-snps-0p3-samples-51-include-1 \
  ../data/include-samples-1.txt

../scripts/ipyrad-branch-include.fish \
  params-clust-80-indel-16-snps-0p3-samples-140.txt \
  clust-80-indel-16-snps-0p3-samples-61-include-1 \
  ../data/include-samples-1.txt
```

Edit params file. Change number of samples per locus 

```bash
sbatch -J clust-80-indel-16-snps-0p3-samples-51-include-1 -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-51-include-1.txt -s 7 -c 10"

sbatch -J clust-80-indel-16-snps-0p3-samples-61-include-1 -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-61-include-1.txt -s 7 -c 10"
```

##### Include 2
Same as include 1 but without I. nebulifer

```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-80-indel-16-snps-0p3-samples-140.txt \
  clust-80-indel-16-snps-0p3-samples-60-include-1 \
  ../data/include-samples-2.txt
```

```bash
sbatch -J clust-80-indel-16-snps-0p3-samples-60-include-2 -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-60-include-2.txt -s 7 -c 10"
```

#### Include 3
Same as two but with a maximum of 4 samples per species.
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-80-indel-16-snps-0p3-samples-140.txt \
  clust-80-indel-16-snps-0p3-samples-24-include-3 \
  ../data/include-samples-3.txt
```

Edit params file.

```bash
sbatch -J clust-80-indel-16-snps-0p3-samples-24-include-3 -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-24-include-3.txt -s 7 -c 10"
```

#### Include 3-nebulifer
Same as 3 but with inclusion of nebulifer.
Same as two but with a maximum of 4 samples per species.
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-80-indel-16-snps-0p3-samples-140.txt \
  clust-80-indel-16-snps-0p3-samples-25-include-3-nebulifer \
  ../data/include-samples-3-nebulifer.txt
```

Edit params file.

```bash
sbatch -J clust-80-indel-16-snps-0p3-samples-25-include-3-nebulifer -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-25-include-3-nebulifer.txt -s 7 -c 10"
```


#### Include 3.2
Same as 3 but excluding hemiophrys and baxteri due to the really long branch 
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-80-indel-16-snps-0p3-samples-140.txt \
  clust-80-indel-16-snps-0p3-samples-12-include-3_2 \
  ../data/include-samples-3.2.txt

```

Edit params files.


```bash
sbatch -J clust-80-indel-16-snps-0p3-samples-6-include-3.2 -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-6-include-3_2.txt -s 7 -c 10"

sbatch -J clust-80-indel-16-snps-0p3-samples-8-include-3.2 -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-8-include-3_2.txt -s 7 -c 10"

sbatch -J clust-80-indel-16-snps-0p3-samples-12-include-3.2 -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-80-indel-16-snps-0p3-samples-12-include-3_2.txt -s 7 -c 10"
```



#### americanus-group-1
fowleri, americanus, terrestris, woodhousii

##### 75% locus coverage
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-90-indel-16-samples-140.txt \
  clust-90-indel-16-samples-165-include-americanus-group-1 \
  ../data/include-americanus-group-1.txt
```

Edit params file.

```bash
sbatch -J clust-90-indel-16-samples-165-include-americanus-group-1 -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-90-indel-16-samples-165-include-americanus-group-1.txt -s 7 -c 10"
```

##### 90% locus coverage
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-90-indel-16-samples-140.txt \
  clust-90-indel-16-samples-198-include-americanus-group-1 \
  ../data/include-americanus-group-1.txt
```

Edit params file.

```bash
sbatch -J clust-90-indel-16-samples-198-include-americanus-group-1 -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-90-indel-16-samples-198-include-americanus-group-1.txt -s 7 -c 10"
```

#### americanus-group-2
fowleri, americanus, terrestris, woodhousii
Excluding samples that have greater than 25% missing data in 
clust-90-indel-16-samples-198-include-americanus-group-1 alignment.

##### 90% locus coverage
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-90-indel-16-samples-140.txt \
  clust-90-indel-16-samples-179-include-americanus-group-2 \
  ../data/include-americanus-group-2.txt
```

Edit params file.

```bash
sbatch -J clust-90-indel-16-samples-179-include-americanus-group-2 -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-90-indel-16-samples-179-include-americanus-group-2.txt -s 7 -c 10"
```

#### ameri-terr-1
americanus and terrestris samples

##### 90% locus coverage
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-90-indel-16-samples-140.txt \
  clust-90-indel-16-samples-149-include-amer-terr-1 \
  ../data/include-amer-terr-1.txt
```

Edit params file.

```bash
sbatch -J clust-90-indel-16-samples-149-include-amer-terr-1 -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-90-indel-16-samples-149-include-amer-terr-1.txt -s 7 -c 10"
```

#### ameri-terr-2
americanus and terrestris samples excluding any that had greater than 10% 
of fowleri/woodhousii ancestry based on clust-90-indel-16-samples-139-include-americanus-group-2 
structure analysis

##### 90% locus coverage
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-90-indel-16-samples-140.txt \
  clust-90-indel-16-samples-139-include-amer-terr-2 \
  ../data/include-amer-terr-2.txt
```

Edit params file.

```bash
sbatch -J clust-90-indel-16-samples-139-include-amer-terr-2 -o %x-%j.out \
  -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-90-indel-16-samples-139-include-amer-terr-2.txt -s 7 -c 10"
```



<!-- 
### americanus-1
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-90-indel-16-samples-140.txt \
  clust-90-indel-16-samples-57-include-americanus-1 \
  ../data/include-americanus-1.txt
```

Edit params file.

```bash
sbatch -J clust-90-indel-16-samples-57-include-americanus-1 -o %x-%j.out \
  --mail-type END -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-90-indel-16-samples-52-include-americanus-1.txt -s 7 -c 10"
```

### americanus-2
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-90-indel-16-samples-140.txt \
  clust-90-indel-16-samples-52-include-americanus-2 \
  ../data/include-americanus-2.txt
```

Edit params file.

```bash
sbatch -J clust-90-indel-16-samples-52-include-americanus-2 -o %x-%j.out \
  --mail-type END -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-90-indel-16-samples-52-include-americanus-2.txt -s 7 -c 10"
```

### terrestris-1
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-90-indel-16-samples-140.txt \
  clust-90-indel-16-samples-81-include-terrestris-1 \
  ../data/include-terrestris-1.txt
```

Edit params file.

```bash
sbatch -J clust-90-indel-16-samples-81-include-terrestris-1 -o %x-%j.out \
  --mail-type END -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-90-indel-16-samples-81-include-terrestris-1.txt -s 7 -c 10"
```

### terrestris-2
```bash
../scripts/ipyrad-branch-include.fish \
  params-clust-90-indel-16-samples-140.txt \
  clust-90-indel-16-samples-75-include-terrestris-2 \
  ../data/include-terrestris-2.txt
```

Edit params file.

```bash
sbatch -J clust-90-indel-16-samples-75-include-terrestris-2 -o %x-%j.out \
  --mail-type END -t 1-00:00:00 --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-clust-90-indel-16-samples-75-include-terrestris-2.txt -s 7 -c 10"
``` -->


## Iqtree
### Exclude 1
```bash
./run-iqtree.fish clust-80-indel-16-snps-0p3-samples-140-exclude-1 
```

### Exclude 2
```bash
./run-iqtree.fish clust-80-indel-16-snps-0p3-samples-140-exclude-2 
```

```bash
./run-iqtree.fish clust-80-indel-16-snps-0p3-samples-51-include-1 snps 
./rerun-iqtree.fish clust-80-indel-16-snps-0p3-samples-51-include-1-snps/clust-80-indel-16-snps-0p3-samples-51-include-1.snps.varsites.phy

```

## Phycoeval

```bash
TODO: Delete these:
# ./run-phycoeval.fish config.yaml clust-80-indel-16-snps-0p3-samples-60-include-2 5
# # BiAllele Output:
# # 920 site with columns containing only N excluded.
# # 970 site with more than two character states were excluded.

# ./run-phycoeval.fish config.yaml clust-80-indel-16-snps-0p3-samples-24-include-3 5 


# ./run-phycoeval.fish config.yaml clust-80-indel-16-snps-0p3-samples-25-include-3-nebulifer 5
# # BiAllele Output:
# # 2101 sites with columns containing only N excluded.
# # 1382 sites with more than two character states were excluded.

./run-phycoeval.fish config.yaml clust-80-indel-16-snps-0p3-samples-24-include-phyco-1 5
# BiAllele Output:
# 2247 sites with columns containing only N excluded.
# 1113 sites with more than two character states were excluded.

./run-phycoeval.fish config.yaml clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1 5
# BiAllele Output:
# 2053 sites with columns containing only N excluded.
# 1155 sites with more than two character states were excluded.

./run-phycoeval.fish config.yaml clust-80-indel-16-snps-0p3-samples-26-include-phyco-neb-unkn-1 5
# BiAllele Output:
# 1833 sites with columns containing only N excluded.
# 1204 sites with more than two character states were excluded.

```



### Summarize Phycoeval

```bash
./assess-phycoeval.fish clust-80-indel-16-snps-0p3-samples-24-include-3 
cat clust-80-indel-16-snps-0p3-samples-24-include-3/divergence-stats.tsv 
# Decide on burnin
./summarize-phycoeval.fish clust-80-indel-16-snps-0p3-samples-24-include-3 100

./assess-phycoeval.fish clust-80-indel-16-snps-0p3-samples-25-include-3-nebulifer 
cat clust-80-indel-16-snps-0p3-samples-25-include-3-nebulifer/divergence-stats.tsv 
# Decide on burnin
./summarize-phycoeval.fish clust-80-indel-16-snps-0p3-samples-25-include-3-nebulifer 100


```

<!-- 
## PhyloNet
```bash
./run-phylonet.fish clust-80-indel-16-snps-0p3-samples-12-include-3_2 ../data/include-samples-3.2.txt 5 snp 50 
``` -->


<!-- ## PopCluster
```bash
./prep-popcluster.fish clust-90-indel-16-samples-152-include-5
```

Edit config

```bash
./run-popcluster.fish clust-90-indel-16-samples-152-include-5/clust-90-indel-16-samples-152-include-5.config 
``` -->


<!-- ## PCA -->

<!-- ```bash
# ./pyrad_pca.py clust-80-indel-16-snps-0p3-samples-140-exclude-1 ../data/exclude-1-included-samples.txt
``` -->


<!-- ## SVD-Quartets
```bash

# ./run-svd.fish clust-80-indel-16-snps-0p3-samples-140 usnps 1.0 1.0 5 10G
# ./run-svd.fish clust-85-indel-16-samples-140 usnps 1.0 1.0 5 10G    
# ./run-svd.fish clust-90-indel-16-samples-140 usnps 1.0 1.0 5 10G    

# ./run-svd.fish clust-80-indel-16-snps-0p3-samples-140 snps 1.0 1.0 5 10G
# ./run-svd.fish clust-85-indel-16-samples-140 snps 1.0 1.0 5 10G    
# ./run-svd.fish clust-90-indel-16-samples-140 snps 1.0 1.0 5 10G 

``` -->




# DSuite

./run-dsuite.fish clust-80-indel-16-snps-0p3-samples-60-include-2 ../data/include-samples-2.txt



# Structure

```bash
./run-structure.fish clust-90-indel-16-samples-179-include-americanus-group-2 2,3,4,5,6,7 20      
./run-structure.fish clust-90-indel-16-samples-150-include-amer-terr-1 2,3,4,5 20
./run-structure.fish clust-90-indel-16-samples-140-include-amer-terr-2 2,3,4,5 20
```
