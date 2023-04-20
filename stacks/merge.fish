#!/usr/bin/env fish

mkdir merged 

cp plate1/*.fq.gz merged
cp plate2/*.fq.gz merged
cp plate3/*.fq.gz merged

rm merged/kac232*
cat plate2/kac232_1.1.fq.gz plate2/kac232_2.1.fq.gz > merged/kac232.1.fq.gz
cat plate2/kac232_1.2.fq.gz plate2/kac232_2.2.fq.gz > merged/kac232.2.fq.gz
cat plate2/kac232_1.rem.1.fq.gz plate2/kac232_2.rem.1.fq.gz > merged/kac232.rem.1.fq.gz
cat plate2/kac232_1.rem.2.fq.gz plate2/kac232_2.rem.2.fq.gz > merged/kac232.rem.2.fq.gz