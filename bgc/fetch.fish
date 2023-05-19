#!/usr/bin/env fish

set name (string trim -r -c "/" $argv[1])

mkdir $name

scp -r "kac0070@easley.auburn.edu:toad/bgc/"$name"/*.hdf5" $name 
scp -r "kac0070@easley.auburn.edu:toad/bgc/"$name"/*.csv" $name 

