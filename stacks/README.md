# Demux samples
```bash
module load stacks
./demultiplex-samples.sh
./merge.fish
```
Moved everything related to demultiplexing into the merged directory to declutter.


# Alignment


./run-denovo-map.sh popmap=$1 outdir=$2 M=$3 N=$4 gaps=$5

140 bp length reads
85%: 21 
90%: 14
95%: 7

```bash
module load gcc/5.3.0
# ./run-denovo-map.sh popmap-all.txt out-all-M42-N52-g14 42 52 14
# ./run-denovo-map.sh popmap-all.txt out-all-M21-N28-g7 21 28 7
./run-denovo-map.sh popmap-all.txt out-all-M21-g7 21 7 

./run-ustacks.fish popmap-americanus.txt out-americanus-M7-g7 7 7 
```