#!/usr/bin/env fish

set name (string trim --right --chars "/" $argv[1])

set threads 8

# Read params from config file
set config $name/config.txt
set popmap (sed -n 's/^popmap: //p' $config)

# Get ids from popmap and get count
set ids (awk -F'\t' '{print $1}' $popmap)
set length (count $ids)

# Create script for batch submission
set cmd \
"#!/usr/bin/env fish

set ids $ids
set id \$ids[\$SLURM_ARRAY_TASK_ID]
echo \"Assembling \$id\"

sstacks \
  -c $name/stacks \
  -s $name/stacks/\$id \
  -p $threads \
  -o $name/stacks
"

# Execute batch submission
echo $cmd | sbatch \
  --job-name sstacks-$name \
  --output $name/logs/%x-%A-%a.out \
  --array 1-$length \
  --cpus-per-task $threads \
  --time 24:00:00 \
  --mem 20G \
  --mail-type END 