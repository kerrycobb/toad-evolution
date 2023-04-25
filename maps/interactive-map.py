#!/usr/bin/env python

import pandas as pd
import folium
from folium.plugins import MarkerCluster
import fire

colors = {
    "americanus": "red",
    "terrestris": "blue",
    "quercicus": "gray",
    "fowleri": "orange",
    "woodhousii": "gray",
    "speciosus": "beige",
    "punctatus": "green",
    "microscaphus": "darkblue",
    "cognatus": "black",
    "hemiophrys": "lightblue",
    "baxteri": "darkpurple",
    "debilis": "pink",
    "retiformis": "lightgreen",
    "fowleri_woodhousii_intergrade": "black"}

# def filter(df, path, oper):
#     ids = []
#     with open(path) as fh:
#         for line in fh:
#             line = line.strip()
#             if not line.startswith("#") and not line.isspace():
#                 ids.append(line)
#                 if not line in df["sample_id2"].values:
#                     quit("Error!: {} not a valid sampled id".format(line))
#     series = pd.Series(ids)
#     if oper == "in":
#         return df[df["sample_id2"].isin(series)]
#     elif oper == "not":
#         return df[~df["sample_id2"].isin(series)]


# def map(output, data, include=None, exclude=None):
#     df = pd.read_csv(data)
#     df = df.dropna(subset=["latitude", "longitude"])
#     if include and exclude:
#         quit("Can't have both include and exclude")
#     if include:
#         df = filter(df, include, "in") 
#     if exclude:
#         df = filter(df, exclude, "not") 

def map(popmap, outpath, extent=None, counties=False, rivers=False):
    popmapDf = pd.read_csv(popmap, sep='\t', header=None, names=["sample_id", "species"]) 
    popmapDf.drop_duplicates(subset="sample_id", inplace=True)
    popmapDf = popmapDf[~popmapDf["species"].isin(["nebulifer", "marina"])]
    dataDf = pd.read_csv("../sample-data.csv")
    dataDf.drop_duplicates(subset="sample_id", inplace=True)
    merged = popmapDf.merge(dataDf[["sample_id", "latitude", "longitude"]], on="sample_id") 

    m = folium.Map(tiles="Stamen Terrain")
    tot = 0
    for sp, data in merged.groupby(by="species"):
        tot += len(data)
        print("{}: {}".format(sp, len(data)))
        # feature_group = folium.FeatureGroup(name=name).add_to(m)
        feature_group = MarkerCluster(name=sp).add_to(m)
        for ix, row  in data.iterrows():
            feature_group.add_child(folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=folium.Popup(
                    "{}<br>{}".format(row["species"], row["sample_id"]),
                    max_width=200),
                icon=folium.Icon(color=colors[sp])))

    m.fit_bounds(m.get_bounds())
    folium.LayerControl().add_to(m)
    m.save(outpath)
    print("Total: {}".format(tot))


if "__main__" == __name__:
    fire.Fire(map)