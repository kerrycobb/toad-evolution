#!/usr/bin/env python

import fire
import subprocess
import textwrap

def gen(sp, file, name, k):
    s = r"""
    \documentclass[border=10pt,varwidth=30cm]{{standalone}}
    \usepackage{{graphicx}}
    \usepackage[export]{{adjustbox}} % Needed for letters to align with top
    \usepackage{{tikz}}
    \usepackage{{multirow}}
    \begin{{document}}
    \begin{{figure}}
    \begin{{tabular}}[t]{{cc}}
        \multicolumn{{2}}{{c}}{{\Large \textit{{{sp}}} Population Structure}} \\
      {{\textbf{{\large A)}}}} & \includegraphics[valign=t,width=0.5\textwidth]{{../structure/plots/{name}-K-{k}.pdf}} \\ \vspace{{1mm}}
      {{\textbf{{\large B)}}}} & \includegraphics[valign=t,width=0.5\textwidth]{{../maps/out/structure-{name}-K-{k}.pdf}} \\
      {{\textbf{{\large C)}}}} & \includegraphics[valign=t,width=0.25\textwidth]{{../pca/out-plots/{name}-pca.pdf}} \\
    \end{{tabular}}
    \end{{figure}}
    \end{{document}}
    """.format(sp=sp, name=name, k=k)
    with open(file, "w") as fh:
        fh.write(textwrap.dedent(s))
    subprocess.run(f"build-pop-struct.sh {file}", shell=True)

if __name__ == '__main__':
    fire.Fire(gen)