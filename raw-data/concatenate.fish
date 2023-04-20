#!/usr/bin/env fish  

for i in 1 2

cat \
L4/iTru7_111_01-toad-1.$i.fq.gz \
L4/iTru7_111_02-toad-1.$i.fq.gz \
L5/iTru7_111_01-toad-1.$i.fq.gz \
L5/iTru7_111_02-toad-1.$i.fq.gz \
L6/iTru7_111_01-toad-1.$i.fq.gz \
L6/iTru7_111_02-toad-1.$i.fq.gz \
> plate1.$i.fq.gz

cat \
L4/iTru7_111_05-toad-2.$i.fq.gz \
L4/iTru7_111_06-toad-2.$i.fq.gz \
L5/iTru7_111_05-toad-2.$i.fq.gz \
L5/iTru7_111_06-toad-2.$i.fq.gz \
L6/iTru7_111_05-toad-2.$i.fq.gz \
L6/iTru7_111_06-toad-2.$i.fq.gz \
> plate2.$i.fq.gz

cat \
L4/iTru7_111_11-toad-3.$i.fq.gz \
L4/iTru7_111_12-toad-3.$i.fq.gz \
L5/iTru7_111_11-toad-3.$i.fq.gz \
L5/iTru7_111_12-toad-3.$i.fq.gz \
L6/iTru7_111_11-toad-3.$i.fq.gz \
L6/iTru7_111_12-toad-3.$i.fq.gz \
> plate3.$i.fq.gz

end
