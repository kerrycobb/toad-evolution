#!/usr/bin/env python

import fire 
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.mpl.ticker as cticker
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import math
import cartopy.io.shapereader as shpreader
from metpy.plots import USSTATES, USCOUNTIES
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
# from matplotlib.patches import Patch
import matplotlib.patches as mpatches
import shapely.geometry as sgeom
import geopandas as gpd

colorPath = "../colors-hybrid.txt"
qmatPath = "../structure/qmats/"
outDir = "out/"

def get_midpoint(lons, lats):
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)
    lon0 = max_lon - ((max_lon - min_lon) / 2)
    lat0 = max_lat - ((max_lat - min_lat) / 2)
    return lon0, lat0 

def rgb(r, g, b):
    return (r/255, g/255, b/255) 

def draw_pie(ax, props, xpos, ypos, size, colors):
    zorder = 100
    cumsum = np.cumsum(props)
    cumsum = cumsum / cumsum[-1]
    pie = [0] + cumsum.tolist()
    for i, (r1, r2) in enumerate(zip(pie[:-1], pie[1:])):
        angles = np.linspace(2 * np.pi * r1, 2 * np.pi * r2)
        x = [0] + np.cos(angles).tolist()
        y = [0] + np.sin(angles).tolist()
        xy = np.column_stack([x, y])
        ax.scatter(xpos, ypos, marker=xy, s=size, color=colors[i], alpha=1, 
                   transform=ccrs.Geodetic(), linewidth=0, zorder=zorder)
    ax.scatter(xpos, ypos, marker="o", s=size, facecolor="none", linewidth=.5,
            edgecolor="black", zorder=zorder, transform=ccrs.Geodetic())

