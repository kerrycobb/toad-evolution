import pandas as pd
import numpy as np
from jinja2 import Template

template = Template(r"""
\begin{longtable}{ {{ "l" * df.shape[1] }} }

% Header for first page
\caption{ {{ caption }}} \\
\hline

% Column names for first page
{% for col in df.columns -%}
    \multicolumn{1}{c}{ {{col}} }
    {%- if not loop.last %} & {% else %} \\ {% endif %} 
{% endfor -%}

\hline 
\endfirsthead

% Header for all but first page
\multicolumn{4}{c}%
{{ '{{' }} \tablename\ \thetable{} -- continued from previous page {{ '}}' }} \\
\hline

% Column names for all but first page
{% for col in df.columns -%}
    \multicolumn{1}{c}{ {{col}} }
    {%- if not loop.last %} & {% else %} \\ {% endif %} 
{% endfor -%}

\hline 
\endhead

% Footer for all but last page 
\hline 
\multicolumn{4}{r}{{ '{{' }}Continued on next page{{ '}}' }} \\
\endfoot
\hline 
\endlastfoot

% Table data
{% for index, row in df.iterrows() %}
    {% for value in row %}
        {{- value -}}
        {% if not loop.last %} & {% endif %}
    {% endfor %}
    {% if not loop.last %} \\ {% endif +%}
{% endfor %}

\label{table:{{ label }}}
\end{longtable}
""",
trim_blocks=True,
lstrip_blocks=True)


def makeTable(df, path, caption, label):
    out = template.render(df=df, caption=caption, label=label)
    with open(path, "w") as fh:
        fh.write(out)


df = pd.read_csv("sample-data-genbank.csv", na_filter=False)
df = df.rename(columns={
    "proj_id": "ID",
    "id": "Voucher",
    "genbank": "SRA",
    "species": "Species", 
    "hyb-zone-pass": "Passed Filter",
    "phylo-phycoeval": "Phycoeval",
    "phylo-structure": "Structure",
    "latitude": "Latitude",
    "longitude": "Longitude"})
df = df.drop_duplicates(subset=['sample_id'])
df["ID"] = df["ID"].str[1:]
df["genus"] = df["genus"].str.replace("Anaxyrus", "A.")
df["Species"] = df["genus"] + ' ' + df["Species"]
df["Species"] = "\\textit{" + df["Species"] + "}"
df["Latitude"] = df["Latitude"].apply(lambda x: '{0:.5f}'.format(x))
df["Longitude"] = df["Longitude"].apply(lambda x: '{0:.5f}'.format(x))


# Phylogeny Chapter tables
phyloCols = ["Voucher", "SRA", "Species", "Phycoeval", "Structure", "Latitude", "Longitude"]
phyloDf = df.loc[((df["phylo"] == "X") & ~(df["loaned"] == "X")), phyloCols]
makeTable(
    df=phyloDf,
    path="sample-table-phylogeny.tex",
    caption="-- Samples collected for this study",
    label="collectedPhylo")

phyloDfLoaned = df.loc[((df["phylo"] == "X") & (df["loaned"] == "X")), phyloCols]
makeTable(
    df=phyloDfLoaned, 
    path="sample-table-phylogeny-loaned.tex", 
    caption="-- Samples loaned from museum collections",
    label="loanedPhylo")


# Hybrid Zone Chapter tables
hybCols = ["ID", "Voucher", "SRA", "Species", "Passed Filter", "Latitude", "Longitude"]
hybDf = df.loc[((df["hyb-zone"] == "X") & ~(df["loaned"] == "X")), hybCols]
makeTable(
    df=hybDf,
    path="sample-table-hybrid-zone.tex",
    caption="-- Samples collected for this study",
    label="collectedHyb")

hybDfLoaned = df.loc[((df["hyb-zone"] == "X") & (df["loaned"] == "X")), hybCols]
makeTable(
    df=hybDfLoaned, 
    path="sample-table-hybrid-zone-loaned.tex", 
    caption="-- Samples loaned from museum collections",
    label="loanedHyb")

print("Number of Samples:")
print(f"Phylo Collected: {len(phyloDf)}")
print(f"Phylo Loaned: {len(phyloDfLoaned)}")
print(f"Phylo Total: {len(phyloDf) + len(phyloDfLoaned)}")
print(f"Hybrid Collected: {len(hybDf)}")
print(f"Hybrid Loaned: {len(hybDfLoaned)}")
print(f"Hybrid Total: {len(hybDf) + len(hybDfLoaned)}")