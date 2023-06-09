#!/usr/bin/env Rscript --vanilla

library(argparse)
library(adegenet)

parser <- ArgumentParser()
parser$add_argument("directory", nargs=1)
args <- parser$parse_args()

dir <- gsub("/$", "", args$directory)
name <- gsub("^out-", "", dir) 
# vcffile <- paste0(dir, "/populations.snps.vcf")
infile <- paste0(dir, "/", dir, ".stru")

data <- read.delim(infile, sep = "\t", header=FALSE)
nSamples <- nrow(data)/2
nLoci <- ncol(data)-1

input <- read.structure(infile, n.ind=nSamples, n.loc=nLoci, ask=FALSE, 
    onerowperind=FALSE, row.marknames=0, NA.char="-9", col.pop=0, col.lab=1)

cat("Missing data:")
cat(sum(is.na(input$tab)))
cat("\n")

# PCA
X <- tab(input, freq=TRUE, NA.method="mean")
pca <- dudi.pca(X, scale=FALSE, scannf=FALSE, nf=3)

print(pca)

pdf(paste0(dir, "/", name, "-eigenvalues-plot.pdf"))
barplot(pca$eig[1:50], main="PCA eigenvalues", col=heat.colors(50))
dev.off()

pdf(paste0(dir, "/", name, "-loading-plot.pdf"))
loadingplot(pca$c1^2)
dev.off()

writeLines(sapply(100*(pca$eig/sum(pca$eig)), toString), paste0(dir, "/prop-variance.txt"))
write.csv(pca$li, paste0(dir, "/principle-components.csv"))

cat("Finished running PCA")
cat("\n")

# Load sample data and set row names to match alignment names
# sampleData <- read.csv("~/Desktop/toad-project/toad-data.csv")
# sampleData <- sampleData[!duplicated(sampleData["rename"]),]
# rownames(sampleData) <- sampleData[,"rename"]

# # # Subset samples from sample data that is present in alignment
# # sampleNames <- unlist(dimnames(input@tab)[1])
# # sampleData <- sampleData[rownames(sampleData) %in% sampleNames,]

# # ggsave(paste0(dir, "/", name, "-eigenvalues.pdf"), device="pdf")

# # ggplot PCA plot
# # split <- strsplit(row.names(pca$li), '_')
# # df <- data.frame(pca$li, do.call(rbind, split))
# # ggplot(df, aes(x=Axis1, y=Axis2))# +
#   # geom_point(aes(color=X2), size=1)
# # ggsave(paste0(dir, "/", name, "-pca.pdf", device="pdf")

# # # Plotly PCA Plot
# # p <- plot_ly(x=df$Axis1, y=df$Axis2, z=df$Axis3, type="scatter3d", 
# #              mode="markers", color=df$X2, text=rownames(df))
# # p
# # saveWidget(p, "amer-terr-pca.html")

# # # dapc
# # grp <- find.clusters(X, max.n.clust=10)
# # dapc1 <- dapc(X, grp$grp)
# # dapc1$grp
# # scatter(dapc1)

# # sampleData["group"] <- NA
# # for (i in 1: length(dapc1$grp)){
# #   sampleData[names(dapc1$grp[i]), "group"] <- as.numeric(dapc1$grp[i]) 
# # }

# # write.csv(sampleData, "amer-terr-dapc-groups.csv", row.names=FALSE)

# # # Maps
# # xlim1 <- c(-96.5, -72)
# # ylim1 <- c(30, 47)
# # scale <- 110
# # linewidth <- 1
# # # countries <- ne_countries(scale=scale, returnclass="sf")
# # # coast <- ne_coastline(scale=scale, returnclass="sf")
# # states <- ne_states(country="united states of america", returnclass="sf")


# # map1 <- ggplot() +
# #   geom_sf(data=states) +
# #   # geom_sf(data=coast) +
# #   geom_point(data=sampleData, mapping=aes(x=longitude, y=latitude, text=rownames(sampleData), color=as.factor(group))) +
# #   coord_sf(xlim=xlim1, ylim=ylim1, expand=FALSE)
# # map1
# # p <- ggplotly(map1)
# # p
# # saveWidget(p, "amer-terr-dapc-map.html")

# # xlim2 <- c(-87, -85)
# # ylim2 <- c(32.5, 34)
# # ggplot() +
# #   geom_sf(data=states) +
# #   geom_point(data=sampleData, mapping=aes(x=longitude, y=latitude, color=as.factor(group))) +
# #   coord_sf(xlim=xlim2, ylim=ylim2, expand=FALSE)




# ################################################################################
# Using snprelate
# #!/usr/bin/env Rscript --vanilla

# library(argparse)
# library(adegenet)
# # library(ggplot2)
# # library(plotly)
# # library(gdsfmt)
# # library(SNPRelate)
# # library(dplyr)
# # library(tidyr)
# # library(ggmap)
# # library(rnaturalearth)
# # library(rnaturalearthdata)
# # library(sf)
# # library(htmlwidgets)

# parser <- ArgumentParser()
# parser$add_argument("directory", nargs=1)
# # parser$add_argument("-k", "--selectK", default=NULL)
# # parser$add_argument("-l", "--labels", default=NULL)
# # parser$add_argument("--showlegend", action='store_true', default=FALSE)
# # parser$add_argument("-p", "--popmap", default=NULL)
# # parser$add_argument("--showindlabel", action='store_true', default=FALSE)
# # parser$add_argument("directory", nargs=1)
# args <- parser$parse_args()

# dir <- gsub("/$", "", args$directory)
# name <- gsub("^out-", "", dir) 
# vcffile <- paste0(dir, "/populations.snps.vcf")
# infile <- paste0(dir, "/populations.snps.gds")

# snpgdsVCF2GDS(vcffile, infile) 
# snpgdsSummary(infile)
# genofile <- snpgdsOpen(infile)
# pca <- snpgdsPCA(genofile)

# df <- data.frame(sample=pca$sample.id, PC1=pca$eigenvect[,1], 
#     PC2=pca$eigenvect[,2], PC3=pca$eigenvect[,3], stringsAsFactors=FALSE)
# print(sum(pca$varprop))
# # Write variance proportion to file 
# writeLines(sapply(pca$varprop, toString), paste0(dir, "/eigenvalues.txt"))
# # Write principle components to file
# write.csv(df, paste0(dir, "/principle-components.csv"))

# # Plot Eigenvalues
# pdf(paste0(dir, "/", name, "-eigenvalues.pdf"))
# barplot(pca$eigenval[1:50], main="PCA eigenvalues", col=heat.colors(50))
# dev.off()