# ipyrad

## Demultiplex

```bash
for i in 1 2 3
  sbatch -J demux-toad-$i -o %x-%j.out --mail-type END \
     -t 1-00:00:00 -c 5 --mem 20G --partition jro0014_amd \
     --wrap "ipyrad -p params-toad-$i.txt -s 1 -c 5"
  sleep 10 
end
```

## Merge
```bash
ipyrad -m merged params-toad-1.txt params-toad-2.txt params-toad-3.txt 
```

## Branch and drop unneeded samples
```bash
ipyrad -p params-merged.txt -b all-subset-c80 ../popmap-all-subset.txt
ipyrad -p params-merged.txt -b all-c80 ../popmap-all.txt
ipyrad -p params-merged.txt -b all-subset-c80-s28 ../popmap-all-subset.txt
ipyrad -p params-merged.txt -b all-subset-c80-s42 ../popmap-all-subset.txt
ipyrad -p params-merged.txt -b all-2-c80-s78 ../popmap-all-2.txt
ipyrad -p params-merged.txt -b all-2-l200-c80-s73 ../popmap-all-2-l200.txt
```

Edit params files 

<!-- ```bash
set name c80-defaults
set dest "/home/kac0070/toad/pyrad"
set src $dest/toad-1
ipyrad -m $name params-toad-1.txt params-toad-2.txt params-toad-3.txt
mv $src/$name.json $dest
sed -i "s|project\":\"$src|project\":\"$dest|g" $dest/$name.json
sed -i "s|_project_dir\":\"$src|_project_dir\":\"$dest|g" $dest/$name.json
sed -i "s|$src|$dest|g" params-$name.txt
``` -->

## Assemble
```bash
# 80 % Similarity clustering with defaults
sbatch -J c80-defaults-all -o %x-%j.out --mail-type END -t 6-00:00:00 -c 10 \
  --mem 50G --partition jro0014_amd \
  --wrap "ipyrad -p params-all-c80.txt -s 234567 -c 10"
```

```bash
sbatch -J c80-defaults-subset -o %x-%j.out --mail-type END -t 6-00:00:00 -c 10 \
  --mem 50G --partition jro0014_amd \
  --wrap "ipyrad -p params-all-subset-c80.txt -s 234567 -c 10"

sbatch -J c80-s28-subset -o %x-%j.out --mail-type END -t 6-00:00:00 -c 10 \
  --mem 50G --partition jro0014_amd \
  --wrap "ipyrad -p params-all-subset-c80-s28.txt -s 234567 -c 10"

sbatch -J c80-s42-subset -o %x-%j.out --mail-type END -t 6-00:00:00 -c 10 \
  --mem 50G --partition jro0014_amd \
  --wrap "ipyrad -p params-all-subset-c80-s42.txt -s 234567 -c 10"

sbatch -J c80-s78-all-2 -o %x-%j.out --mail-type END -t 6-00:00:00 -c 10 \
  --mem 50G --partition jro0014_amd \
  --wrap "ipyrad -p params-all-2-c80-s78.txt -s 234567 -c 10"

# Filter individuals with less than 200 loci and loci not found in at least 75% of individuals (73)
sbatch -J all-2-l200-c80-s73 -o %x-%j.out --mail-type END -t 6-00:00:00 -c 10 \
  --mem 50G --partition jro0014_amd \
  --wrap "ipyrad -p params-all-2-l200-c80-s73.txt -s 234567 -c 10"
```


## Filter Loci
#### Loci not present in 50% of samples
```bash
ipyrad -p params-all-c80.txt -b all-c80-s61
ipyrad -p params-all-subset-c80.txt -b all-subset-c80-s28

```


```bash
sbatch -J c80-all-s61 -o %x-%j.out -t 8:00:00 \
  --mem 50G --partition jro0014_amd \
  --wrap "ipyrad -p params-all-c80-s61.txt -s 7"

sbatch -J c80-all-subset-s28 -o %x-%j.out -t 8:00:00 \
  --mem 50G --partition jro0014_amd \
  --wrap "ipyrad -p params-all-subset-c80-s28.txt -s 7"
```


<!-- ## Filtering 

### c80-s61-l200
Filter loci found in less than half (61/121) samples.
```bash
ipyrad -p params-c80-defaults.txt -b c80-s61
```

Edit params file

```bash
sbatch -J c80-s61 -o %x-%j.out -t 2-00:00:00 \
  --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-c80-s61.txt -s 7"
```

### c80-s61-l200
Filter samples with fewer than 200 loci in c80-s61 alignment.
Identify samples in ipyrad stats output exclude them from samples-c80-s61-l200.txt 
```bash
ipyrad -p params-c80-defaults.txt -b c80-s61-l200.txt samples-c80-s61-l200.txt  
```

Edit params file

```bash
sbatch -J c80-s61-l200 -o %x-%j.out -t 2-00:00:00 \
  --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-c80-s61-l200.txt -s 7"
```
 -->
