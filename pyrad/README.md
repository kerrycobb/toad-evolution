# ipyrad

## Demultiplex

```bash
for i in 1 2 3
  sbatch -J demux-toad-$i -o %x-%j.out --mail-type END \
     -t 1-00:00:00 -c 5 --mem 20G --partition jro0014_amd \
     --wrap "ipyrad -p params-toad-$i.txt -s 1 -c 5"
end
```

## Merge
```bash
set name c80-defaults
set dest "/home/kac0070/toad/pyrad"
set src $dest/toad-1
ipyrad -m $name params-toad-1.txt params-toad-2.txt params-toad-3.txt
mv $src/$name.json $dest
sed -i "s|project\":\"$src|project\":\"$dest|g" $dest/$name.json
sed -i "s|_project_dir\":\"$src|_project_dir\":\"$dest|g" $dest/$name.json
sed -i "s|$src|$dest|g" params-$name.txt
```

## Assemble
```bash
# 80 % Similarity clustering with defaults
sbatch -J c80-defaults -o %x-%j.out --mail-type END -t 6-00:00:00 -c 10 \
  --mem 50G --partition jro0014_amd \
  --wrap "ipyrad -p params-c80-defaults.txt -s 234567 -c 10"
```

## Filtering 

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
sbatch -J c80-s61-l200 -o %x-%j.out -t 2-00:00:00 \
  --mem 30G --partition jro0014_amd \
  --wrap "ipyrad -p params-c80-s61-l200.txt -s 7"
```

