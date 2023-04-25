#!/usr/bin/env python

import fire 
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy import feature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.mpl.ticker as cticker
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import math
import cartopy.io.shapereader as shpreader
from metpy.plots import USCOUNTIES

palette = sns.color_palette()
style = {
    'americanus': {"color": palette[0], "shape": "o", "order": 1},
    'terrestris': {"color": palette[1], "shape": "o", "order": 2},
    'fowleri': {"color": palette[2], "shape": "o", "order": 3},
    'woodhousii': {"color": palette[3], "shape": "o", "order": 4},
    'baxteri': {"color": palette[4], "shape": "o", "order": 5},
    'quercicus': {"color": palette[5], "shape": "o", "order": 6},
    'hemiophrys': {"color": palette[6], "shape": "o", "order": 7},
    'speciosus': {"color": palette[7], "shape": "o", "order": 8},
    'cognatus': {"color": palette[8], "shape": "o", "order": 9},
    'microscaphus': {"color": palette[9], "shape": "o", "order": 10},
    'debilis': {"color": palette[0], "shape": "o", "order": 11},
    'retiformis': {"color": palette[1], "shape": "v", "order": 12},
    'punctatus': {"color": palette[2], "shape": "v", "order": 13},
}

def get_midpoint(lons, lats):
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)
    lon0 = max_lon - ((max_lon - min_lon) / 2)
    lat0 = max_lat - ((max_lat - min_lat) / 2)
    return lon0, lat0 

def rgb(r, g, b):
    return (r/255, g/255, b/255) 

def map(popmap, outpath, extent=None, counties=False, rivers=False):
    popmapDf = pd.read_csv(popmap, sep='\t', header=None, names=["sample_id", "species"]) 
    popmapDf.drop_duplicates(subset="sample_id", inplace=True)
    popmapDf = popmapDf[~popmapDf["species"].isin(["nebulifer", "marina"])]
    dataDf = pd.read_csv("../sample-data.csv")
    dataDf.drop_duplicates(subset="sample_id", inplace=True)
    merged = popmapDf.merge(dataDf[["sample_id", "latitude", "longitude"]], on="sample_id") 

    lon0, lat0 = get_midpoint(merged["longitude"], merged["latitude"])
    
    proj = ccrs.Orthographic(lon0, lat0)
    # proj = ccrs.PlateCarree()

    borderColor = (0.6, 0.6, 0.6)
    landColor = rgb(236, 236, 213)
    waterColor = rgb(197, 213, 227)

    fig = plt.figure()
    ax = plt.axes(projection=proj)
    ax.add_feature(feature.LAND, linewidth=1, facecolor=landColor, edgecolor=landColor)
    ax.add_feature(feature.OCEAN, linewidth=1, facecolor=waterColor, edgecolor=waterColor)
    if rivers:
        ax.add_feature(feature.RIVERS, linewidth=1, facecolor=waterColor, edgecolor=waterColor)
    ax.add_feature(feature.LAKES, linewidth=1, facecolor=waterColor, edgecolor=waterColor)
    if counties:
        ax.add_feature(USCOUNTIES.with_scale("20m"), linewidth=0.1, edgecolor=borderColor)
    ax.add_feature(feature.STATES, linewidth=0.1, edgecolor=borderColor)
    # ax.add_feature(feature.BORDERS, linewidth=1, edgecolor=borderColor)

    # ax.gridlines(linewidth=0.25, color="gray", linestyle=(0, (10, 10)), alpha=1.0)
 
    if extent:
        ax.set_extent(extent)

    for sp, data in merged.groupby(by="species"):
        ax.scatter(data["longitude"], data["latitude"], 
            label=sp,
            transform=ccrs.Geodetic(), 
            color=style[sp]["color"],
            marker=style[sp]["shape"],
            zorder=style[sp]["order"],
            s=1) 

    # ax.scatter(lon0, lat0, transform=ccrs.Geodetic(),)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.title("Sampling Distribution")
    plt.savefig(outpath, transparent=True, bbox_inches='tight')
    # plt.show()



