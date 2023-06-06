#!/usr/bin/env fish

set name $argv[1]

mkdir $name

scp -r "kac0070@easley.auburn.edu:toad/structure/"$name"/populations.structure" $name/$name.stru 



# set dir $argv[1]
# set alignment $argv[2]
# set outdir out-$dir-$alignment

# mkdir $outdir

# scp -r "kac0070@easley.auburn.edu:toad/stacks/out-$dir/out-$alignment/populations.snps.vcf" $outdir/populations.snps.vcf 