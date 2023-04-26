#!/usr/bin/env fish

set inp demux
set out demux/merged

mkdir $out 

cp $inp/plate1/*.fq.gz $out 
cp $inp/plate2/*.fq.gz $out 
cp $inp/plate3/*.fq.gz $out 

set duplicates plate2/kac232 plate2/kac161 plate2/kac187 plate2/kac211 plate2/kac221

for i in $duplicates 
  set sample (string split / $i )[2]
  rm $out/$sample*
  cat $inp/{$i}_1.1.fq.gz     $inp/{$i}_2.1.fq.gz     > $out/$sample.1.fq.gz
  cat $inp/{$i}_1.2.fq.gz     $inp/{$i}_2.2.fq.gz     > $out/$sample.2.fq.gz
  cat $inp/{$i}_1.rem.1.fq.gz $inp/{$i}_2.rem.1.fq.gz > $out/$sample.rem.1.fq.gz
  cat $inp/{$i}_1.rem.2.fq.gz $inp/{$i}_2.rem.2.fq.gz > $out/$sample.rem.2.fq.gz
end