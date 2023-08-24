#!/usr/bin/env fish

set dir $argv[1]
set name (string trim --right --chars=/ $dir)

./bin/sumphycoeval -c 100  $name"/run-"*"-"$name"-trees-run-1.nex" > $name"/divergence-stats.tsv" 
