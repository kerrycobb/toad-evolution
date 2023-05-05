#!/usr/bin/env python

## Renames some problematic sample names for running structure

import fire
import pandas as pd
import subprocess
import fileinput

sample_ids = [
    ("kac2018021701", "kac8021701"),
    ("kac2018021704", "kac8021704"),
    ("kac2018021705", "kac8021705"),
    ("kac2018021706", "kac8021706"),
    ("kac2018021707", "kac8021707"),
    ("kac201803101", "kac803101"),
    ("kac201803102", "kac803102"),
    ("kac201803103", "kac803103"),
    ("kac201803104", "kac803104"),
    ("kac201803105", "kac803105"),
    ("kac201808181", "kac808181"),
    ("kac201808182", "kac808182"),
    ("kac201808183", "kac808183"),
    ("kac201808184", "kac808184"),
    ("kac201908251", "kac908251"),
    ("kac201908252", "kac908252")]

def find_replace(file, reverse=False):
    with open(file, 'r') as f: 
        filedata = f.read()
        for ids in sample_ids:
            if reverse:
                filedata = filedata.replace(ids[1], ids[0])
            else:
                filedata = filedata.replace(ids[0], ids[1])
    with open(file, 'w') as f:
        f.write(filedata)

if __name__ == "__main__":
    fire.Fire(find_replace)      