#!/usr/bin/env fish

set inp demux
set out demux/merged

mkdir $out 

cp $inp/plate1/*.fq.gz $out 
cp $inp/plate2/*.fq.gz $out 
cp $inp/plate3/*.fq.gz $out 

for i in plate2/kac232 plate2/kac161 plate2/kac187 plate2/kac211 plate2/kac221

set id (string split -m 1 $i /)[1]
rm $out/$id.*
cat $inp/$i_1.1.fq.gz     $inp/$i_2.1.fq.gz     > $out/$id.1.fq.gz
cat $inp/$i_1.2.fq.gz     $inp/$i_2.2.fq.gz     > $out/$id.2.fq.gz
cat $inp/$i_1.rem.1.fq.gz $inp/$i_2.rem.1.fq.gz > $out/$id.rem.1.fq.gz
cat $inp/$i_1.rem.2.fq.gz $inp/$i_2.rem.2.fq.gz > $out/$id.rem.2.fq.gz

end