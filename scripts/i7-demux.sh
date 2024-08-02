#!/usr/bin/env bash 

read1=$1
read2=$2
barcodes=$3
outdir=$4
name=$5

outpath=$outdir/$name
mkdir -p $outpath 

threads=4


sbatch \
  --job-name i7-demux-$name  \
  --output $outdir/%x-%j.out \
  --mail-type END \
  --time 24:00:00 \
  --cpus-per-task $threads  \
  --mem 10G \
  --partition jro0014_amd \
<< EOF
#!/usr/bin/env bash

process_radtags \
  -1 $read1 \
  -2 $read2 \
  --barcodes $barcodes \
  --out-path $outpath \
  --threads $threads \
  --in-type gzfastq \
  --barcode_dist_1 2 \
  --rescue \
  --index_null \
  --disable_rad_check \
  --retain_header
EOF