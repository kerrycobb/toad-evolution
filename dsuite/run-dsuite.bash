#!/usr/bin/env bash

NAME=$1
VCF=$2
TREE=$3
SETS=$4

cd $NAME

CMD="../Dsuite Dtrios -c -o $NAME -t ../$TREE $VCF ../$SETS; ../Dsuite Fbranch ../$TREE ${NAME}_tree.txt > ${NAME}_Fbranch.txt; dtools.py ${NAME}_Fbranch.txt ../$TREE"

sbatch -J dsuit-$NAME -o %x-%j.out -t 1:00:00 \
  --mem 10G \
  --wrap "$CMD"