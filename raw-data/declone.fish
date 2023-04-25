#!/usr/bin/env fish

set threads 8

for i in 1 2 3 

set cmd \
"#!/usr/bin/env fish

clone_filter \
  -1 plate$i.1.fq.gz \
  -2 plate$i.2.fq.gz \
  -i gzfastq \
  -o . \
  --null_index \
  --oligo_len_2 8

mv plate$i.1.1.fq.gz plate$i.decloned.1.fq.gz
mv plate$i.2.2.fq.gz plate$i.decloned.2.fq.gz
"

echo $cmd | sbatch \
  --job-name declone-$i \
  --output %x-%j.out \
  --mail-type END \
  --time 24:00:00 \
  --cpus-per-task $threads  \
  --mem 50G \
  --partition jro0014_amd

end