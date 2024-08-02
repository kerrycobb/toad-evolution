# Structure

## Clust-90-missing-0.9-exclude-1
Dropped individuals with more than 25% missing data initially. 
Max % missing after filtering is individuals was 35%. Filtered individuals 
are in exclude-missing-data-clust-90-missing-0.9-exclude-1.txt
```bash

# Call from within output directory
../prepare_data.fish \
  ~/scratch/anaxyrus/pyrad/clust-90-defaults_outfiles/clust-90-defaults.vcf \
  0.9 \
  exclude-missing-data-clust-90-missing-0.9-exclude-1.txt \
  clust-90-missing-0.9-exclude-1

cd ..

./run-structure.fish clust-90-missing-0.9-exclude-1 2,3,4 20 


```


## Clust-90-missing-0.75-exclude-1
Dropped individuals with more than 25% missing data initially. 
Max % missing after filtering is individuals was 39%. Filtered individuals 
are in exclude-missing-data-clust-90-missing-0.75-exclude-1.txt
```bash

# Call from within output directory
../prepare_data.fish \
  ~/scratch/anaxyrus/pyrad/clust-90-defaults_outfiles/clust-90-defaults.vcf \
  0.75 \
  exclude-missing-data-clust-90-missing-0.75-exclude-1.txt \
  clust-90-missing-0.75-exclude-1

cd ..

./run-structure.fish clust-90-missing-0.75-exclude-1 2,3,4 20 


```



## Clust-85-missing-0.9-exclude-1
Dropped individuals with more than 25% missing data initially. 
Max % missing after filtering is individuals was 35%. Filtered individuals 
are in exclude-missing-data-clust-85-missing-0.9-exclude-1.txt
```bash

# Call from within output directory
../prepare_data.fish \
  ~/scratch/anaxyrus/pyrad/clust-85-defaults_outfiles/clust-85-defaults.vcf \
  0.9 \
  exclude-missing-data-clust-85-missing-0.9-exclude-1.txt \
  clust-80-missing-0.9-exclude-1

cd ..

./run-structure.fish clust-80-missing-0.9-exclude-1 2,3,4 20 
```


## Clust-80-missing-0.9-exclude-1
Dropped individuals with more than 25% missing data initially. 
Max % missing after filtering is individuals was 35%. Filtered individuals 
are in exclude-missing-data-clust-80-missing-0.9-exclude-1.txt
```bash

# Call from within output directory
../prepare_data.fish \
  ~/scratch/anaxyrus/pyrad/clust-80-defaults_outfiles/clust-80-defaults.vcf \
  0.9 \
  exclude-missing-data-clust-80-missing-0.9-exclude-1.txt \
  clust-80-missing-0.9-exclude-1

cd ..

./run-structure.fish clust-80-missing-0.9-exclude-1 2,3,4 20 
```