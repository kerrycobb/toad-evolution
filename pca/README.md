
# Run PCA and plot

```bash

./fetch.fish out-hybrid-zone-minSamples95-mac3-popmap2
./fetch.fish out-hybrid-zone-minSamples1.0-mac3-popmap2
./fetch.fish out-hybrid-zone-minSamples95-mac3-popmap3
./fetch.fish out-hybrid-zone-minSamples1.0-mac3-popmap3

./run-pca.r out-hybrid-zone-minSamples95-mac3-popmap2
./run-pca.r out-hybrid-zone-minSamples1.0-mac3-popmap2
./run-pca.r out-hybrid-zone-minSamples95-mac3-popmap3
./run-pca.r out-hybrid-zone-minSamples1.0-mac3-popmap3

./plot-hybrid-pca.py out-hybrid-zone-minSamples95-mac3-popmap2 hybrid-zone-minSamples95-mac3-popmap2 assign-popmap2-95 True 
./plot-hybrid-pca.py out-hybrid-zone-minSamples1.0-mac3-popmap2 hybrid-zone-minSamples1.0-mac3-popmap2 assign-popmap2-100 
./plot-hybrid-pca.py out-hybrid-zone-minSamples95-mac3-popmap3 hybrid-zone-minSamples95-mac3-popmap3 assign-popmap3-95 True
./plot-hybrid-pca.py out-hybrid-zone-minSamples1.0-mac3-popmap3 hybrid-zone-minSamples1.0-mac3-popmap3 assign-popmap3-100

```

