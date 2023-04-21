#!/usr/bin/env fish

set name (string trim --right --chars "/" $argv[1])
set popmap $argv[2]
set outdir $argv[3]
set args $argv[4..]

set threads 8

set outpath $name/$outdir
mkdir $outpath

# Create script for batch submission
set cmd \
"#!/usr/bin/env fish

populations \
  --in-path $name/stacks \
  --out-path $outpath \
  --threads $threads \
  --popmap $popmap \
  $args
"

# Execute batch submission
echo $cmd | sbatch \
  --job-name pop-$name \
  --output $name/%x-%j.out \
  --cpus-per-task $threads \
  --time 4:00:00 \
  --mem 10G \
  --partition jro0014_amd #\
  # --mail-type END \


