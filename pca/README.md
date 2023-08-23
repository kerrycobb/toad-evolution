
# Run PCA and plot

```bash

# Hybrid zone
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

# Phylogeny
./fetch.fish out-americanus-minSamples99-mac3-popmap3
./fetch.fish out-fowleri-minSamples1.0-mac3-popmap2
./fetch.fish out-terrestris-minSamples1.0-mac3-popmap3
./fetch.fish out-woodhousii-minSamples1.0-mac3-popmap3
./fetch.fish out-woodhousii-minSamples80-mac3-popmap2

./run-pca.r out-americanus-minSamples99-mac3-popmap3
./run-pca.r out-fowleri-minSamples1.0-mac3-popmap2
./run-pca.r out-terrestris-minSamples1.0-mac3-popmap3
./run-pca.r out-woodhousii-minSamples1.0-mac3-popmap3
./run-pca.r out-woodhousii-minSamples80-mac3-popmap2

./plot-pca.py out-americanus-minSamples99-mac3-popmap3 americanus-minSamples99-mac3-popmap3-K-3 
./plot-pca.py out-fowleri-minSamples1.0-mac3-popmap2 fowleri-minSamples1.0-mac3-popmap2-K-2
./plot-pca.py out-terrestris-minSamples1.0-mac3-popmap3 terrestris-minSamples1.0-mac3-popmap3-K-2
./plot-pca.py out-woodhousii-minSamples1.0-mac3-popmap3 woodhousii-minSamples1.0-mac3-popmap3-K-2
./plot-pca.py out-woodhousii-minSamples80-mac3-popmap2 woodhousii-minSamples80-mac3-popmap2-K-2

```

