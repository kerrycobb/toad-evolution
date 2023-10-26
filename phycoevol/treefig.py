from ete3 import Tree, TreeStyle, NodeStyle, AttrFace, TextFace, RectFace, faces

genus_map = dict( 
  woodhousii =   "A. woodhousii",
  fowleri =      "A. fowleri",
  terrestris =   "A. terrestris",
  americanus =   "A. americanus",
  hemiophrys =   "A. hemiophrys",
  baxteri =      "A. baxteri",
  microscaphus = "A. microscaphus",
  speciosus =    "A. speciosus",
  cognatus =     "A. cognatus",
  quercicus =    "A. quercicus",
  punctatus =    "A. punctatus",
  debilis =      "A. debilis",
  nebulifer =    "I. nebulifer")

path = "clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1/map-tree.newick"
out = "clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1-tree.pdf"
tree = Tree(path, format=0)

root = tree.get_tree_root()
root.dist = 0.002

for node in tree.traverse():
    nstyle = NodeStyle()
    # nstyle["vt_line_width"] = 1 
    # nstyle["hz_line_width"] = 1 
    if node.is_leaf():
        nstyle["size"] = 0
        # text = TextFace(genus_map[node.name], fsize=12)
        text = TextFace(genus_map[node.name])
        text.margin_left = 5
        node.add_face(text, column=0)
    else:
        if round(node.support, 2) >= 0.99:
            nstyle["fgcolor"] = "black"
            # nstyle["size"] = 3 
        else:
            nstyle["size"] = 0
    node.set_style(nstyle)

ts = TreeStyle()
ts.show_leaf_name = False
# ts.branch_vertical_margin = 15 
# tree.show(tree_style=ts)
# ts.scale = 2000
tree.render(out, w=100, units="px", tree_style=ts)
# tree.render(out, tree_style=ts)



# from ete3 import Tree, TreeStyle, NodeStyle, AttrFace, TextFace, RectFace, faces

# genus_map = dict( 
#   woodhousii =   "A. woodhousii",
#   fowleri =      "A. fowleri",
#   terrestris =   "A. terrestris",
#   americanus =   "A. americanus",
#   hemiophrys =   "A. hemiophrys",
#   baxteri =      "A. baxteri",
#   microscaphus = "A. microscaphus",
#   speciosus =    "A. speciosus",
#   cognatus =     "A. cognatus",
#   quercicus =    "A. quercicus",
#   punctatus =    "A. punctatus",
#   debilis =      "A. debilis",
#   nebulifer =    "I. nebulifer")

# path = "clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1/map-tree.newick"
# out = "clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1-tree.pdf"
# tree = Tree(path, format=0)

# root = tree.get_tree_root()
# root.dist = 0.002

# for node in tree.traverse():
#     nstyle = NodeStyle()
#     nstyle["vt_line_width"] = 1 
#     nstyle["hz_line_width"] = 1 
#     if node.is_leaf():
#         nstyle["size"] = 0
#         # text = TextFace(genus_map[node.name], fsize=12)
#         text = TextFace(genus_map[node.name])
#         text.margin_left = 5
#         node.add_face(text, column=0)
#     else:
#         if round(node.support, 2) >= 0.99:
#             nstyle["fgcolor"] = "black"
#             nstyle["size"] = 3 
#         else:
#             nstyle["size"] = 0
#     node.set_style(nstyle)

# ts = TreeStyle()
# ts.show_leaf_name = False
# ts.branch_vertical_margin = 15 
# # tree.show(tree_style=ts)
# # ts.scale = 2000
# tree.render(out, w=2000, units="px", tree_style=ts)
# # tree.render(out, tree_style=ts)