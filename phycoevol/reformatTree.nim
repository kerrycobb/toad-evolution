import phylogeni
import regex
import tables
import strutils
import npeg

type 
  Extended = OrderedTable[string, string]

proc parseAnnotation(p: var NewickParser[Extended], annotation:string) =
  var p = p
  let par = peg "parser":
    num     <- >*(Digit | {'.', 'e', '-'})
    key     <- >*(Alnum | '_')
    val     <- >num
    list    <- >('{' * num * ',' * num * '}') 
    pair    <- key * '=' * (list | val): 
      p.currNode.data[$1] = $2
    parser  <- pair * *(',' * pair)
  let r = par.match(annotation)

  # let annotations = annotation.split(",")
  # for i in annotations: 
  #   let split = i.split("=")
  #   if len(split) == 2:
  #     p.currNode.data[split[0]] = split[1]

proc writeAnnotation(node: Node[Extended], str: var string) = 
  # discard
  str.add("[&&NHX")
  if not node.isLeaf:
    str.add(":height=")
    str.add((parseFloat(node.data["index_height_mean"])/1000000).formatFloat(ffDecimal,1))
    str.add(":freq=")
    str.add(node.data["node_freq"])
    str.add(":index_height_hpdi_95=")
    str.add(node.data["index_height_hpdi_95"])
  str.add("]")

let 
  path = "clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1/map-tree.nex"
  contents = readFile(path)
var 
  m: RegexMatch2
  newick: string
if find(contents, re2"BEGIN TREES;\n\s+TREE tree1 = \[&R\] (.+)\nEND;", m):
  newick = contents[m.group(0)]

var tree = treeFromString(newick, Extended)

# Remove debilis
for node in tree.preorder:
  if node.label == "debilis":
    tree.prune(node)

# for node in tree.preorder:
#     echo node.label
#     echo node.data 


# Rescale branch lengths
for node in tree.preorder: 
  node.length = node.length / 1000000
  if not node.isLeaf:
    node.label = node.data["node_freq"]

# Add branch length to root
tree.root.length = 2

tree.ladderize()

tree.writeNewickFile("clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1/map-tree.newick")