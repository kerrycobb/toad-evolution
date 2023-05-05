#!/usr/bin/env fish

set indir "demux/merged"
set outfile "demux/read-counts.txt"

echo -n > $outfile 

for i in (find $indir -name '*.1.fq.gz' ! -name '*.rem.1.fq.gz' -type f)
  set sample (string split "." -m1 (basename $i))[1]
  set num (math (zcat $i | wc -l) / 4)
  printf "$sample\t$num\n" >> $outfile
end