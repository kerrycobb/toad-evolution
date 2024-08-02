#!/usr/bin/env fish 

module load structure

set name $argv[1]
set kVals (string split , $argv[2])
set iterations $argv[3]

set infile $name/$name.str

set nsamples (math (wc -l < $infile) / 2) 
set nloci (math (head -n 1 $infile | awk '{print NF}') - 1)

./rename-structure.py $infile

for k in $kVals
  for i in (seq $iterations)
    set outfile $name/$name.K-$k.I-$i.str.out
    set seed (random) 
    sbatch \
      --job-name structure-$name \
      --output $name"/%x-%j.out" \
      --partition jro0014_amd \
      --time=6-00:00:00 \
      --cpus-per-task 1 \
      --mem 20GB \
      --wrap "structure -K $k -L $nloci -N $nsamples -i $infile -o $outfile -D $seed; ./rename-structure.py $outfile_f --reverse"
  end
end
