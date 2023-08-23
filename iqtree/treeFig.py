#!/usr/bin/env python

# import ete3 as et
from ete3 import Tree, TreeStyle, faces, NodeStyle, AttrFace
import pandas as pd
import fire 


def plot(path, output):
    df = pd.read_csv("../sample-data.csv").set_index("sample_id")
    df = df[~df.index.duplicated(keep="first")]
    d = df.to_dict("index")


    def layout(node):
        node.img_style["size"] = 0
        if node.is_leaf():
            id = d[node.name]["id"] 
            sp = d[node.name]["species"]
            text = faces.TextFace(f"{id} {sp}")
            text.margin_left = 5
            faces.add_face_to_node(text, node, column=0)
        else:
            pass 


    t = Tree(path)
    t.set_outgroup("hera10484")
    t.ladderize(direction=0)
    ts = TreeStyle()
    ts.show_branch_support = True
    ts.layout_fn = layout
    ts.show_leaf_name = False
    # t.show(tree_style=ts)
    t.render(output, tree_style=ts)

# def layout(node):
#     if node.is_leaf():
#         node.set_style(NodeStyle(dict(size=0)))
#         search = df[df["id"] == node.name]
#         if len(search) == 1:
#             row = search.iloc[0]
#             if row["Cluster1"] > 0.9:
#                 node.set_style(NodeStyle(dict(fgcolor="blue")))
#             elif row["Cluster2"] > 0.9:
#                 node.set_style(NodeStyle(dict(fgcolor="red")))
#             elif row["Cluster3"] > 0.9: 
#                 node.set_style(NodeStyle(dict(fgcolor="green")))
#             else:
#                 node.set_style(NodeStyle(dict(fgcolor="pink")))
#     else:
#         node.set_style(NodeStyle(dict(size=0)))


    # ts = et.TreeStyle()
# ts.branch_vertical_margin = 1
# ts.layout_fn = layout
    # ts.scale = 10000 


# ns = et.NodeStyle()
# ns["size"] = 0
# t.set_style(ns)
# for n in t.traverse():
    # n.set_style(ns)

# for n in t.iter_leaves():
#     search = df[df["id"] == n.name]
#     if len(search) == 1:
#         row = search.iloc[0]
#         if row["Cluster1"] > 0.95:
#             n.set_style(NodeStyle(dict(fgcolor="blue")))
#         if row["Cluster2"] > 0.95:
#             n.set_style(NodeStyle(dict(fgcolor="")))
#         if row["Cluster3"] > 0.95: 
#             n.set_style(NodeStyle(dict(fgcolor="green")))



#     n.set_style(ns)

    # t.show(tree_style=ts)


if __name__ == "__main__":
    fire.Fire(plot)