#!/usr/bin/env bash 

prefix="oaks_june_2022_CKDL220014323-1A_HHM3TBBXX"
threads=4

for i in 4 5 6
do

out="L$i"
mkdir $out 
sbatch \
  --job-name i7-demux-$i  \
  --output %x-%j.out \
  --mail-type END \
  --time 24:00:00 \
  --cpus-per-task $threads  \
  --mem 10G \
  --partition jro0014_amd \
<< EOF
#!/usr/bin/env bash

process_radtags \
  -1 ${prefix}_${out}_1.fq.gz \
  -2 ${prefix}_${out}_2.fq.gz \
  --barcodes i7-indexes.tsv \
  --out-path $out \
  --threads $threads \
  --in-type gzfastq \
  --barcode_dist_1 2 \
  --rescue \
  --index_null \
  --disable_rad_check \
  --retain_header
EOF

done