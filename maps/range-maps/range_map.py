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

# colorPath = "../../colors-hybrid.txt"
colors = dict( 
    americanus="#b48e3c",
    baxteri="#f70511",
    fowleri="#c9783a",
    hemiophrys="#873e23",
    microscaphus="#64469B",
    terrestris="#3c425e",
    woodhousii="#1e81b0",
)

def rgb(r, g, b):
    return (r/255, g/255, b/255) 

proj = ccrs.Orthographic(-100,40)
# proj = ccrs.PlateCarree()

americanus_range = gpd.read_file("range-americanus.geojson")
americanus_range.to_crs(proj.proj4_params, inplace=True)

baxteri_range = gpd.read_file("range-baxteri.geojson")
baxteri_range.to_crs(proj.proj4_params, inplace=True)

fowleri_range = gpd.read_file("range-fowleri.geojson")
fowleri_range.to_crs(proj.proj4_params, inplace=True)

hemiophrys_range = gpd.read_file("range-hemiophrys.geojson")
hemiophrys_range.to_crs(proj.proj4_params, inplace=True)

microscaphus_range = gpd.read_file("range-microscaphus.geojson")
microscaphus_range.to_crs(proj.proj4_params, inplace=True)

terrestris_range = gpd.read_file("range-terrestris.geojson")
terrestris_range.to_crs(proj.proj4_params, inplace=True)

woodhousii_range = gpd.read_file("range-woodhousii.geojson")
woodhousii_range.to_crs(proj.proj4_params, inplace=True)


fig = plt.figure()
ax = plt.axes(projection=proj)

ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.LAND, facecolor="#eeeee4")
ax.add_feature(cfeature.LAKES)
ax.add_feature(cfeature.STATES, linewidth=0.2, edgecolor=rgb(0, 0, 0))
ax.add_feature(cfeature.COASTLINE, linewidth=0.2, edgecolor=rgb(0, 0, 0))

fowleri_range.plot(ax=ax, facecolor=colors["fowleri"], linewidth=0)
woodhousii_range.plot(ax=ax, facecolor=colors["woodhousii"], linewidth=0)

gl = ax.gridlines(draw_labels=False, linewidth=0.25, color='gray', alpha=1.0, 
             linestyle=(0, (10, 5)))
gl.xlocator = mticker.FixedLocator([-100, -90, -80, -70, -60])
gl.ylocator = mticker.FixedLocator([20, 30, 40, 50, 60])

outPath1 = "range-map-wood-fowl.pdf" 
plt.savefig(outPath1)
cropPath1 = outPath1 + "-cropped"
subprocess.run(f"pdfcrop {outPath1} {cropPath1}", shell=True)
subprocess.run(f"mv {cropPath1} {outPath1}", shell=True)
# plt.show()

fig = plt.figure()
ax = plt.axes(projection=proj)

ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.LAND, facecolor="#eeeee4")
ax.add_feature(cfeature.LAKES)
ax.add_feature(cfeature.STATES, linewidth=0.2, edgecolor=rgb(0, 0, 0))
ax.add_feature(cfeature.COASTLINE, linewidth=0.2, edgecolor=rgb(0, 0, 0))

americanus_range.plot(ax=ax, facecolor=colors["americanus"], linewidth=0)
baxteri_range.plot(ax=ax, facecolor=colors["baxteri"], linewidth=0)
hemiophrys_range.plot(ax=ax, facecolor=colors["hemiophrys"], alpha=0.65, linewidth=0)
microscaphus_range.plot(ax=ax, facecolor=colors["microscaphus"], linewidth=0)
terrestris_range.plot(ax=ax, facecolor=colors["terrestris"], linewidth=0)

gl = ax.gridlines(draw_labels=False, linewidth=0.25, color='gray', alpha=1.0, 
             linestyle=(0, (10, 5)))
gl.xlocator = mticker.FixedLocator([-100, -90, -80, -70, -60])
gl.ylocator = mticker.FixedLocator([20, 30, 40, 50, 60])

outPath2 = "range-map-amer-baxt-hemi-terr.pdf" 
plt.savefig(outPath2)
cropPath2 = outPath2 + "-cropped"
subprocess.run(f"pdfcrop {outPath2} {cropPath2}", shell=True)
subprocess.run(f"mv {cropPath2} {outPath2}", shell=True)
plt.show()