def map(name, assign, extent=None, counties=False, rivers=False, title=None, legend=None, labels=None):
    colors = [line.rstrip('\n') for line in open(colorPath)]
    # Read sample data
    data = pd.read_csv("../sample-data.csv")
    data.drop_duplicates(subset="sample_id", inplace=True)
    # Read admixture coefficients
    qmat = pd.read_csv(qmatPath + name +".csv", index_col=0)
    # Merge everything
    merged = qmat.merge(data[["sample_id", "latitude", "longitude"]], left_index=True, 
        right_on="sample_id") 
    # Convert to geo dataframe
    gdf = gpd.GeoDataFrame(merged, geometry=gpd.points_from_xy(
            merged.longitude, merged.latitude), crs="EPSG:4326")

    # # Read pop assignments
    # amer = pd.read_csv(f"../bgc/{assign}-americanus.txt", header=None)
    # terr = pd.read_csv(f"../bgc/{assign}-terrestris.txt", header=None)
    # admx = pd.read_csv(f"../bgc/{assign}-admixed.txt", header=None)
    # amer["assigned"] = "americanus"
    # terr["assigned"] = "terrestris"
    # admx["assigned"] = "admixed"
    # # amer = merged.merge(amer, left_on="sample_id", right_on=0, how="inner")
    # terr = merged.merge(terr, left_on="sample_id", right_on=0, how="inner")
    # admx = merged.merge(admx, left_on="sample_id", right_on=0, how="inner")

    # Create projection
    lon0, lat0 = get_midpoint(gdf.longitude, gdf.latitude)
    # proj = ccrs.Orthographic(lon0, lat0)
    proj = ccrs.PlateCarree()


    # Create plot object
    fig = plt.figure()
    ax = plt.axes(projection=proj)

    # Add default features
    # ax.add_feature(cfeature.OCEAN.with_scale("10m"))
    ax.add_feature(cfeature.LAND.with_scale("10m"))
    # ax.add_feature(cfeature.STATES.with_scale("10m"), linewidth=0.4, 
            # edgecolor=rgb(120, 120, 120))

    # # Add optional features            
    # if counties:
    #     county_data = cfeature.NaturalEarthFeature(category="cultural", scale="10m",
    #             name="admin_2_counties")
    #     ax.add_feature(county_data, linewidth=0.2, edgecolor=rgb(150, 150, 150), 
    #             facecolor="none")
    # if rivers:
    #     ax.add_feature(cfeature.RIVERS)

    # # Set extent manually 
    # if extent:
    #     ax.set_extent([float(x.strip()) for x in extent.split(",")])

    # Highlight areas for zoom
    zoom1_box = sgeom.box(-86.72,33.16,-86.36,32.86) #
    ax.add_geometries([zoom1_box], crs=ccrs.Geodetic(), facecolor="none", 
            linewidth=1, edgecolor="black", zorder=1000)
    is_zoom1 = gdf.within(zoom1_box)

    zoom2_box = sgeom.box(-85.86,32.84,-85.4,32.36) #
    ax.add_geometries([zoom2_box], crs=ccrs.Geodetic(), facecolor="none", 
            linewidth=1, edgecolor="black", zorder=1000)
    is_zoom2 = gdf.within(zoom2_box)

    # Plot admixture proportions
    gdf.loc[is_zoom1 | is_zoom2, "size"] = 10
    gdf.loc[~is_zoom1 & ~is_zoom2, "size"] = 100
    for ix, row in gdf.iterrows():
        props = row[0:2].to_list()
        draw_pie(ax, props, row.longitude, row.latitude, row["size"], colors)

    ###########################
    # Zoom maps
    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
    # zoomProj = ccrs.Orthographic(inLon0, inLat0) 
    zoomProj = ccrs.PlateCarree() 
    # inset_ax = fig.add_axes([0, 0, 0.25, 0.25], projection=zoomProj) 

    zoom1_ax = ax.inset_axes(, projection=zoomProj) 
    for ix, row in gdf[is_zoom1].iterrows():
        props = row[0:2].to_list()
        draw_pie(zoom1_ax, props, row.longitude, row.latitude, row["size"], colors)
    # zoom1_ax.set_extent


    # ########################### 
    # # Create Inset 
    # def set_subplot2corner(ax, ax_sub, corner, pad=0):
    #     ax.get_figure().canvas.draw()
    #     p1 = ax.get_position()
    #     p2 = ax_sub.get_position()
    #     hp = pad * p1.width 
    #     vp = pad * p1.height 
    #     if corner == "topright":
    #         ax_sub.set_position([p1.x1-p2.width-hp, p1.y1-p2.height-vp, p2.width, p2.height])
    #     if corner == "bottomright":
    #         ax_sub.set_position([p1.x1-p2.width-hp, p1.y0+vp, p2.width, p2.height])
    #     if corner == "bottomleft":
    #         ax_sub.set_position([p1.x0+hp, p1.y0+vp, p2.width, p2.height])
    #     if corner == "topleft":
    #         ax_sub.set_position([p1.x0+hp, p1.y1-p2.height-vp, p2.width, p2.height])

    # # Create inset projection and axis
    # inset_extent = [-98, -73.5, 23.5, 44]
    # inLon0, inLat0 = get_midpoint(inset_extent[0:2], inset_extent[2:4])
    # # inProj = ccrs.Orthographic(inLon0, inLat0) 
    # inProj = proj
    # inset_ax = fig.add_axes([0, 0, 0.25, 0.25], projection=inProj)
    # inset_ax.set_extent(inset_extent)

    # # Add features to inset map
    # inset_ax.add_feature(cfeature.OCEAN)
    # inset_ax.add_feature(cfeature.LAND) 
    # inset_ax.add_feature(cfeature.LAKES)
    # inset_ax.add_feature(cfeature.STATES, linewidth=.25, edgecolor="black")

    # # Show species ranges on inset map
    # americanus_range = gpd.read_file("range-maps/americanus-great-lakes.geojson")
    # americanus_range.to_crs(inProj.proj4_params, inplace=True)
    # americanus_range.plot(ax=inset_ax, facecolor=colors[0], alpha=0.85, linewidth=0)

    # terrestris_range = gpd.read_file("range-maps/terrestris.geojson")
    # terrestris_range.to_crs(inProj.proj4_params, inplace=True)
    # terrestris_range.plot(ax=inset_ax, facecolor=colors[1], alpha=0.85, linewidth=0)

    # # Show extent of main map on inset
    # map_extent = ax.get_extent(crs=ccrs.PlateCarree())
    # extent_box = sgeom.box(map_extent[0], map_extent[2], map_extent[1], map_extent[3])
    # inset_ax.add_geometries([extent_box], crs=ccrs.Geodetic(), facecolor='red', zorder=100, 
    #         alpha=0.3, edgecolor="red", linewidth=0.5)
    # # inset_ax.add_geometries([extent_box], crs=ccrs.Geodetic(), edgecolor="red", 
    #         # facecolor="None", linewidth=.5)

    # # Reposition and style inset
    # set_subplot2corner(ax, inset_ax, "bottomleft", 0.015)
    # inset_ax.spines[:].set_linewidth(2)

    # #########################
    # # Make legend
    # if legend:
    #     if labels:
    #         legLabels = labels
    #     else:
    #         legLabels = qmat.columns[0:2]
    #     legendElements = [] 
    #     for i in range(2):
    #         legendElements.append(mpatches.Patch(
    #             facecolor=colors[i], edgecolor="black", label=legLabels[i]))
    #     ax.legend(loc=legend, handles=legendElements, fontsize=6)

    # Output
    outPath = outDir + "structure-" + name + ".pdf" 
    # plt.savefig(outPath, bbox_inches='tight', pad_inches=0)
    print(f"Plot output to {outPath}")
    plt.show()




if __name__ == "__main__":
    fire.Fire(map)