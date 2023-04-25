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
./run-ustacks.fish popmap-all.txt out-all-M21-g7 21 7 
**./run-cstacks.fish out-all-M21-g7
./run-sstacks.fish out-all-M21-g7
./run-gstacks.fish out-all-M21-g7
./run-populations.fish out-all-M21-g7 popmap-all.txt \
  out-all-minSamples75 --min-samples-per-overall 0.75 --vcf --structure
```

## Americanus Group
```bash
./run-ustacks.fish popmap-americanus-group.txt out-americanus-group-M14-g7 14 7 
./run-cstacks.fish out-americanus-group-M14-g7
./run-sstacks.fish out-americanus-group-M14-g7
./run-gstacks.fish out-americanus-group-M14-g7
**./run-populations.fish out-americanus-group-M14-g7 popmap-americanus-group.txt \
  out-all-minSamples75 --min-samples-per-overall 0.75 --vcf --structure
```

## Americanus
```bash
./run-ustacks.fish popmap-americanus.txt out-americanus-M7-g7 7 7 
./run-cstacks.fish out-americanus-M7-g7
./run-sstacks.fish out-americanus-M7-g7
./run-gstacks.fish out-americanus-M7-g7
./run-populations.fish out-americanus-M7-g7 popmap-americanus.txt \
  out-all-minSamples75 --min-samples-overall 0.75 --vcf --structure
*Done
```

## Fowleri
```bash
./run-ustacks.fish popmap-fowleri.txt out-fowleri-M7-g7 7 7 
./run-cstacks.fish out-fowleri-M7-g7
./run-sstacks.fish out-fowleri-M7-g7
./run-gstacks.fish out-fowleri-M7-g7
./run-populations.fish out-fowleri-M7-g7 popmap-fowleri.txt \
  out-all-minSamples75 --min-samples-overall 0.75 --vcf --structure
*Done
```

## Terrestris 
```bash
./run-ustacks.fish popmap-terrestris.txt out-terrestris-M7-g7 7 7 
./run-cstacks.fish out-terrestris-M7-g7
./run-sstacks.fish out-terrestris-M7-g7
./run-gstacks.fish out-terrestris-M7-g7
./run-populations.fish out-terrestris-M7-g7 popmap-terrestris.txt \
  out-all-minSamples75 --min-samples-overall 0.75 --vcf --structure
*Done
```

## Woodhousii 
```bash
./run-ustacks.fish popmap-woodhousii.txt out-woodhousii-M7-g7 7 7 
./run-cstacks.fish out-woodhousii-M7-g7
./run-sstacks.fish out-woodhousii-M7-g7
./run-gstacks.fish out-woodhousii-M7-g7
./run-populations.fish out-woodhousii-M7-g7 popmap-woodhousii.txt \
  out-all-minSamples75 --min-samples-overall 0.75 --vcf --structure
*Done
```

## Hybrid Zone


<!-- slurmstepd: error: *** JOB 602487 ON node030 CANCELLED AT 2023-04-22T03:09:19 DUE TO TIME LIMIT ***
slurmstepd: error: *** JOB 602447 ON node071 CANCELLED AT 2023-04-22T01:51:49 DUE TO TIME LIMIT ***
slurmstepd: error: *** JOB 602328 ON node216 CANCELLED AT 2023-04-21T22:10:47 DUE TO TIME LIMIT ***
slurmstepd: error: *** JOB 602350 ON node074 CANCELLED AT 2023-04-22T08:42:44 *** -->