#!/usr/bin/env fish

set yaml $argv[1]
set name $argv[2]
set chains $argv[3]

set threads 10 

set outdir $name"/"
set inAlign $name".phy"
set pyradPath "/scratch/phyletica/anaxyrus/pyrad"
set inAlignPath $pyradPath"/"$name"_outfiles/"$inAlign
set filename $name".nex"
set filePath $outdir$filename
set yamlPath $outdir$name".yaml"

if test -d $outdir
  echo "Output directory already exists"
  exit 
else
  mkdir $outdir
end

sed "s/path\:/path\: $filename/" $yaml > $yamlPath
../scripts/toBiallelic -i $inAlignPath -o $filePath;
../scripts/find_replace.py $filePath;


for i in (seq 1 $chains)
  set seed (random)
  sbatch \
    --job-name phycoeval-$name"-run-"$i \
    --output $outdir%x-%j.out \
    --mail-type END \
    --partition jro0014_amd \
    --time 30-00:00:00 \
    --cpus-per-task $threads \
    --mem 10GB \
    --wrap "./bin/phycoeval --prefix $name"/run-"$i"-" --seed $seed --nthreads $threads --relax-missing-sites $yamlPath;"
end