#!/usr/bin/env bash

NAME=$1
VCF=$2
TREE=$3
SETS=$4

cd $NAME
sbatch -J dsuit-$NAME -o %x-%j.out -t 1:00:00 \
  --mem 20G --partition jro0014_amd \
  --wrap "../Dsuite Dtrios -c -n $NAME -o $NAME -t ../$TREE $VCF $SETS; ../Dsuite Fbranch ../$TREE $NAME_tree.txt > $NAME_Fbranch.txt; dtools.py $NAME_Fbranch.txt ../$TREE"