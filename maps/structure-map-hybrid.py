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
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.patches import FancyBboxPatch

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

def scale_bar(ax, length=None, location=(0.5, 0.05)):
    """
    ax is the axes to draw the scalebar on.
    length is the length of the scalebar in km.
    location is center of the scalebar in axis coordinates.
    (ie. 0.5 is the middle of the plot)
    linewidth is the thickness of the scalebar.
    """
    #Get the limits of the axis in lat long
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    #Make tmc horizontally centred on the middle of the map,
    #vertically at scale bar location
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]
    tmc = ccrs.TransverseMercator(sbllx, sblly)
    #Get the extent of the plotted area in coordinates in metres
    x0, x1, y0, y1 = ax.get_extent(tmc)
    height = y1 - y0  
    width = x1 - x0
    #Turn the specified scalebar location into coordinates in metres
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]
    #Calculate a scale bar length if none has been given
    #(Theres probably a more pythonic way of rounding the number but this works)
    if not length: 
        length = (x1 - x0) / 5000 #in km
        ndim = int(np.floor(np.log10(length))) #number of digits in number
        length = round(length, -ndim) #round to 1sf
        #Returns numbers starting with the list
        def scale_number(x):
            if str(x)[0] in ['1', '2', '5']: return int(x)        
            else: return scale_number(x - 10 ** ndim)
        length = scale_number(length) 
    #Generate the x coordinate for the ends of the scalebar
    bar_xs = [sbx - length * 500, sbx + length * 500]
    linewidth = 0.5
    # Calculate some offsets
    offset = 0.01
    sby_off_plus = sby + (height * offset) 
    sby_off_minus = sby - (height * offset) 
    #Plot the scalebar with end caps
    ax.plot(bar_xs, [sby, sby], transform=tmc, color='black', linewidth=linewidth)
    ax.plot([bar_xs[0], bar_xs[0]], [sby_off_plus, sby_off_minus], 
            transform=tmc, color="black", linewidth=linewidth)
    ax.plot([bar_xs[1], bar_xs[1]], [sby_off_plus, sby_off_minus], 
            transform=tmc, color="black", linewidth=linewidth)
    #Plot the scalebar label
    ax.text(sbx, sby - (height * 0.01), str(length) + ' km', transform=tmc,
            horizontalalignment='center', verticalalignment='top', fontsize=5)

