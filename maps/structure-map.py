#!/usr/bin/env python

import fire 
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy import feature
# from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
# import cartopy.mpl.ticker as cticker
# import matplotlib.ticker as mticker
import seaborn as sns
# import numpy as np
# import math
# import cartopy.io.shapereader as shpreader
# from metpy.plots import USCOUNTIES
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# from matplotlib.patches import Patch
import matplotlib.patches as mpatches
# from matplotlib_scalebar.scalebar import ScaleBar

colorPath = "../colors.txt"
qmatPath = "../structure/qmats/"
outDir = "out/"
radius = 0.15

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

# def draw_pie(props, xpos, ypos, size, colors, ax):
#     cumsum = np.cumsum(props)
#     cumsum = cumsum / cumsum[-1]
#     pie = [0] + cumsum.tolist()
#     for i, (r1, r2) in enumerate(zip(pie[:-1], pie[1:])):
#         angles = np.linspace(2 * np.pi * r1, 2 * np.pi * r2)
#         x = [0] + np.cos(angles).tolist()
#         y = [0] + np.sin(angles).tolist()
#         xy = np.column_stack([x, y])
#         ax.scatter([xpos], [ypos], marker=xy, s=size, color=colors[i], alpha=1, 
#                    transform=ccrs.Geodetic(), zorder=100)

def map(name, extent=None, counties=False, rivers=False, title=None, legend=False, labels=None):
    ## Extent: x0, x1, y0, y1 
    data = pd.read_csv("../sample-data.csv")
    data.drop_duplicates(subset="sample_id", inplace=True)
    qmat = pd.read_csv(qmatPath + name +".csv", index_col=0)
    merged = qmat.merge(data[["sample_id", "latitude", "longitude"]], left_index=True, 
        right_on="sample_id") 
    k = len(qmat.columns)
    colors = [line.rstrip('\n') for line in open(colorPath)]

    lon0, lat0 = get_midpoint(merged["longitude"], merged["latitude"])
    proj = ccrs.Orthographic(lon0, lat0)
    # proj = ccrs.LambertConformal(lon0, lat0)
    # # proj = ccrs.PlateCarree()
    # # proj = ccrs.Robinson()

    borderColor = rgb(200, 200, 200)
    landColor = rgb(245, 245, 223)
    waterColor = rgb(218, 228, 237)

    fig = plt.figure()
    ax = plt.axes(projection=proj)
    ax.add_feature(feature.OCEAN, linewidth=0, facecolor=waterColor, 
                   edgecolor=waterColor, zorder=10)
    ax.add_feature(feature.LAND, linewidth=0, facecolor=landColor, 
                   edgecolor=landColor, zorder=11)
    if rivers:
        ax.add_feature(feature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '50m'),
                linewidth=1.5, facecolor="None", edgecolor=waterColor, zorder=22)
        # ax.add_feature(feature.RIVERS, linewidth=1.5, facecolor=waterColor, 
                    #    edgecolor=waterColor, zorder=22)
    ax.add_feature(feature.LAKES, linewidth=0, facecolor=waterColor, 
                   edgecolor=waterColor, zorder=13)
    # # ax.add_feature(feature.BORDERS, linewidth=1, edgecolor=borderColor, zorder=22)
    ax.add_feature(feature.STATES, linewidth=0.2, edgecolor=borderColor, zorder=21)
    # if counties:
    #     ax.add_feature(USCOUNTIES.with_scale("20m"), linewidth=0.1, 
    #                    edgecolor=borderColor, zorder=20)
    if extent:
        # ax.set_extent([float(x.strip()) for x in extent.split(",")])
        # ax.set_extent(extent)
        ax.set_extent(extent)

    for ix, row in merged.iterrows():
        props = row[0:k].to_list()
        lonT, latT = proj.transform_point(row["longitude"], row["latitude"], ccrs.PlateCarree())
        # draw_pie(props, row["longitude"], row["latitude"], 200, colors, ax)
        ax_sub = inset_axes(ax, width=radius, height=radius, 
                bbox_to_anchor=(lonT, latT),
                bbox_transform=ax.transData,
                borderpad=0, loc=10)
        ax_sub.pie([1], radius=1, colors=["black"]) # Hack to creat black border
        ax_sub.pie(props, radius=1 - 0.01, colors=colors)
        ax_sub.set_aspect("equal")
        ax.scatter(row["longitude"], row["latitude"], alpha=0, transform=ccrs.Geodetic())
    
    # if title:
    #     plt.title(title)

    # if legend:
    #     if labels:
    #         legLabels = labels.split(",")
    #     else:
    #         legLabels = qmat.columns[i]
    #     legendElements = [] 
    #     for i in range(k):
    #         legendElements.append(mpatches.Patch(
    #             facecolor="blue", edgecolor="black", label=legLabels
    #         ))
    
    #     ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    #     ax.legend(handles=legendElements)

    outPath = outDir + "structure-" + name + ".pdf" 
    # plt.savefig(outPath, transparent=True, bbox_inches='tight', pad_inches=0)
    # plt.savefig(outPath, pad_inches=0)
    plt.savefig(outPath)
    print(f"Plot output to {outPath}")
    cropPath = outPath + "-cropped"
    subprocess.run(f"pdfcrop {outPath} {cropPath}", shell=True)
    subprocess.run(f"mv {cropPath} {outPath}", shell=True)
    # plt.show()

if __name__ == "__main__":
    fire.Fire(map)


# import cartopy.crs as ccrs
# import matplotlib.pyplot as plt
# from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# ax = plt.axes(projection=ccrs.Robinson())
# ax.coastlines(resolution='110m')
# ax.stock_img() 


# def plot_pie_inset(data,ilon,ilat,ax,width):
#     ax_sub= inset_axes(ax, width=width, height=width, loc=10, 
#                        bbox_to_anchor=(ilon, ilat),
#                        bbox_transform=ax.transData, 
#                        borderpad=0)
#     wedges,texts= ax_sub.pie(data)

#     ax_sub.set_aspect("equal")

# lon,lat = 90,30
# lonr,latr =  ccrs.Robinson().transform_point(lon,lat, ccrs.PlateCarree())
# plot_pie_inset([0.25, 0.75],lonr,latr,ax,0.5)


# plt.show()