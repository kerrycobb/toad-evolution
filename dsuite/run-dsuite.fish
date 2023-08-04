#!/usr/bin/env bash

NAME=$1
VCF=$2
TREE=$3
SETS=$4

cd $NAME
../Dsuite Dtrios -c -n $NAME -t ../$TREE $VCF $SETS
