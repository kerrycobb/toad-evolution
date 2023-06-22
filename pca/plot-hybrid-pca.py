#!/usr/bin/env python

import fire
import pandas as pd
from functools import reduce
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio   
pio.kaleido.scope.mathjax = None # Needed to elemenate mathjax loading box being displayed on pdfs

def plotPCA(dir, qmatFile, assign, reverse_y=False):
    name = dir.rstrip('/').lstrip("out-") 
    path = dir + "/principle-components.csv"
    df = pd.read_csv(path)
    if reverse_y:
        df["Axis2"] = df["Axis2"].apply(np.negative)
    anc_coeff = pd.read_csv(f"../structure/qmats/{qmatFile}-K-2.csv")
    df = df.merge(anc_coeff, left_on="Unnamed: 0", right_on="Unnamed: 0", how="inner")
    colors = [l.strip() for l in open("../colors-hybrid.txt", "r")]
    propVariance = [float(l.strip()) for l in open(f"{dir}/prop-variance.txt")]
    amer = pd.read_csv(f"../bgc/{assign}-americanus.txt", header=None)
    terr = pd.read_csv(f"../bgc/{assign}-terrestris.txt", header=None)
    admx = pd.read_csv(f"../bgc/{assign}-admixed.txt", header=None)
    amer["assigned"] = "americanus"
    terr["assigned"] = "terrestris"
    admx["assigned"] = "admixed"
    amer = df.merge(amer, left_on="Unnamed: 0", right_on=0, how="inner")
    terr = df.merge(terr, left_on="Unnamed: 0", right_on=0, how="inner")
    admx = df.merge(admx, left_on="Unnamed: 0", right_on=0, how="inner")

    # PCA Plot 
    fig = go.Figure()
    def add_pca_trace(df, name, color):
        fig.add_trace(go.Scatter(
            x=df["Axis1"],
            y=df["Axis2"],
            mode="markers",
            name=name,
            hovertext=df[0],
            marker_color=color,
            opacity=1.0,
            marker=dict(size=10, line=dict(width=.5, color="black")),
    ))
    add_pca_trace(amer, "americanus", colors[0])
    add_pca_trace(terr, "terrestris", colors[1])
    add_pca_trace(admx, "admixed", colors[2])
    fig.update_layout(
        plot_bgcolor="white",
        width=500,
        height=500,
        margin=dict(l=0,r=0,b=0,t=0), 
        showlegend=False)
    fig.update_xaxes(
        title_text=f"PC1({propVariance[0]:.1f}%)",
        title_font=dict(size=20),
        showline=True,
        linewidth=1,
        linecolor="black",
        ticks="outside")
    fig.update_yaxes(
        title_text=f"PC2({propVariance[1]:.1f}%)",
        title_font=dict(size=20),
        showline=True,
        linewidth=1,
        linecolor="black",
        ticks="outside")
    plot_path = f"out-plots/{name}-pca.pdf"
    fig.write_image(plot_path)
    # fig.show()
    print(f"Plot written to {plot_path}")


    # Ancestry Plot
    fig = go.Figure()
    def add_pca_trace(df, name, color):
        fig.add_trace(go.Scatter(
            x=df["Axis1"],
            y=df["Cluster1"],
            mode="markers",
            name=name,
            hovertext=df[0],
            marker_color=color,
            opacity=1.0,
            marker=dict(size=10, line=dict(width=.5, color="black")),
        ))
    add_pca_trace(amer, "americanus", colors[0])
    add_pca_trace(terr, "terrestris", colors[1])
    add_pca_trace(admx, "admixed", colors[2])
    fig.update_layout(
        plot_bgcolor="white",
        width=500,
        height=500,
        margin=dict(l=0,r=0,b=0,t=0),
        showlegend=False)
        # legend=dict(
        #     yanchor="top",
        #     y=0.99,
        #     xanchor="left",
        #     x=0.01))
    fig.update_xaxes(
        title_text=f"PC1",
        title_font=dict(size=20),
        showline=True,
        ticks="outside",
        linecolor="black",
        linewidth=1)
    fig.update_yaxes(
        title_text=f"Ancestry Coefficient",
        title_font=dict(size=20),
        showline=True,
        ticks="outside", 
        linecolor="black",
        linewidth=1)

    plot_path = f"out-plots/{name}-admx-coeff.pdf"
    fig.write_image(plot_path) 
    # fig.show()
    print(f"Plot written to {plot_path}")

if __name__ == "__main__":
    fire.Fire(plotPCA)