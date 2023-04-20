#!/usr/bin/env bash

popmap=$1
outdir=$2
M=$3 # Maximum distance (in nucleotides) allowed between stacks 
# N=$4 # Maximum distance allowed to align secondary reads to primary stacks 
# gaps=$5 # Number of gaps allowed
gaps=$4 # Number of gaps allowed

threads=8

mkdir $outdir

sbatch \
  --job-name $outdir  \
  --output %x-%j.out \
  --mail-type END \
  --time 7-00:00:00 \
  --cpus-per-task $threads  \
  --mem 30G \
  --partition jro0014_amd \
<< EOF
#!/usr/bin/env bash

denovo_map.pl \
    --samples merged/ \
    --popmap $popmap \
    -o $outdir \
    --threads $threads \
    --paired \
    -M $M \
    -X "ustacks: --max_gaps $gaps" 
    -X "cstacks: --max_gaps $gaps"
EOF
    # -X "ustacks: -N $N --max_gaps $gaps" 