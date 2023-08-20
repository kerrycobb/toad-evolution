#!/usr/bin/env fish 

set name $argv[1]
set path $argv[2]
set outgroup $argv[3]

set cpus 5 
set mem 10G 
set outdir $name"/"
set inpath $path 
set datapath $outdir$name".phy"

mkdir $outdir

# set script """ 
#   cp $inpath $datapath
#   ../scripts/find_replace.py $datapath
#   iqtree -m GTR -bb 1000 -o $outgroup -s $datapath -nt $cpus -mem $mem
# """

set script """ 
  cp $inpath $datapath
  iqtree -m GTR -bb 1000 -o $outgroup -s $datapath -nt $cpus -mem $mem
"""

set script """ 
  cp $inpath $datapath
  iqtree -m GTR -bb 1000 -o $outgroup -s $datapath -nt $cpus -mem $mem
"""

sbatch \
  --job-name "iqtree-"$name \
  --output $outdir%x-%j.out \
  --mail-type END \
  --partition jro0014_amd \
  --time 2-00:00:00 \
  --cpus-per-task $cpus \
  --mem $mem \
  --wrap $script 








