#!/usr/bin/env fish

set name (string trim --right --chars "/" $argv[1])

set threads 8

# Read params from config file
set config $name/config.txt
set popmap (sed -n 's/^popmap: //p' $config)
set M (sed -n 's/^M: //p' $config)
set gaps (sed -n 's/^gaps: //p' $config)

# Create script for batch submission
set cmd \
"#!/usr/bin/env fish

cstacks \
  --in_path $name/stacks \
  --popmap $popmap \
  -n $M \
  --max_gaps $gaps \
  --threads $threads
"

# Execute batch submission
echo $cmd | sbatch \
  --job-name cstacks-$name \
  --output $name/%x-%j.out \
  --cpus-per-task $threads \
  --time 72:00:00 \
  --mem 30G \
  --mail-type END \
  --partition jro0014_amd