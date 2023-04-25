#!/usr/bin/env fish 

set name (string trim --right --chars "/" $argv[1])

# Constants
set threads 10 

# Load params from config file
set config $name/config.txt
set M (sed -n 's/^M: //p' $config)
set gaps (sed -n 's/^gaps: //p' $config)
set rawReads (sed -n 's/^rawReadsDir: //p' $config)

# Get list of files and sample ids that need to be run again
set outFiles
set sample_ids 
set ids
for file in $name/logs/ustacks-*.out
  set firstLine (head -n 1 $file)
  set -l firstLine (string split " " $firstLine)
  set sample_id $firstLine[2] 
  set lastLine (tail -n 1 $file)
  if [ $lastLine != "ustacks is done." ]
    set -a ids (string split "." (string split "-" $file)[-1])[1]
    set -a outFiles $file
    set -a sample_ids $sample_id
  end
end

set length (count $ids)

# Create script for batch submission
set cmd \
"#!/usr/bin/env fish  

set ids $ids
set sample_ids $sample_ids
set outFiles $outFiles

set id \$ids[\$SLURM_ARRAY_TASK_ID]
set sample_id \$sample_ids[\$SLURM_ARRAY_TASK_ID]
set outFile \$outFiles[\$SLURM_ARRAY_TASK_ID]

echo \"Assembling \$sample_id\"

rm \$outFile
rm $name/stacks/\$sample_id*

ustacks \
  -t gzfastq \
  -f $rawReads/\$sample_id.1.fq.gz \
  -o $name/stacks \
  -i \$id \
  --name \$sample_id \
  -p $threads \
  -M $M  \
  --max_gaps $gaps 

"

# Execute batch submission
echo $cmd | sbatch \
  --job-name ustacks-$name \
  --output $name/logs/%x-%A-%a.out \
  --array 1-$length \
  --cpus-per-task $threads \
  --time 72:00:00 \
  --mem 30G \
  --mail-type END \
  --partition jro0014_amd 