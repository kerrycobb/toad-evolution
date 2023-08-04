#!/usr/bin/env python

import os
import fire    
from bgc_utils import BGC, cline_plot, outliers
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import norm
from scipy.stats import pearsonr
from scipy.stats import norm
from scipy.stats import kruskal
import plotly.io as pio   
pio.kaleido.scope.mathjax = None


# # name = "popmap2-100" 
# name = "popmap2-95" 
# # name = "popmap3-100" 
# # name = "popmap3-95" 
# outDir = "out-" + name

def pearson_correlation(fst, param, outlier, param_str, path, highlight=True):
    nan = fst["WEIR_AND_COCKERHAM_FST"].isnull() 
    fst = fst[~nan]
    param = param[~nan]
    # outlier = outlier[~nan]

    x = fst["WEIR_AND_COCKERHAM_FST"].to_numpy() 
    y = param.to_numpy()
    assert x.shape == y.shape

    pearson = pearsonr(x, y)
    print(pearson)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(color="rgb(150, 150, 150)")))
    pad = 0.01
    fig.update_layout(width=400, height=400, plot_bgcolor="white", 
            margin=dict(l=0,r=0,b=0,t=0), legend=dict(yanchor="top", xanchor="right"))
    fig.update_xaxes(title_font=dict(size=20), range=[min(x)-0.01, max(x)+0.01], 
            showline=True, ticks="outside", linecolor="black", linewidth=1)
    fig.update_yaxes(title_font=dict(size=20), range=[min(y)-0.005,max(y)+0.005], 
            showline=True, ticks="outside", linecolor="black", linewidth=1)
    fig.write_image(path)

