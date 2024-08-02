#!/usr/bin/env python

from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
import fire 

def filter(input, output, maxMissingPerSample=1.0, maxMissingPerSite=1.0, outFormat="phylip-relaxed"):
    ## maxMissingPerSample: maximum proportion of sites in a sample allowed to be "-" or "N"
    ##  default is 1.0 which will remove only samples that have only "-" or "N"
    ## maxMissingPerSite: maximum proportion of rows in a site allowed to be "-" or "N"
    ##  default is 1.0 which will remove only sites that have only "-" or "N"

    orig = AlignIO.read(open(input), "phylip-relaxed")
    origChars = orig.get_alignment_length()

    # Remove rows
    rowFiltered = MultipleSeqAlignment([])
    removedIds = []
    for record in orig:
        missing = record.seq.count("N") + record.seq.count("-")
        propMissing = missing / origChars 
        if propMissing < maxMissingPerSample:
            rowFiltered.extend([record])
        else:
            removedIds.append(record.id)
    
    # Remove columns
    removedColumns = []
    columnFiltered = rowFiltered 
    offset = 0
    for col in range(0, origChars):
        missing = rowFiltered[:,col].count('N') + rowFiltered[:,col].count('-')
        propMissing = missing / len(rowFiltered) 
        if propMissing >= maxMissingPerSite: 
            columnFiltered = columnFiltered[:,:col-offset] + columnFiltered[:, col-offset+1:]
            removedColumns.append(col)
            offset += 1
    
    if outFormat == "nexus": 
        for record in columnFiltered:
            record.annotations["molecule_type"] = "DNA"

    # Save output
    AlignIO.write(columnFiltered, open(output, "w"), outFormat)

    # Print outcome
    if removedIds:
        for i in removedIds:
            print("{} removed".format(i))
    if removedColumns:
        print("Removed columns {}".format(removedColumns))

    for i in range(0, columnFiltered.get_alignment_length()):
        chars = set(columnFiltered[:,i])
        if chars == set(['N', '-']):
            print("Site {} has only {}".format(i, chars))
        elif len(chars) == 1:
            print("Site {} has only {}".format(i, chars))


if __name__ == "__main__":
    fire.Fire(filter)