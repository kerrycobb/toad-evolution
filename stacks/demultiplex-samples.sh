#!/usr/bin/env bash 

path="~/toad-data"
threads=4

for i in 1 2 3 
do

out="plate$i"
mkdir $out 
sbatch \
  --job-name demux-$i  \
  --output %x-%j.out \
  --mail-type END \
  --time 24:00:00 \
  --cpus-per-task $threads  \
  --mem 10G \
  --partition jro0014_amd \
<< EOF
#!/usr/bin/env bash

process_radtags \
  -1 $path/plate$i.1.fq.gz \
  -2 $path/plate$i.2.fq.gz \
  -b toad-${i}-barcodes.tsv \
  --out-path $out \
  --renz_1 xbaI \
  --renz_2 ecoRI \
  --barcode_dist_1 2 \
  --barcode_dist_2 2 \
  -i gzfastq \
  --rescue \
  --quality \
  --clean \
  --filter_illumina \
  --inline_inline \
  --retain_header
EOF
done