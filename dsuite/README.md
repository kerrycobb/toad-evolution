
Run with bash

cp popmap, rename Incillius to indicate that it is the outgroup

```bash
mkdir all-subset-c80-s28

module load gcc/5.3.0

./run-dsuite.bash \
  all-subset-c80-s28 \
  /scratch/kac0070/toad-phyl/pyrad/all-subset-c80-s28_outfiles/all-subset-c80-s28.vcf \
  sp-tree-incillius.tre \
  popmap-all-subset.txt

```