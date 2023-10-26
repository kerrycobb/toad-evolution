#!/usr/bin/env fish

set dir $argv[1]
set burn $arv[2]

set name (string trim --right --chars=/ $dir)

./bin/sumphycoeval -b=$burn --map-tree-out=$name/map-tree.nex $name/run-*-$name-trees-run-1.nex > $name/posterior-summary.yaml 