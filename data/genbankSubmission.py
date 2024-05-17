import pandas as pd

def makeTable(df, path):
    print(f"Outputing {len(df)} samples into {path}")
    d = pd.DataFrame()
    # Sample Metadata
    d["*sample_name"] = df["id"]
    d["*organism"] = df["genus"] + " " + df["species"]
    d["breed"] = "Not Applicable"
    d["dev_stage"] = "Adult"
    d["*collection_date"] = "2022-06"
    d["*geo_loc_name"] = "USA"
    d["*sex"] = "not provided"
    d["*tissue"] = "Liver"
    d["collected_by"] = "Kerry Cobb"
    d["specimen_voucher"] = df["id"]
    d["lat_lon"] = df["latitude"].astype(str) + " N " + df["longitude"].astype(str).str.lstrip("-") + " W" 

    # Library Metadata
    d["library_ID"] = df["id"]
    d["title"] = "ddRADseq from Anaxyrus americanus and A. terrestris hybrid zone" 
    d["library_strategy"] = "RAD-Seq"
    d["library_source"] = "GENOMIC"
    d["library_selection"] = "Restriction Digest"
    d["library_layout"] = "paired"
    d["platform"] = "ILLUMINA"
    d["instrument_model"] = "Illumina HiSeq X"
    d["design_description"] = "Double digest RADseq library prepared using 2RAD method"
    d["filetype"] = "fastq"
    d["filename"] = df["sample_id"] + ".1.fq.gz"
    d["filename2"] = df["sample_id"] + ".2.fq.gz"

    d.to_csv(path, sep="\t", index=False)


df = pd.read_csv("sample-data.csv")
df.drop_duplicates(subset=["sample_id"], inplace=True)
df['id'].fillna(df['sample_id'], inplace=True)

makeTable(df[(df["hyb-zone"] == 'X') | (df["phylo"] == 'X')], "genbank-submission-file.tsv")

# makeTable(
#     df[df["hyb-zone"] == 'X'],
#     "genbank-hybrid-zone.tsv")

# makeTable(
#     df[df["phylo"] == 'X'],
#     "genbank-phylo.tsv")


