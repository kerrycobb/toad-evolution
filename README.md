# Toad Evolution

This repository has the scripts used to process and analyze 3RAD data collected
to study phylogeography and hybridization in North American toads.

Below is a brief explanation of the contents of this repository. Each directory
contains an additional README with more extensive details.

## raw-data/ 
Scripts and index sequences for demultiplexing the i7-indexes in the raw data 
are in the `raw-data/` directory.

## stacks/ 
Scripts and barcode sequences for demultiplexing individual samples and 
de novo assembling reads into alignments. 

## iqtree/

## structure/

## phycoeval/

## dsuite/

## scripts/
Some scripts that are used throughout the project and are not specific for 
any one analysis.

## sample-data-phyl.csv
Collecting and wetlab data associated with each sample used in the phylogeography study. 

## sample-data-hyb.csv
Collecting and wetlab data associated with each sample used in the hybridization study. 

## Popmaps
### popmap-all-2.txt
Includes americanus-popmap3, fowleri-popmap2, terrestris-popmap3, and woodhousii-popmap3 samples

### popmap-all-2-l200.txt
Same as popmap-all-2.txt but excluding samples with less than 200 loci.