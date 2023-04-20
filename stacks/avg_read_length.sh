#!/bin/bash

# Check if the file exists and is a FASTQ or gzipped FASTQ file
if [ ! -f "$1" ] || ! [[ "$1" =~ \.(fastq|fq|fastq.gz|fq.gz)$ ]]; then
  echo "Usage: $0 <fastq_file>"
  exit 1
fi

# Determine if the file is gzipped
if [[ "$1" =~ \.(gz|gzip)$ ]]; then
  zcat "$1" | awk 'NR%4==2' > temp.seq
else
  awk 'NR%4==2' "$1" > temp.seq
fi

# Extract the sequence lines and count the number of lines
num_seqs=$(wc -l < temp.seq)

# Calculate the total length of all sequences
total_length=$(awk '{ sum += length } END { print sum }' temp.seq)

# Calculate the average length
avg_length=$((total_length / num_seqs))

echo "Average read length: $avg_length"

# Clean up temporary files
rm temp.seq