def summary(outDir, chains, burnin, interval):
    colors = [line.rstrip('\n') for line in open('../colors-hybrid.txt')]
    name = outDir.lstrip("out-") 
    paths = [os.path.join(outDir, "{}_{}.hdf5".format(name, i)) for i in range(1, chains + 1)]
    rand_loci = np.sort(np.random.randint(502, size=20))

    bgc = BGC(paths, burnin, interval)

    # LnL = bgc.posterior("LnL")
    alpha = bgc.posterior("alpha")
    tau_alpha = bgc.posterior("tau-alpha")
    beta = bgc.posterior("beta")
    tau_beta = bgc.posterior("tau-beta")
    # hi = bgc.posterior("hi")

    # def plot_path(param):
    #     return os.path.join(outDir, f"{name}-{param}.html")

    # LnL.histogram().write_html(plot_path("LnL-hist")) 
    # alpha.histogram(rand_loci).write_html(plot_path("alpha-hist")) 
    # tau_alpha.histogram().write_html(plot_path("tau_alpha-hist")) 
    # beta.histogram(rand_loci).write_html(plot_path("beta-hist")) 
    # tau_beta.histogram().write_html(plot_path("tau_beta-hist")) 
    # hi.histogram().write_html(plot_path("hi-hist")) 

    # LnL.trace().write_html(plot_path("LnL-trace")) 
    # alpha.trace(rand_loci).write_html(plot_path("alpha-trace")) 
    # tau_alpha.trace().write_html(plot_path("tau_alpha-trace")) 
    # beta.trace(rand_loci).write_html(plot_path("beta-trace")) 
    # tau_beta.trace().write_html(plot_path("tau_beta-trace")) 
    # hi.trace().write_html(plot_path("hi-trace")) 

    # all_sum = pd.concat(
    #     [
    #         LnL.summary,
    #         alpha.summary,
    #         tau_alpha.summary,
    #         beta.summary,
    #         tau_beta.summary,
    #         hi.summary,
    #     ])   
    # all_sum.to_csv(os.path.join(outDir, "parameter-summaries.csv"))

    print("Alpha range: {:.3} - {:.3}".format(min(alpha.summary["median"]), 
            max(alpha.summary["median"])))
    print("Beta range: {:.3} - {:.3}".format(min(beta.summary["median"]), 
            max(beta.summary["median"])))

    ## Identify outliers
    # Identify outlier loci relative to genome-wide average 
    alpha_covered = ~alpha.covered(0)
    print(f"Genome-wide average alpha distribution outliers: {alpha_covered.sum()}")
    beta_covered = ~beta.covered(0)
    print(f"Genome-wide average beta distribution outliers: {beta_covered.sum()}")

    # Breakdown negative vs positive alpha outliers relative to genome-wide average
    neg_alpha_covered = alpha_covered & (alpha.summary["median"] < 0)
    pos_alpha_covered = alpha_covered & (alpha.summary["median"] > 0)
    uncovered_alpha = ~alpha_covered
    print(f"Negative covered alpha: {neg_alpha_covered.sum()}")
    print(f"Positive covered alpha: {pos_alpha_covered.sum()}")

    # Identify outlier loci relative to genome-wide distribution of locus specific introgression 
    alpha_out = outliers(alpha, tau_alpha, 0.95)
    print(f"Genome-wide distribution of locus specific introgression alpha outliers: {sum(alpha_out)}")
    beta_out = outliers(beta, tau_beta, 0.95)
    print(f"Genome-wide distribution of locus specific introgression beta outliers: {sum(beta_out)}")

    # Breakdown negative vs positive alpha outliers relative to genome-wide 
    # distribution of locus specific introgression
    neg_alpha_out = alpha_out & (alpha.summary["median"] < 0)
    pos_alpha_out = alpha_out & (alpha.summary["median"] > 0)
    neutral_alpha = ~alpha_out
    print(f"Negative genome-wide distribution of locus specific introgression outliers: {sum(neg_alpha_out)}")
    print(f"Positive genome-wide distribution of locus specific introgression outliers: {sum(pos_alpha_out)}")

    # Check that there is complete overlap between alpha outlier types 
    print(f"Number of alpha outlier loci overalpping: {sum(alpha_covered & alpha_out)}")

    ## Plot clines and outliers
    cline_plot(
        alpha=alpha.summary["median"], 
        beta=beta.summary["median"], 
        outliers=[pos_alpha_out, neg_alpha_out], 
        outlier_label=["<i>americanus</i>", "<i>terrestris</i>"],
        outlier_color=[colors[0], colors[1]],
        yaxis_label="<i>americanus</i> Ancestry Probability"
    ).write_image(outDir + "/cline-outliers.pdf")


    # # # Code to visualize conditional prior distribution along with the posterior 
    # # def plot_tau(param, tau, path):
    # #     tau_central = tau.summary.iloc[0]["mean"]
    # #     sigma = 1/tau_central     
    # #     x = np.linspace(-3*sigma, 3*sigma, 100)
    # #     pdf = norm.pdf(x, 0, sigma)
    # #     fig, ax = plt.subplots()
    # #     ax.hist(param.summary["median"], bins="auto", density=True, alpha=0.7)
    # #     ax.plot(x, pdf)
    # #     fig.savefig(path, bbox_inches="tight")
    # #     # plt.show()
    # # plot_tau(alpha, tau_alpha, outDir + "/tau_alpha.pdf")
    # # plot_tau(beta, tau_beta, outDir + "/tau_beta.pdf")


    # Read in fst estimates and replace negatives with 0
    fst = pd.read_csv(os.path.join(outDir, name + "-mean-fst.csv"))
    neg = fst["WEIR_AND_COCKERHAM_FST"] < 0 
    fst[neg] = 0.0

    fst_neg_alpha_out = fst[neg_alpha_out]["WEIR_AND_COCKERHAM_FST"].values 
    fst_pos_alpha_out = fst[pos_alpha_out]["WEIR_AND_COCKERHAM_FST"].values 
    fst_neutral_alpha = fst[neutral_alpha] 
    fst_neutral_alpha = fst_neutral_alpha.dropna(subset="WEIR_AND_COCKERHAM_FST")
    fst_neutral_alpha = fst_neutral_alpha["WEIR_AND_COCKERHAM_FST"].values 

    print("Mean fst: {}".format(fst["WEIR_AND_COCKERHAM_FST"].mean()))
    print("Fixed Loci: {}".format((fst["WEIR_AND_COCKERHAM_FST"] == 1.0).sum()))
    print("Fst 0: {}".format((fst["WEIR_AND_COCKERHAM_FST"] == 0.0).sum()))

    # Pearson Correlation
    print("Alpha correlation")
    pearson_correlation(fst, alpha.summary["median"].abs(), np.zeros(len(fst)).astype(bool), 
            r"$\alpha$", outDir + "/fst-alpha-relation.pdf")
    print("Beta Correlation")
    pearson_correlation(fst, beta.summary["median"], beta_out, 
            r"$\beta$", outDir + "/fst-beta-relation.pdf")


    ## Fst Plot 
    # Histogram
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.075,
            subplot_titles=("(A)", "(B)"))
    fig.add_trace(go.Histogram(x=fst["WEIR_AND_COCKERHAM_FST"],
            marker=dict(color="rgb(150, 150, 150)", line=dict(color="black"))),
            row=1, col=1)
    # Box Plot
    fig.add_trace(go.Box(x=fst_neg_alpha_out, name="<i>terrestris</i>", line=dict(color=colors[1]), 
            pointpos=0, boxpoints="all", jitter=0.2), row=2, col=1)
    fig.add_trace(go.Box(x=fst_neutral_alpha, name="Neutral", line=dict(color="rgb(150, 150, 150)"),
            pointpos=0, boxpoints="all", jitter=0.2), row=2, col=1)
    fig.add_trace(go.Box(x=fst_pos_alpha_out, name="<i>americanus</i>", line=dict(color=colors[0]), 
            pointpos=0, boxpoints="all", jitter=0.2), row=2, col=1)
    fig.update_layout(width=800, height=600, plot_bgcolor="white", bargap=0.1,
            margin=dict(l=0,r=0,b=0,t=20), showlegend=False)
    fig.update_xaxes(title_font=dict(size=20), showline=True, ticks="outside", 
            linecolor="black", linewidth=1)
    fig.update_xaxes(title_text="F<sub>ST</sub>", row=2, col=1)
    fig.update_yaxes(showline=True, ticks="outside", linecolor="black", linewidth=1)
    fig.layout.annotations[0].update(x=-0.1)
    fig.layout.annotations[1].update(x=-0.1)
    fig.write_image(outDir + "/fst-plot.pdf")
    # fig.show()

    krus = kruskal(fst_neg_alpha_out, fst_pos_alpha_out, fst_neutral_alpha)
    print(krus)

    import scikit_posthocs as sp
   
    fst_neg_alpha_out_df =  pd.DataFrame(fst_neg_alpha_out, columns=["fst"])
    fst_pos_alpha_out_df =  pd.DataFrame(fst_pos_alpha_out, columns=["fst"])
    fst_neutral_alpha_df =  pd.DataFrame(fst_neutral_alpha, columns=["fst"])
    fst_neg_alpha_out_df["group"] = "negative"
    fst_pos_alpha_out_df["group"] = "positive"
    fst_neutral_alpha_df["group"] = "netural"
    fst_df  = pd.concat([fst_neg_alpha_out_df, fst_pos_alpha_out_df, fst_neutral_alpha_df], ignore_index=True, axis=0)
    mann_whit = sp.posthoc_mannwhitney(fst_df, val_col="fst", group_col="group")
    print("Mann-Whitney Uncorrected P-values")
    print(mann_whit)
    # mann_whit = sp.posthoc_mannwhitney(fst_df, val_col="fst", group_col="group", p_adjust="bonferroni")
    # print(mann_whit)




if __name__ == "__main__":
    fire.Fire(summary)


