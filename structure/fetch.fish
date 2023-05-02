#!/usr/bin/env fish

set name $argv[1]

mkdir $name

scp -r "kac0070@easley.auburn.edu:toad/structure/"$name"/*.out_f" $name 

for i in (ls $name/*.out_f)
  ../scripts/find_replace.py $i
end