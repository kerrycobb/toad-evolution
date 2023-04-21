#!/usr/bin/env fish 

set path "../raw-data"
set threads 8 

for i in 1 2 3 

set out demux/plate$i
mkdir -p $out 

set cmd \
"#!/usr/bin/env bash

process_radtags \
  -1 $path/plate$i.1.fq.gz \
  -2 $path/plate$i.2.fq.gz \
  -b barcodes-plate$i.tsv \
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
"

echo $cmd | sbatch \
  --job-name demux-$i  \
  --output %x-%j.out \
  --mail-type END \
  --time 24:00:00 \
  --cpus-per-task $threads  \
  --mem 10G \
  --partition jro0014_amd

end