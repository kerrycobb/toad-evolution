import pandas as pd

data = pd.read_csv("../sample-data.csv")
all = pd.read_csv("../popmap-all.txt", sep='\t', header=None)
all2_l200 = pd.read_csv("../popmap-all-2-l200.txt", sep='\t', header=None)
phyco = pd.read_csv("../phycoeval-samples.txt", sep='\t', header=None)
amer = pd.read_csv("../popmap-americanus-3.txt", sep='\t', header=None)
fowl = pd.read_csv("../popmap-fowleri-2.txt", sep='\t', header=None)
terr = pd.read_csv("../popmap-terrestris-3.txt", sep='\t', header=None)
wood = pd.read_csv("../popmap-woodhousii-3.txt", sep='\t', header=None)

data["proj_id"] = data["proj_id"].str[1:]
data = data.rename(columns={
    "id": "Sample ID",
    "species": "Species", 
    "latitude": "Latitude",
    "longitude": "Longitude"})

df = data[data["sample_id"].isin(all[0])].copy()
df["Passed Filters"] = " "
df["Phycoeval"] = " "
df["Structure"] = " "
df.loc[df["sample_id"].isin(all2_l200[0]), "Passed Filters"] = "X"
df.loc[df["sample_id"].isin(phyco[0]), "Phycoeval"] = "X"
df.loc[df["sample_id"].isin(amer[0]), "Structure"] = "X"
df.loc[df["sample_id"].isin(fowl[0]), "Structure"] = "X"
df.loc[df["sample_id"].isin(terr[0]), "Structure"] = "X"
df.loc[df["sample_id"].isin(wood[0]), "Structure"] = "X"

df["Latitude"] = df["Latitude"].apply(lambda x: '{0:.5f}'.format(x))
df["Longitude"] = df["Longitude"].apply(lambda x: '{0:.5f}'.format(x))
df.reset_index(inplace=True)
last_ix = len(df) - 1
with open("phylo-chapter-sample-table.tex", "w") as fh:
    for ix, row in df.iterrows():
        fh.write("{} & {} & \\textit{{{}}} & {} & {} & {} & {} & {}".format(
            row["proj_id"],
            row["Sample ID"], 
            row["Species"], 
            row["Latitude"], 
            row["Longitude"],
            row["Passed Filters"],
            row["Phycoeval"],
            row["Structure"]
            ))
        if ix < last_ix:
            fh.write(" \\\\ \n")

# print(df["Passed Filters"])
# def make_latex(prefix, group, df):
#     df.reset_index(inplace=True)
#     df = df.sort_values("Sample ID")
#     df["Latitude"] = df["Latitude"].apply(lambda x: '{0:.5f}'.format(x))
#     df["Longitude"] = df["Longitude"].apply(lambda x: '{0:.5f}'.format(x))
#     last_ix = len(df) - 1
#     with open(f"{prefix}-{group}.tex", "w") as fh:
#         for ix, row in df.iterrows():
#             if row["Passed Filtering"]:
#                 passed_filter = "X"
#             else:
#                 passed_filter = " "
#             fh.write("{} & \\textit{{{}}} & {} & {} & {}".format(
#                 row["Sample ID"], 
#                 row["Species"], 
#                 row["Latitude"], 
#                 row["Longitude"],
#                 passed_filter))
#             if ix < last_ix:
#                 fh.write(" \\\\ \n")