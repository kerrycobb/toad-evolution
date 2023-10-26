#!/usr/bin/env python

import fire 
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import numpy as np
from metpy.plots import USSTATES, USCOUNTIES
import matplotlib.patches as mpatches
import shapely.geometry as sgeom
from shapely.geometry.point import Point
import geopandas as gpd
from matplotlib.patches import FancyBboxPatch
import subprocess

colorPath = "../colors-hybrid.txt"
outDir = "out/"

def rgb(r, g, b):
    return (r/255, g/255, b/255) 

colors = [line.rstrip('\n') for line in open(colorPath)]

proj = ccrs.Orthographic(-90,40)
# proj = ccrs.PlateCarree()

americanus_range = gpd.read_file("range-maps/americanus-great-lakes.geojson")
americanus_range.to_crs(proj.proj4_params, inplace=True)
terrestris_range = gpd.read_file("range-maps/terrestris.geojson")
terrestris_range.to_crs(proj.proj4_params, inplace=True)

# # Whole map
# fig = plt.figure()
# ax = plt.axes(projection=proj)

# ax.add_feature(cfeature.OCEAN)
# ax.add_feature(cfeature.LAND)
# ax.add_feature(cfeature.LAKES)
# ax.add_feature(cfeature.STATES, linewidth=0.4, 
#         edgecolor=rgb(120, 120, 120))
# americanus_range.plot(ax=ax, facecolor=colors[0], alpha=0.85, linewidth=0)
# terrestris_range.plot(ax=ax, facecolor=colors[1], alpha=0.85, linewidth=0)

# gl = ax.gridlines(draw_labels=False, linewidth=0.5, color='gray', alpha=1.0, 
#              linestyle=(0, (10, 5)))

# gl.xlocator = mticker.FixedLocator([-100, -90, -80, -70, -60])
# gl.ylocator = mticker.FixedLocator([20, 30, 40, 50, 60])

# outPath1 = outDir + "hybrid-zone1.pdf" 
# plt.savefig(outPath1)
# cropPath1 = outPath1 + "-cropped"
# subprocess.run(f"pdfcrop {outPath1} {cropPath1}", shell=True)
# subprocess.run(f"mv {cropPath1} {outPath1}", shell=True)


# # Zoomed 
# fig = plt.figure()
# ax = plt.axes(projection=proj)

# ax.add_feature(cfeature.OCEAN)
# ax.add_feature(cfeature.LAND)
# ax.add_feature(cfeature.LAKES)
# ax.add_feature(cfeature.STATES, linewidth=0.4, 
#         edgecolor=rgb(120, 120, 120))
# americanus_range.plot(ax=ax, facecolor=colors[0], alpha=0.85, linewidth=0)
# terrestris_range.plot(ax=ax, facecolor=colors[1], alpha=0.85, linewidth=0)

# ax.set_extent([-92.5,-77,25,38])

# outPath2 = outDir + "hybrid-zone2.pdf" 
# plt.savefig(outPath2)
# cropPath2 = outPath2 + "-cropped"
# subprocess.run(f"pdfcrop {outPath2} {cropPath2}", shell=True)
# subprocess.run(f"mv {cropPath2} {outPath2}", shell=True)


proj = ccrs.Orthographic(-86.91,32.71)
data = pd.read_csv("../sample-data.csv")
samples = pd.read_csv("../popmap-hybrid-zone.txt", sep='\t', header=None)
data = data[data["sample_id"].isin(samples[0])].drop_duplicates(subset="sample_id")
# print(len(data))

americanus_range = gpd.read_file("range-maps/americanus-great-lakes.geojson")
americanus_range.to_crs(proj.proj4_params, inplace=True)
terrestris_range = gpd.read_file("range-maps/terrestris.geojson")
terrestris_range.to_crs(proj.proj4_params, inplace=True)

fig = plt.figure()
ax = plt.axes(projection=proj)

ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.STATES, linewidth=0.4, 
        edgecolor=rgb(120, 120, 120))
americanus_range.plot(ax=ax, facecolor=colors[0], alpha=0.85, linewidth=0)
terrestris_range.plot(ax=ax, facecolor=colors[1], alpha=0.85, linewidth=0)

ax.scatter(data["longitude"], data["latitude"], 5, color="black", zorder=100, transform=ccrs.Geodetic())

ax.set_extent([-89.46,-84.36,30.33,35.09])

outPath3 = outDir + "hybrid-zone-samples.pdf" 
plt.savefig(outPath3)
cropPath3 = outPath3 + "-cropped"
subprocess.run(f"pdfcrop {outPath3} {cropPath3}", shell=True)
subprocess.run(f"mv {cropPath3} {outPath3}", shell=True)