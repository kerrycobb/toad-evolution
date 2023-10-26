library(ape)
# library(phytools)
library(ggplot2)
library(ggtree)
library(treeio)

genus_map <- list(
  "woodhousii"   = "A. woodhousii",
  "fowleri"      = "A. fowleri",
  "terrestris"   = "A. terrestris",
  "americanus"   = "A. americanus",
  "hemiophrys"   = "A. hemiophrys",
  "baxteri"      = "A. baxteri",
  "microscaphus" = "A. microscaphus",
  "speciosus"    = "A. speciosus",
  "cognatus"     = "A. cognatus",
  "quercicus"    = "A. quercicus",
  "punctatus"    = "A. punctatus",
  "debilis"      = "A. debilis",
  "nebulifer"    = "I. nebulifer"
)

# path <- "clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1/map-tree.newick"
path <- "clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1/map-tree.nex"
out <- "clust-80-indel-16-snps-0p3-samples-25-include-phyco-neb-1-tree.pdf" 

# tree <- read.nhx(path)
tree <- read.beast(path)
# print(str(tree))


tree <- drop.tip(tree, "debilis")
tree@phylo <- ladderize(tree@phylo)

# Replace tip labels
tree@phylo$tip.label <- sapply(tree@phylo$tip.label, function(label) {
  if (label %in% names(genus_map)) {
    return(genus_map[[label]])
  } else {
    return(label)
  }
})


p <- ggtree(tree, mrsd="00-01-01", ladderize=FALSE) 
p <- revts(p) +
  theme_tree2() +
  scale_x_continuous(labels=function(l){abs(l/1000000)} ) +
  geom_tiplab(as_ylab=TRUE, size=10) + 
  geom_rootedge() + 
  geom_range("index_height_hpdi_95", color="red", size=2, alpha=0.6) +
  # geom_text(aes(label=node)) + # Use this to get node indexes
  geom_text2(size=2.5, hjust=1.1, nudge_y=-0.15, 
      aes(label=(paste0(sprintf("%0.1f", split_height_mean / 1000000), " / ", substring(node_freq, 1, 4))),
      subset=c(F,F,F,F,F,F,F,F,F,F,F,F,T,T,T,T,T,T,T,T,T,F)
      )) + 
  geom_text2(size=2.5, hjust=1.1, nudge_y=0.15, 
      aes(label=(paste0(sprintf("%0.1f", split_height_mean / 1000000), " / ", substring(node_freq, 1, 4))),
      subset=c(F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,T)
      )) +
  labs(caption="Divergence time (million years ago)")  

ggsave(out, plot=p)
