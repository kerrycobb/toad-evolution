#!/usr/bin/env python

from ete3 import Tree, TreeStyle, faces, NodeStyle, AttrFace
import pandas as pd
import fire 


def plot(path, output1, output2, outgroup):
    df = pd.read_csv("../sample-data.csv").set_index("sample_id")
    df = df[~df.index.duplicated(keep="first")]
    d = df.to_dict("index")

    def layout1(node):
        node.img_style["size"] = 0
        node.img_style["vt_line_width"] = 1 
        node.img_style["hz_line_width"] = 1 
        if node.is_leaf():
            # id = d[node.name]["proj_id"][1:] 
            id = d[node.name]["id"] 
            sp = d[node.name]["species"]
            if sp == "nebulifer":
                gen = "Incillius" 
            else:
                gen = "A."
            text = faces.TextFace(f"{id} {gen} {sp}")
            text.margin_left = 5
            faces.add_face_to_node(text, node, column=0)
        # else:
        #     if node.support >= 100:
        #         node.img_style["size"] = 4 
        #         node.img_style["fgcolor"] = "black"
        #     elif node.support >= 70:
        #         node.img_style["size"] =4 
        #         node.img_style["fgcolor"] = "gray"
    
    def layout2(node):
        node.img_style["size"] = 0
        node.img_style["vt_line_width"] = 2 
        node.img_style["hz_line_width"] = 2 
        if node.is_leaf():
            text = faces.TextFace(node.name, fsize=20)
            text.margin_left = 5
            faces.add_face_to_node(text, node, column=0)
        else:
            if node.support != 1: 
                supp = faces.TextFace("{:.0f}".format(node.support), fsize=12)
                supp.margin_right = 2 
                node.add_face(supp, column=0, position="branch-bottom")


    t = Tree(path)
    t.set_outgroup(outgroup)
    t.ladderize(direction=0)
    # print(t.features["support"])
    # t.support =  
    ts = TreeStyle()
    # ts.show_branch_support = True
    ts.layout_fn = layout1
    ts.show_leaf_name = False
    ts.scale_length = 0.0025
    # t.show(tree_style=ts)
    t.render(output1, tree_style=ts)

    amer = t.get_common_ancestor("inhs17016", "utep20921")
    baxt = t.get_common_ancestor("msb92691", "msb92692")
    fowl = t.get_common_ancestor("utep19941", "utep19943")
    spec = t.get_common_ancestor("utep21885", "utep21884")
    terr = t.get_common_ancestor("kac230", "aht5278")
    wood = t.get_common_ancestor("hera20415", "utep21886")

    amer.dist = amer.dist + (amer.get_farthest_leaf()[1] + amer.get_closest_leaf()[1]) / 2
    baxt.dist = baxt.dist + (baxt.get_farthest_leaf()[1] + baxt.get_closest_leaf()[1]) / 2
    fowl.dist = fowl.dist + (fowl.get_farthest_leaf()[1] + fowl.get_closest_leaf()[1]) / 2
    spec.dist = spec.dist + (spec.get_farthest_leaf()[1] + spec.get_closest_leaf()[1]) / 2
    terr.dist = terr.dist + (terr.get_farthest_leaf()[1] + terr.get_closest_leaf()[1]) / 2
    wood.dist = wood.dist + (wood.get_farthest_leaf()[1] + wood.get_closest_leaf()[1]) / 2

    aht3413 = t.search_nodes(name="aht3413")[0]
    cogn = t.search_nodes(name="msb104677")[0] 
    hemi = t.search_nodes(name="msb104681")[0] 
    micr = t.search_nodes(name="msb100793")[0]  
    nebu = t.search_nodes(name="kac243")[0]
    punc = t.search_nodes(name="kac062")[0] 
    quer = t.search_nodes(name="aht2544")[0] 

    t.prune([amer, baxt, fowl, spec, terr, wood, aht3413, cogn, hemi, micr, nebu, punc, quer])

    amer.name = "A. americanus"
    baxt.name = "A. baxteri"
    fowl.name = "A. fowleri"
    spec.name = "A. speciosus"
    terr.name = "A. terrestris"
    wood.name = "A. woodhousii"
    aht3413.name = "A. fowleri - sample 006"
    cogn.name = "A. cognatus"
    hemi.name = "A. hemiophrys"
    micr.name = "A. microscaphus"
    nebu.name = "Incillius nebulifer"
    punc.name = "A. punctatus"
    quer.name = "A. quercicus"

    ts = TreeStyle()
    # ts.show_branch_support = True
    ts.layout_fn = layout2
    ts.show_leaf_name = False
    ts.scale = 30000 
    ts.scale_length = 0.0025
    ts.branch_vertical_margin = 30
    # t.show(tree_style=ts)
    t.render(output2, tree_style=ts)



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