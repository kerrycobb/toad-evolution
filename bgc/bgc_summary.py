from bgc_utils import BGC, cline_plot, outliers
import pandas as pd
import numpy as np
import os
from scipy.stats import norm

# name = "popmap2-100" 
name = "popmap2-95" 
# name = "popmap3-100" 
# name = "popmap3-95" 
outDir = "out-" + name
show = False

chains = 5 
paths = [os.path.join(outDir, "{}_{}.hdf5".format(name, i)) for i in range(1, chains + 1)]
rand_loci = np.sort(np.random.randint(502, size=20))

bgc = BGC(paths, 100, 0.9)

# LnL = bgc.posterior("LnL")
alpha = bgc.posterior("alpha")
tau_alpha = bgc.posterior("tau-alpha")
beta = bgc.posterior("beta")
tau_beta = bgc.posterior("tau-beta")
# hi = bgc.posterior("hi")

# def plot_path(param):
#     return os.path.join(outDir, f"{name}-{param}.html")

# LnL.histogram(plot_path("LnL-hist"), show=show) 
# alpha.histogram(plot_path("alpha-hist"), rand_loci, show=show) 
# tau_alpha.histogram(plot_path("tau_alpha-hist"), show=show) 
# beta.histogram(plot_path("beta-hist"), rand_loci, show=show) 
# tau_beta.histogram(plot_path("tau_beta-hist"), show=show) 
# hi.histogram(plot_path("hi-hist"), show=show) 

# LnL.trace(plot_path("LnL-trace"), show=show) 
# alpha.trace(plot_path("alpha-trace"), rand_loci, show=show) 
# tau_alpha.trace(plot_path("tau_alpha-trace"), show=show) 
# beta.trace(plot_path("beta-trace"), rand_loci, show=show) 
# tau_beta.trace(plot_path("tau_beta-trace"), show=show) 
# hi.trace(plot_path("hi-trace"), show=show) 

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

# Identify loci with excess ancestry
alpha_covered = ~alpha.covered(0)
print(f"Loci with excess ancestry: {alpha_covered.sum()}")

beta_covered = ~beta.covered(0)
print(f"Number of Beta outliers: {beta_covered.sum()}")

# Identify outlier loci
alpha_out = outliers(alpha, tau_alpha, 0.95)
print(f"Alpha outliers: {sum(alpha_out)}")

beta_out = outliers(beta, tau_beta, 0.95)
print(f"Beta outliers: {sum(beta_out)}")

## Plot clines and outliers
cline_plot(alpha.summary["median"], beta.summary["median"], [alpha_covered, alpha_out])
# cline_plot(alpha.summary["median"], beta.summary["median"], beta_covered)

# # Code to visualize conditional prior distribution along with the posterior 
# import matplotlib.pyplot as plt
# from scipy.stats import norm

# def plot_tau(param, tau, path):
#     tau_central = tau.summary.iloc[0]["mean"]
#     sigma = 1/tau_central     
#     x = np.linspace(-3*sigma, 3*sigma, 100)
#     pdf = norm.pdf(x, 0, sigma)
#     fig, ax = plt.subplots()
#     ax.hist(param.summary["median"], bins="auto", density=True, alpha=0.7)
#     ax.plot(x, pdf)
#     fig.savefig(path, bbox_inches="tight")
#     # plt.show()

# plot_tau(alpha, tau_alpha, outDir + "/tau_alpha.pdf")
# plot_tau(beta, tau_beta, outDir + "/tau_beta.pdf")


from scipy.stats import pearsonr
import plotly.graph_objects as go

def pearson_correlation(fst, param, covered, outlier, highlight=True):
    nan = fst["WEIR_AND_COCKERHAM_FST"].isnull() 
    fst = fst[~nan]
    param_sum = param.summary[~nan]
    covered = covered[~nan]
    outlier = outlier[~nan]

    x = fst["WEIR_AND_COCKERHAM_FST"].to_numpy() 
    y = param_sum["median"].to_numpy()
    assert x.shape == y.shape

    min_x = x.min()
    max_x = x.max()

    pearson = pearsonr(x, y)
    print(pearson)

    fig = go.Figure()
    if highlight:
        fig.add_trace(go.Scatter(x=fst["WEIR_AND_COCKERHAM_FST"], 
                y=param_sum["median"][~covered & ~outlier], 
                name="Non Outlier", mode="markers"))
        fig.add_trace(go.Scatter(x=fst["WEIR_AND_COCKERHAM_FST"], 
                y=param_sum["median"][covered & ~outlier], 
                name="Excess Ancestry", mode="markers"))
        fig.add_trace(go.Scatter(x=fst["WEIR_AND_COCKERHAM_FST"], 
                y=param_sum["median"][~covered & outlier], 
                name="Outlier", mode="markers"))
        fig.add_trace(go.Scatter(x=fst["WEIR_AND_COCKERHAM_FST"], 
                y=param_sum["median"][covered & outlier], 
                name="Excess Ancestry and Outlier", mode="markers"))
    
    else: 
        fig.add_trace(go.Scatter(x=x, y=y, mode="markers"))
    # fig.add_trace(go.Scatter(x=linspace, y=y_line, mode="lines"))
    fig.show()

# Read in fst estimates and replace negatives with 0
fst = pd.read_csv(os.path.join(outDir, name + "-mean-fst.csv"))
neg = fst["WEIR_AND_COCKERHAM_FST"] < 0 
fst[neg] = 0

pearson_correlation(fst, alpha, alpha_covered, alpha_out)
pearson_correlation(fst, beta, beta_covered, beta_out)


## Plot histogram of fst
# import plotly.express as px
# fig = px.histogram(fst, x="WEIR_AND_COCKERHAM_FST")
# fig.show()