if __name__ == "__main__":
    fire.Fire(map)






# import pandas as pd
# import matplotlib.pyplot as plt
# from cartopy import crs
# # from cartopy.feature import ShapelyFeature, NaturalEarthFeature
# import cartopy.feature as cfeature
# import math
# import seaborn as sns
# import numpy as np

# def rgb(r, g, b):
#     return (r/255, g/255, b/255) 


# toadData = pd.read_csv("~/Desktop/toad-project/toad-data.csv")
# toadData = toadData[toadData["species"] != "?"]
# toadData = toadData[toadData["species"] != "fowleri / woodhousii intergrade"]
# toadData["species"] = toadData["species"].astype("category")
# colorMap = dict(zip(toadData["species"].cat.categories.tolist(), plt.cm.tab20.colors))

# # Read in data
# # weatherby_samples = pd.read_csv("weatherby-sites.csv")
# # my_samples = pd.read_csv("cobb-sites.csv")
# # fall_line = pd.read_csv("fall-line.csv")

# # Filter data
# # terr = my_samples[my_samples["species"] == "terrestris"]
# # amer = my_samples[my_samples["species"] == "americanus"]

# res = "50m"
# lineWidth = .5
# waterFaceColor = rgb(197, 213, 227)
# waterEdgeColor = rgb(88, 135, 155)
# borderColor = (0.6, 0.6, 0.6)
# extent = [-120.38896371457172, -67.05643017812572, 23.33769204708392, 49.75492690666086]

# proj = crs.Orthographic(central_longitude=-98.5795, central_latitude=36)
# transform = crs.Geodetic()


# # All species map
# plt.figure()
# ax = plt.axes(projection=proj)
# ax.add_feature(cfeature.STATES.with_scale(res), edgecolor=borderColor, linewidth=lineWidth, zorder=1)
# ax.add_feature(cfeature.OCEAN.with_scale(res), facecolor=waterFaceColor, edgecolor=waterEdgeColor, linewidth=lineWidth, zorder=2)
# ax.add_feature(cfeature.LAKES.with_scale(res), facecolor=waterFaceColor, edgecolor=waterEdgeColor, linewidth=lineWidth/2, zorder=2)
# for name, group in toadData.groupby("species"):
#     ax.scatter(group["longitude"], group["latitude"], label=name, transform=transform, color=colorMap[name], edgecolor="black", linewidth=0.3, s=15, zorder=100)
# # ax.scatter(midLon, midLat, s=100, color="black")

# # ax.gridlines(linewidth=0.25, color="gray", linestyle=(0, (10, 10)), alpha=1.0)
# ax.set_extent(extent)
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
# plt.title("Sampling Distribution")
# plt.savefig('sample-map.svg', transparent=True, bbox_inches='tight')


# # Single species maps
# for name, group in toadData.groupby("species"):
#     plt.figure()
#     ax = plt.axes(projection=proj)
#     ax.add_feature(cfeature.STATES.with_scale(res), edgecolor=borderColor, linewidth=lineWidth)
#     ax.add_feature(cfeature.OCEAN.with_scale(res), facecolor=waterFaceColor, edgecolor=waterEdgeColor, linewidth=lineWidth)
#     ax.add_feature(cfeature.LAKES.with_scale(res), facecolor=waterFaceColor, edgecolor=waterEdgeColor, linewidth=lineWidth)
#     ax.scatter(group["longitude"], group["latitude"], transform=transform, color=colorMap[name], edgecolor="black", linewidth=0.3, s=20, zorder=100)
#     ax.gridlines(linewidth=0.5, color="gray", linestyle='--', alpha=0.5)
#     ax.set_extent(extent)
#     plt.title("${}$ Sampling Distribution".format(name))
#     plt.savefig('species-sampling/{}.svg'.format(name), transparent=True, bbox_inches='tight')

