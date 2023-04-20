#!/usr/bin/env bash

length=4

popmap=$1
outdir=$2
M=$3 # Maximum distance (in nucleotides) allowed between stacks 
gaps=$4 # Number of gaps allowed

indir=merged/
threads=10

mkdir $outdir

ids=($(awk -F'\t' '{print $1}' $popmap))
# length=${#files[@]}

sbatch \
  --job-name $outdir \
  --output $outdir/%x-%A-%a.out \
  --array 0-$(($length - 1)) \
  --cpus-per-task $threads \
  --time 24:00:00 \
  --mem 20G \
  --mail-type END \
<< EOF 
#!/usr/bin/env bash

ids=(\$(awk -F'\t' '{print \$1}' $popmap))
id=\${ids[\$SLURM_ARRAY_TASK_ID]}

ustacks \
  -t gzfastq \
  -f $indir/\$id.1.fq.gz \
  -o $outdir \
  -i \$SLURM_ARRAY_TASK_ID \
  --name \$id \
  -p $threads \
  -M $M  \
  --max_gaps $gaps 

EOF