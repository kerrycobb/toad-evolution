#!/usr/bin/env fish 

set dataPath $argv[1]
set cpus 5 
set mem 10G 

set name (string split '/' $dataPath)[1]"-rerun"

set batchCmd \
  "sbatch" \
  "--job-name iqtree-$name" \
  "--output %x-%j.out" \
  "--mail-type=END" \
  "--partition jro0014_amd" \
  "--time=6-00:00:00" \
  "--cpus-per-task $cpus" \
  "--mem $mem" \
  "--wrap" 

set cmds \
  "../scripts/filter_alignment.py $dataPath $dataPath;" \
  "iqtree -m GTR+ASC -bb 1000 -s $dataPath -nt $cpus -mem $mem"


eval "$batchCmd \"$cmds\""
# echo "$batchCmd \"$cmds\""