#!/usr/bin/env fish 

set popmap $argv[1]
set name (string trim --right --chars "/" $argv[2])
set M $argv[3] # Maximum distance (in nucleotides) allowed between stacks 
set gaps $argv[4] # Number of gaps allowed

# Constants
set indir demux/merged
set threads 8 

set logpath $name/logs
mkdir -p $logpath

set outpath $name/stacks
mkdir -p $outpath

# Create config file from input params
echo "popmap: $popmap" > $name/config.txt
echo "M: $M" >> $name/config.txt
echo "gaps: $gaps" >> $name/config.txt
echo "rawReadsDir: $indir" >> $name/config.txt

# File to store stacks id associated with sample id
echo -n "" > "$name/stacks-id.txt"

# Get ids from popmap and get count
set ids (awk -F'\t' '{print $1}' $popmap)
set length (count $ids)
echo "Assembling $length samples"

# Create script for batch submission
set cmd \
"#!/usr/bin/env fish  

set ids $ids
set id \$ids[\$SLURM_ARRAY_TASK_ID]
echo \"Assembling \$id\"
echo \"\$id \$SLURM_ARRAY_TASK_ID\" >> $name/stacks-id.txt
ustacks \
  -t gzfastq \
  -f $indir/\$id.1.fq.gz \
  -o $outpath \
  -i \$SLURM_ARRAY_TASK_ID \
  --name \$id \
  -p $threads \
  -M $M  \
  --max_gaps $gaps 
"

# Execute batch submission
echo $cmd | sbatch \
  --job-name ustacks-$name \
  --output $logpath/%x-%A-%a.out \
  --array 1-$length \
  --cpus-per-task $threads \
  --time 24:00:00 \
  --mem 20G \
  --mail-type END 