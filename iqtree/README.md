# Iqtree

## all-c80-defaults
```bash
./run-iqtree.fish \
  all-c80-s61 \
  /scratch/kac0070/toad-phyl/pyrad/all-c80-s61_outfiles/all-c80-s61.phy \
  hera10484

./run-iqtree.fish \
  subset-c80-s28 \
  /scratch/kac0070/toad-phyl/pyrad/all-subset-c80-s28_outfiles/all-subset-c80-s28.phy \
  hera10484

./run-iqtree.fish \
  all-2-c80-s78 \
  /scratch/kac0070/toad-phyl/pyrad/all-2-c80-s78_outfiles/all-2-c80-s78.phy \
  kac243

./run-iqtree.fish \
  all-2-l200-c80-s73 \
  /scratch/kac0070/toad-phyl/pyrad/all-2-l200-c80-s73_outfiles/all-2-l200-c80-s73.phy \
  kac243

```

## Output tree to pdf
```bash
./treefig.py all-c80-s61.phy.contree all-c80-s61-iqtree.pdf hera10484 
./treefig.py all-2-c80-s78.phy.contree all-2-c80-s78-iqtree.pdf kac243  
./treefig.py all-2-l200-c80-s73.phy.contree all-2-l200-c80-s73.pdf kac243
./treefig.py subset-c80-s28.phy.contree subset-c80-s28-iqtree.pdf hera10484 
```

<!-- ## c80-500-loci-defaults 
```bash
./run-iqtree.fish \
  c80-500-loci-defaults \
  /scratch/kac0070/toad-phyl/pyrad/c80-defaults/c80-500-loci-defaults_outfiles/c80-500-loci-defaults.phy 
```

## c80-500-loci-52-samples-defaults
```bash
./run-iqtree.fish \
  c80-500-loci-52-samples-defaults \
  /scratch/kac0070/toad-phyl/pyrad/c80-defaults/c80-500-loci-52-samples-defaults_outfiles/c80-500-loci-52-samples-defaults.phy 
``` -->