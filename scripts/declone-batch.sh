#!/usr/bin/env bash

NAME=$1
INDIR=$2
OUTDIR=$3

mkdir $OUTDIR/$NAME

sbatch \
  --job-name declone-$NAME  \
  --output $OUTDIR/%x-%j.out \
  --mail-type=END \
  --mail-user=kac0070@auburn.edu \
  --time=48:00:00 \
  --mem 80G \
  --partition jro0014_amd \
  declone.sh \
    $INDIR/$NAME/$NAME.1.fq.gz \
    $INDIR/$NAME/$NAME.2.fq.gz \
    $OUTDIR/$NAME