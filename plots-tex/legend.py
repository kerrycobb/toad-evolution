import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import subprocess

labels = ["americanus", "terrestris", "admixed"]
colors = [line.rstrip('\n') for line in open("../colors-hybrid.txt")]


f = lambda m,c: plt.plot([],[],marker=m, color=c, ls="none")[0]
handles = [f("s", colors[i]) for i in range(3)]
legend = plt.legend(handles, labels, loc=3, framealpha=1, frameon=False, handletextpad=-0.25)

fig  = legend.figure
fig.canvas.draw()
bbox  = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
fig.savefig("legend.pdf", dpi="figure", bbox_inches=bbox, pad_inches=0)
subprocess.call(["pdfcrop", "legend.pdf", "legend.pdf"])