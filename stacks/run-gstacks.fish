#!/usr/bin/env fish

set name (string trim --right --chars "/" $argv[1])

set threads 8

# Read params from config file
set config $name/config.txt
set popmap (sed -n 's/^popmap: //p' $config)
set rawReads (sed -n 's/^rawReadsDir: //p' $config)

# Create script for batch submission
set cmd \
"#!/usr/bin/env fish

tsv2bam \
  --in-dir $name/stacks \
  --popmap $popmap \
  --pe-reads-dir $rawReads \
  -t $threads 

gstacks \
  -P $name/stacks \
  -M $popmap \
  -t $threads 
"

# Execute batch submission
echo $cmd | sbatch \
  --job-name cstacks-$name \
  --output $name/logs/%x-%j.out \
  --cpus-per-task $threads \
  --time 72:00:00 \
  --mem 30G \
  --mail-type END \
  --partition jro0014_amd


