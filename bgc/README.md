

# Create Assignment Files
```bash
./gen-sample-assign.py ../structure/qmats/hybrid-zone-minSamples95-mac3-popmap2-K-2.csv popmap2-95 .025 terrestris americanus
./gen-sample-assign.py ../structure/qmats/hybrid-zone-minSamples1.0-mac3-popmap2-K-2.csv popmap2-100 .025 americanus terrestris

./gen-sample-assign.py ../structure/qmats/hybrid-zone-minSamples95-mac3-popmap3-K-2.csv popmap3-95 .025 terrestris americanus
./gen-sample-assign.py ../structure/qmats/hybrid-zone-minSamples1.0-mac3-popmap3-K-2.csv popmap3-100 .025 americanus terrestris
```

# Run BGC

Run with bash shell



## popmap2 100% complete data
```bash
./prepare-bgc.fish ../stacks/out-hybrid-zone-M14-g7/out-minSamples1.0-mac3-popmap2/populations.snps.vcf popmap2-100 assign-popmap2-100-americanus.txt assign-popmap2-100-terrestris.txt assign-popmap2-100-admixed.txt

module load bgc

# Make sure these don't start at the same time or they will have identical starting seeds
for i in $(seq 1 5); do
  ./run-bgc.sh popmap2-100 $i;
  sleep 10;
done
```



## popmap2 95% complete data
```bash
./prepare-bgc.fish ../stacks/out-hybrid-zone-M14-g7/out-minSamples95-mac3-popmap2/populations.snps.vcf popmap2-95 assign-popmap2-95-americanus.txt assign-popmap2-95-terrestris.txt assign-popmap2-95-admixed.txt

module load bgc

# Make sure these don't start at the same time or they will have identical starting seeds
for i in $(seq 1 5); do
  ./run-bgc.sh popmap2-95 $i;
  sleep 10;
done
```



## popmap3 100% complete data
```bash
./prepare-bgc.fish ../stacks/out-hybrid-zone-M14-g7/out-minSamples1.0-mac3-popmap3/populations.snps.vcf popmap3-100 assign-popmap3-100-americanus.txt assign-popmap3-100-terrestris.txt assign-popmap3-100-admixed.txt

module load bgc

# Make sure these don't start at the same time or they will have identical starting seeds
for i in $(seq 1 5); do
  ./run-bgc.sh popmap3-100 $i;
  sleep 10;
done
```



## popmap3 95% complete data
```bash
./prepare-bgc.fish ../stacks/out-hybrid-zone-M14-g7/out-minSamples95-mac3-popmap3/populations.snps.vcf popmap3-95 assign-popmap3-95-americanus.txt assign-popmap3-95-terrestris.txt assign-popmap3-95-admixed.txt

module load bgc

# Make sure these don't start at the same time or they will have identical starting seeds
for i in $(seq 1 5); do
  ./run-bgc.sh popmap3-95 $i;
  sleep 10;
done
```


# Fetch remote files

```bash
./fetch.fish out-popmap2-95
./fetch.fish out-popmap2-100
./fetch.fish out-popmap3-95
./fetch.fish out-popmap3-100
```

# Analyze results
```bash
./bgc_summary.py out-popmap2-95 5 100 0.9
./bgc_summary.py out-popmap3-95 5 100 0.9
./bgc_summary.py out-popmap2-100 5 100 0.9
./bgc_summary.py out-popmap3-100 5 100 0.9
```