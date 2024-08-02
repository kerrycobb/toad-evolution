#!/usr/bin/env fish  

set plateNames $argv[1]
set outdir $argv[2]
set indirs $argv[3..-1]

for plate in (cat $plateNames)
  set plate (string trim $plate)
  for read in 1 2 
    for dir in $indirs
      for file in $dir/*$plate.$read.fq.gz
        set cmd "cat $file >> $outdir/$plate.$read.fq.gz"
        echo $cmd
        eval $cmd
      end
    end
  end
end
