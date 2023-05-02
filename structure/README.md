# Structure

## Hybrid zone

```bash
# ./prepare_data.fish \
#   ../stacks/out-hybrid-zone-M14-g7/out- \
#   ../popmap-hybrid-zone.txt \
#   out-hybrid-zone-M14-g7-sites.75-indiv.75 \
#   0.75

```

## Americanus 

```bash

./run-structure.fish \
  out-americanus-minSamples1.0-mac3-popmap2 \
  ../stacks/out-americanus-M7-g7/out-minSamples1.0-mac3-popmap2/populations.structure \
  1,2,3,4,5 10 

./run-structure.fish \
  out-americanus-minSamples99-mac3-popmap3 \
  ../stacks/out-americanus-M7-g7/out-minSamples99-mac3-popmap3/populations.structure \
  1,2,3,4,5 10 

```

## Fowleri 

```bash

./run-structure.fish \
  out-fowleri-minSamples1.0-mac3-popmap2 \
  ../stacks/out-fowleri-M7-g7/out-minSamples1.0-mac3-popmap2/populations.structure \
  1,2,3,4,5 10 

./run-structure.fish \
  out-fowleri-minSamples95-mac3-popmap2 \
  ../stacks/out-fowleri-M7-g7/out-minSamples95-mac3-popmap2/populations.structure \
  1,2,3,4,5 10 

```

## Terrestris

```bash

./run-structure.fish \
  out-terrestris-minSamples1.0-mac3-popmap2 \
  ../stacks/out-terrestris-M7-g7/out-minSamples1.0-mac3-popmap2/populations.structure \
  1,2,3,4,5 10 

./run-structure.fish \
  out-terrestris-minSamples1.0-mac3-popmap3 \
  ../stacks/out-terrestris-M7-g7/out-minSamples1.0-mac3-popmap3/populations.structure \
  1,2,3,4,5 10 

```

## Woodhousii

```bash

./run-structure.fish \
  out-woodhousii-minSamples80-mac3 \
  ../stacks/out-woodhousii-M7-g7/out-minSamples80-mac3/populations.structure \
  1,2,3,4,5 10 

  ./run-structure.fish \
  out-woodhousii-minSamples80-mac3-popmap2 \
  ../stacks/out-woodhousii-M7-g7/out-minSamples80-mac3-popmap2/populations.structure \
  1,2,3,4,5 10 

./run-structure.fish \
  out-woodhousii-minSamples1.0-mac3-popmap3 \
  ../stacks/out-woodhousii-M7-g7/out-minSamples1.0-mac3-popmap3/populations.structure \
  1,2,3,4,5 10 

```





## Fetch remote output files for use locally

```bash
./fetch.fish out-americanus-minSamples1.0-mac3-popmap2
./fetch.fish out-americanus-minSamples99-mac3-popmap3

./fetch.fish out-fowleri-minSamples1.0-mac3-popmap2 
./fetch.fish out-fowleri-minSamples95-mac3-popmap2

./fetch.fish out-terrestris-minSamples1.0-mac3-popmap2
./fetch.fish out-terrestris-minSamples1.0-mac3-popmap3

./fetch.fish out-woodhousii-minSamples80-mac3
./fetch.fish out-woodhousii-minSamples80-mac3-popmap2
./fetch.fish out-woodhousii-minSamples1.0-mac3-popmap3

```