#!/usr/bin/env fish 

module load structure

set name (string trim --right --chars "/" $argv[1])
set structureInput $argv[2]
set kVals (string split , $argv[3])
set iterations $argv[4]

# Make the output directory if doesn't already exist
set outdir $name
if test -d $outdir 
    echo "Directory already exists."
    exit 1
else
  mkdir $outdir
end

# Copy structure file and replace long names with shorter ones
set structureCopy $outdir/(basename $structureInput)
cp $structureInput $structureCopy
sed -i '1,2d' $structureCopy 
cut -f1,3- $structureCopy > $structureCopy.tmp 
mv $structureCopy.tmp $structureCopy
./rename-structure.py $structureCopy

# Get the number of samples and loci in the file
# set nsamples (math (math (wc -l < $structureCopy) - 0) / 2)
set nsamples (math (wc -l < $structureCopy) / 2)
set nloci (math (awk -F'\t' 'NR==1{print NF}' $structureCopy) - 1)

#  Create arrays for use in batch submission
set nJobs (math $iterations \* (count $kVals))
set kArray
set iArray
set seedArray
for k in (seq (count $kVals))
  for i in (seq $iterations)
    set -a kArray $k
    set -a iArray $i
    set -a seedArray (random)
  end
end

# Store the random seeds
echo $seedArray > $outdir/random_seeds.txt

set cmd \
"#!/usr/bin/env fish

set kArray $kArray
set iArray $iArray
set seedArray $seedArray
set ix \$SLURM_ARRAY_TASK_ID
set k \$kArray[\$ix] 
set i \$iArray[\$ix]
set seed \$seedArray[\$ix]
set outfile $outdir/$name-K\$k-I\$i.str.out

structure \
  -K \$k \
  -L $nloci \
  -N $nsamples \
  -i $structureCopy \
  -o \$outfile \
  -D \$seed 

./rename-structure.py {\$outfile}_f --reverse
"

echo $cmd | sbatch \
  --job-name structure-$name \
  --output $outdir/%x-%A-%a.out \
  --array 1-$nJobs \
  --time=24-00:00:00 \
  --cpus-per-task 1 \
  --mem 20GB 

  # --partition jro0014_amd \

