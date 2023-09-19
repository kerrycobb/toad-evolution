
Run with bash

# c80-500-loci-defaults 
```bash
mkdir c80-500-loci-defaults/
```

Make `c80-500-loci-defaults/ignore.txt` file with Rhinella sample id to ignore Rhinella

```bash
./make_pop_map.py \
  /scratch/kac0070/toad-phyl/pyrad/c80-defaults/c80-500-loci-defaults_outfiles/c80-500-loci-defaults.vcf \
  c80-500-loci-defaults/popmap.txt \
  nebulifer \
  c80-500-loci-defaults/ignore.txt

module load gcc/5.3.0

./run-dsuite \
  c80-500-loci-defaults \
  /scratch/kac0070/toad-phyl/pyrad/c80-defaults/c80-500-loci-defaults_outfiles/c80-500-loci-defaults.vcf \
  sp-tree-incillius.tre \
  popmap.txt

```

# Fetch output

```bash
./fetch.fish all-subset-c80-s28/
```