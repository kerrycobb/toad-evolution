#!/usr/bin/env fish

set name (string trim --right --chars "/" $argv[1])
set popmap $argv[2]
set outName $argv[3]
set args $argv[4..]

set threads 8
set outpath $name/out-$outName

# Check if output already exists
if test -d $outpath 
    read -l -P "Output exists. Overwrite? [y/n]" confirm
    if test $confirm = "y" 
       rm -rf $outpath/* 
    else
        echo "Aborted"
        exit 0 
    end
else
  mkdir $outpath
end

# Create script for batch submission
set cmd \
"#!/usr/bin/env fish

populations \
  --in-path $name/stacks \
  --out-path $outpath \
  --threads $threads \
  --popmap $popmap \
  $args
"

# Execute batch submission
echo $cmd | sbatch \
  --job-name pop-$name-$outName \
  --output $outpath/%x-%j.out \
  --cpus-per-task $threads \
  --time 4:00:00 \
  --mem 10G \
  --partition jro0014_amd