def map(name, extent=None, legend=None, labels=None):
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
    proj = ccrs.AlbersEqualArea(lon0, lat0)
    # proj = ccrs.PlateCarree()

    # Create plot object
    fig = plt.figure(1)
    ax = plt.axes(projection=proj)

    # Add default features
    ax.add_feature(cfeature.OCEAN.with_scale("10m"))
    ax.add_feature(cfeature.LAND.with_scale("10m"))
    ax.add_feature(cfeature.STATES.with_scale("10m"), linewidth=0.4, 
            edgecolor=rgb(120, 120, 120))
    county_data = cfeature.NaturalEarthFeature(category="cultural", scale="10m",
            name="admin_2_counties")
    ax.add_feature(county_data, linewidth=0.2, edgecolor=rgb(150, 150, 150), 
            facecolor="none")

    # Highlight areas for zoom
    zoom1_box = sgeom.box(-86.72,33.16,-86.36,32.86) #
    # ax.add_geometries([zoom1_box], crs=ccrs.Geodetic(), facecolor="none", 
    #         linewidth=1, edgecolor="black", zorder=1000)
    is_zoom1 = gdf.within(zoom1_box)
    zoom1_box_gdf = gpd.GeoDataFrame(index=[0], crs=proj.proj4_params, geometry=[zoom1_box])

    zoom2_box = sgeom.box(-85.86,32.84,-85.4,32.36) #
    # ax.add_geometries([zoom2_box], crs=ccrs.Geodetic(), facecolor="none", 
    #         linewidth=1, edgecolor="black", zorder=1000)
    is_zoom2 = gdf.within(zoom2_box)

    # Plot admixture proportions
    gdf.loc[is_zoom1 | is_zoom2, "size"] = 8 
    gdf.loc[~is_zoom1 & ~is_zoom2, "size"] = 100
    for ix, row in gdf.iterrows():
        props = row[0:2].to_list()
        draw_pie(ax, props, row.longitude, row.latitude, row["size"], colors)

    outPath = outDir + "structure-" + name + "-main.pdf" 
    plt.savefig(outPath, bbox_inches='tight', pad_inches=0)

    ########################### 
    ## Create Inset 
    def set_subplot2corner(ax, ax_sub, corner, pad=0):
        ax.get_figure().canvas.draw()
        p1 = ax.get_position()
        p2 = ax_sub.get_position()
        hp = pad * p1.width 
        vp = pad * p1.height 
        if corner == "topright":
            ax_sub.set_position([p1.x1-p2.width-hp, p1.y1-p2.height-vp, p2.width, p2.height])
        if corner == "bottomright":
            ax_sub.set_position([p1.x1-p2.width-hp, p1.y0+vp, p2.width, p2.height])
        if corner == "bottomleft":
            ax_sub.set_position([p1.x0+hp, p1.y0+vp, p2.width, p2.height])
        if corner == "topleft":
            ax_sub.set_position([p1.x0+hp, p1.y1-p2.height-vp, p2.width, p2.height])

    # Create inset projection and axis
    inset_extent = [-98, -73.5, 23.5, 44]
    inLon0, inLat0 = get_midpoint(inset_extent[0:2], inset_extent[2:4])
    inProj = ccrs.AlbersEqualArea(inLon0, inLat0)
    inset_ax = fig.add_axes([0, 0, 0.25, 0.25], projection=inProj)

    inset_ax.set_extent(inset_extent)

    # Add features to inset map
    inset_ax.add_feature(cfeature.OCEAN)
    inset_ax.add_feature(cfeature.LAND) 
    inset_ax.add_feature(cfeature.LAKES)
    inset_ax.add_feature(cfeature.STATES, linewidth=.25, edgecolor="black")

    # gl = inset_ax.gridlines(linewidth=0.25, linestyle=(0, (5, 5)), color="black")
    # gl.xlocator = mticker.FixedLocator([-95, -85, -75])
    # gl.ylocator = mticker.FixedLocator([25, 33, 41])

    # Show species ranges on inset map
    americanus_range = gpd.read_file("range-maps/range-americanus.geojson")
    americanus_range.to_crs(inProj.proj4_params, inplace=True)
    americanus_range.plot(ax=inset_ax, facecolor=colors[0], alpha=0.85, linewidth=0)

    terrestris_range = gpd.read_file("range-maps/range-terrestris.geojson")
    terrestris_range.to_crs(inProj.proj4_params, inplace=True)
    terrestris_range.plot(ax=inset_ax, facecolor=colors[1], alpha=0.85, linewidth=0)

    # Show extent of main map on inset
    map_extent = ax.get_extent(crs=ccrs.PlateCarree())
    extent_box = sgeom.box(map_extent[0], map_extent[2], map_extent[1], map_extent[3])
    inset_ax.add_geometries([extent_box], crs=ccrs.Geodetic(), facecolor='red', zorder=100, 
            alpha=0.3, edgecolor="red", linewidth=0.5)
    # inset_ax.add_geometries([extent_box], crs=ccrs.Geodetic(), edgecolor="red", 
            # facecolor="None", linewidth=.5)


    # Reposition and style inset
    set_subplot2corner(ax, inset_ax, "bottomleft", 0.015)
    inset_ax.spines[:].set_linewidth(2)
    inset_ax.spines[:].set_joinstyle("round")
    inset_ax.spines[:].set_capstyle("projecting")


    ###########################
    ## Zoom maps

    def create_zoom_ax(points, scale_pos, name, stream=None):
        ## Zoom 2 Map
        # lon0, lat0 = get_midpoint(gdf[points].longitude, gdf[points].latitude)
        # Create Map
        ax = fig.add_axes([1, -0.1, 0.375, 0.375], projection=proj)
        # Add features
        ax.add_feature(cfeature.LAND.with_scale("10m"))
        county_data = cfeature.NaturalEarthFeature(category="cultural", scale="10m",
                name="admin_2_counties")
        ax.add_feature(county_data, linewidth=0.2, edgecolor=rgb(150, 150, 150), 
                facecolor="none")
        ax.add_feature(cfeature.RIVERS.with_scale("10m"), linewidth=4)
        # ax.add_feature(cfeature.LAKES.with_scale("10m"))

        # Add pies
        for ix, row in gdf[points].iterrows():
            props = row[0:2].to_list()
            draw_pie(ax, props, row.longitude, row.latitude, 100, colors)
        ## Scale Bar
        scale_bar(ax, 5, scale_pos) 

        if stream is not None:
            ax.autoscale(False)
            stream.plot(ax=ax, edgecolor=cfeature.COLORS["water"], linewidth=2)
        return ax

    waxahatchee = gpd.read_file("water-data/waxahatchee-creek.geojson")
    waxahatchee.to_crs(proj.proj4_params, inplace=True)
    sougahatchee = gpd.read_file("water-data/sougahatchee-creek.geojson")
    sougahatchee.to_crs(proj.proj4_params, inplace=True)

    zoom1_ax = create_zoom_ax(is_zoom1, (0.9, 0.95), name + "-zoom1", waxahatchee)
    zoom2_ax = create_zoom_ax(is_zoom2, (0.1, 0.95), name + "-zoom2", sougahatchee)

    ## Reposition Zoom Axes
    ax.get_figure().canvas.draw()
    p1 = ax.get_position()
    p2 = zoom1_ax.get_position()
    p3 = zoom2_ax.get_position()
    pad = 0.025
    # Caclulate padding for each axis
    hp = pad * p1.width 
    vp = pad * p1.height 
    # Reposition based on position and calulated padding
    # [Horizontal Position, Vertical Position, Width, Height]
    zoom1_ax.set_position([p1.x1 + hp, p1.y0 + (p1.height/2) + (vp/2) , p2.width, p2.height])
    zoom2_ax.set_position([p1.x1 + hp, p1.y0 + (p1.height/2) - p3.height - (vp/2), p3.width, p3.height])

    ## Zoom Indicators
    ax.indicate_inset_zoom(zoom1_ax)#, connector_lines=(True, True, True, True))#, edgecolor="black", linewidth=0.5, alpha=1) 
    ax.indicate_inset_zoom(zoom2_ax)#, connector_lines=(True, True, True, True))#, edgecolor="black", linewidth=0.5, alpha=1) 

    #########################
    # Make legend
    if legend:
        if labels:
            legLabels = labels
        else:
            legLabels = qmat.columns[0:2]
        legendElements = [] 
        for i in range(2):
            legendElements.append(mpatches.Patch(
                facecolor=colors[i], edgecolor="black", label=legLabels[i]))
        ax.legend(loc=legend, handles=legendElements, fontsize=6)

    # Output
    outPath = outDir + "structure-" + name + ".pdf" 
    plt.savefig(outPath, bbox_inches='tight', pad_inches=0)
    print(f"Plot output to {outPath}")
    # plt.show()

if __name__ == "__main__":
    fire.Fire(map)