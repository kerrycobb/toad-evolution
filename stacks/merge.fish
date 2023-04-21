#!/usr/bin/env fish

mkdir demux/merged 

cp demux/plate1/*.fq.gz merged
cp demux/plate2/*.fq.gz merged
cp demux/plate3/*.fq.gz merged

for i in plate2/kac232 plate2/kac161 plate2/kac187 plate2/kac211 plate2/kac221 plate2/kac232

set id (string split -m 1 $i /)[1]
rm merged/$id*
cat $i_1.1.fq.gz     $i_2.1.fq.gz     > merged/$i.1.fq.gz
cat $i_1.2.fq.gz     $i_2.2.fq.gz     > merged/$i.2.fq.gz
cat $i_1.rem.1.fq.gz $i_2.rem.1.fq.gz > merged/$i.rem.1.fq.gz
cat $i_1.rem.2.fq.gz $i_2.rem.2.fq.gz > merged/$i.rem.2.fq.gz

end