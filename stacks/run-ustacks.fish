#!/usr/bin/env fish 

set popmap $argv[1]
set outdir $argv[2]
set M $argv[3] # Maximum distance (in nucleotides) allowed between stacks 
set gaps $argv[4] # Number of gaps allowed

set indir merged
set threads 8 

mkdir $outdir

set ids (awk -F'\t' '{print $1}' $popmap)
set length (count $ids)
echo "Assembling $length samples"

set cmd \
"#!/usr/bin/env fish  

set ids $ids
set id \$ids[\$SLURM_ARRAY_TASK_ID]
echo \"Assembling \$id\"
ustacks \
  -t gzfastq \
  -f $indir/\$id.1.fq.gz \
  -o $outdir \
  -i \$SLURM_ARRAY_TASK_ID \
  --name \$id \
  -p $threads \
  -M $M  \
  --max_gaps $gaps 
"

# echo $cmd > "$outdir/jobscript.fish"

echo $cmd | sbatch \
  --job-name $outdir \
  --output $outdir/%x-%A-%a.out \
  --array 1-$length \
  --cpus-per-task $threads \
  --time 24:00:00 \
  --mem 20G \
  --mail-type END 
  # $outdir/jobscript.fish


