# Structure

## Hybrid zone

```bash
./run-structure.fish \
  out-hybrid-zone-minSamples1.0-mac3-popmap2 \
  ../stacks/out-hybrid-zone-M14-g7/out-minSamples1.0-mac3-popmap2-single-snp/populations.structure \
  1,2,3,4 10 

./run-structure.fish \
  out-hybrid-zone-minSamples95-mac3-popmap2 \
  ../stacks/out-hybrid-zone-M14-g7/out-minSamples95-mac3-popmap2-single-snp/populations.structure \
  1,2,3,4 10 

./run-structure.fish \
  out-hybrid-zone-minSamples1.0-mac3-popmap3 \
  ../stacks/out-hybrid-zone-M14-g7/out-minSamples1.0-mac3-popmap3-single-snp/populations.structure \
  1,2,3,4 10 

./run-structure.fish \
  out-hybrid-zone-minSamples95-mac3-popmap3 \
  ../stacks/out-hybrid-zone-M14-g7/out-minSamples95-mac3-popmap3-single-snp/populations.structure \
  1,2,3,4 10 
```

## Americanus Group 
```bash

./run-structure.fish \
  out-americanus-group-minSamples1.0-mac3-popmap2 \
  ../stacks/out-americanus-group-M14-g7/out-minSamples1.0-mac3-popmap2/populations.structure \
  1,2,3,4,5,6 10 

./run-structure.fish \
  out-americanus-group-minSamples95-mac3-popmap2 \
  ../stacks/out-americanus-group-M14-g7/out-minSamples95-mac3-popmap2/populations.structure \
  1,2,3,4,5,6 10 

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

## Fetch Structure Results
```bash
./fetch.fish out-americanus-group-minSamples1.0-mac3-popmap2/
./fetch.fish out-americanus-group-minSamples95-mac3-popmap2/

./fetch.fish out-americanus-minSamples1.0-mac3-popmap2
./fetch.fish out-americanus-minSamples99-mac3-popmap3

./fetch.fish out-fowleri-minSamples1.0-mac3-popmap2 
./fetch.fish out-fowleri-minSamples95-mac3-popmap2

./fetch.fish out-terrestris-minSamples1.0-mac3-popmap2
./fetch.fish out-terrestris-minSamples1.0-mac3-popmap3

./fetch.fish out-woodhousii-minSamples80-mac3
./fetch.fish out-woodhousii-minSamples80-mac3-popmap2
./fetch.fish out-woodhousii-minSamples1.0-mac3-popmap3

./fetch.fish out-hybrid-zone-minSamples1.0-mac3-popmap2
./fetch.fish out-hybrid-zone-minSamples95-mac3-popmap2
./fetch.fish out-hybrid-zone-minSamples1.0-mac3-popmap3
./fetch.fish out-hybrid-zone-minSamples95-mac3-popmap3

```




## Plot Structure

```bash
#### Americanus Group  
./plot-structure.R out-americanus-group-minSamples1.0-mac3-popmap2 --showindlabel
./plot-structure.R out-americanus-group-minSamples1.0-mac3-popmap2 -k 4 -p ../popmap-americanus-group-2.txt --showindlabel
  
./plot-structure.R out-americanus-group-minSamples95-mac3-popmap2 --showindlabel
./plot-structure.R out-americanus-group-minSamples95-mac3-popmap2 -k 4 -p ../popmap-americanus-group-2.txt --showindlabel
  
#### Americanus
./plot-structure.R out-americanus-minSamples1.0-mac3-popmap2 --showindlabel
./plot-structure.R out-americanus-minSamples1.0-mac3-popmap2 -k 2
./plot-structure.R out-americanus-minSamples1.0-mac3-popmap2 -k 3
./plot-structure.R out-americanus-minSamples1.0-mac3-popmap2 -k 4

./plot-structure.R out-americanus-minSamples99-mac3-popmap3 --showindlabel
./plot-structure.R out-americanus-minSamples99-mac3-popmap3 -k 2
./plot-structure.R out-americanus-minSamples99-mac3-popmap3 -k 3
./plot-structure.R out-americanus-minSamples99-mac3-popmap3 -k 4

#### Fowleri
./plot-structure.R out-fowleri-minSamples1.0-mac3-popmap2 --showindlabel
./plot-structure.R out-fowleri-minSamples1.0-mac3-popmap2 -k 2
./plot-structure.R out-fowleri-minSamples1.0-mac3-popmap2 -k 3
./plot-structure.R out-fowleri-minSamples1.0-mac3-popmap2 -k 4

./plot-structure.R out-fowleri-minSamples95-mac3-popmap2 --showindlabel
./plot-structure.R out-fowleri-minSamples95-mac3-popmap2 -k 2
./plot-structure.R out-fowleri-minSamples95-mac3-popmap2 -k 3
./plot-structure.R out-fowleri-minSamples95-mac3-popmap2 -k 4


#### Terrestris
./plot-structure.R out-terrestris-minSamples1.0-mac3-popmap2 --showindlabel
./plot-structure.R out-terrestris-minSamples1.0-mac3-popmap2 -k 2
./plot-structure.R out-terrestris-minSamples1.0-mac3-popmap2 -k 3 
./plot-structure.R out-terrestris-minSamples1.0-mac3-popmap2 -k 4 

./plot-structure.R out-terrestris-minSamples1.0-mac3-popmap3 --showindlabel
./plot-structure.R out-terrestris-minSamples1.0-mac3-popmap3 -k 2
./plot-structure.R out-terrestris-minSamples1.0-mac3-popmap3 -k 3 
./plot-structure.R out-terrestris-minSamples1.0-mac3-popmap3 -k 4 

#### Woodhousii
./plot-structure.R out-woodhousii-minSamples80-mac3 --showindlabel
./plot-structure.R out-woodhousii-minSamples80-mac3 -k 2
./plot-structure.R out-woodhousii-minSamples80-mac3 -k 3
./plot-structure.R out-woodhousii-minSamples80-mac3 -k 4

./plot-structure.R out-woodhousii-minSamples80-mac3-popmap2 --showindlabel
./plot-structure.R out-woodhousii-minSamples80-mac3-popmap2 -k 2
./plot-structure.R out-woodhousii-minSamples80-mac3-popmap2 -k 3

#### Hybrid Zone
./plot-structure.R out-hybrid-zone-minSamples1.0-mac3-popmap2 -c ../colors-hybrid.txt --showindlabel
./plot-structure.R out-hybrid-zone-minSamples1.0-mac3-popmap2 -c ../colors-hybrid.txt -k 2 --showindlabel

./plot-structure.R out-hybrid-zone-minSamples95-mac3-popmap2 -c ../colors-hybrid.txt --showindlabel
./plot-structure.R out-hybrid-zone-minSamples95-mac3-popmap2 -c ../colors-hybrid.txt -k 2 --showindlabel

./plot-structure.R out-hybrid-zone-minSamples1.0-mac3-popmap3 -c ../colors-hybrid.txt --showindlabel
./plot-structure.R out-hybrid-zone-minSamples1.0-mac3-popmap3 -c ../colors-hybrid.txt -k 2 --showindlabel

./plot-structure.R out-hybrid-zone-minSamples95-mac3-popmap3 -c ../colors-hybrid.txt --showindlabel
./plot-structure.R out-hybrid-zone-minSamples95-mac3-popmap3 -c ../colors-hybrid.txt -k 2 --showindlabel

```