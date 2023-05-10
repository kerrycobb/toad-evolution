#!/usr/bin/env Rscript --vanilla

library(argparse)
library(pophelper)
library(gridExtra)
library(ggplot2)

width <- 12 
height <- 3 

parser <- ArgumentParser()
parser$add_argument("-k", "--selectK", default=NULL)
# parser$add_argument("-l", "--labels", default=NULL)
parser$add_argument("-c", "--colors")
parser$add_argument("-p", "--popmap", default=NULL)
parser$add_argument("--showindlabel", action='store_true', default=FALSE)
parser$add_argument("directory", nargs=1)
parser$add_argument("colors", nargs=1)
args <- parser$parse_args()

dir <- gsub("/$", "", args$directory)
name <- gsub("^out-", "", dir) 
colors <- readLines(args$colors)

# Read in data files
files <- list.files(dir, full.names=TRUE)
qlist <- readQ(files=files, filetype="structure", indlabfromfile=TRUE)
t <- tabulateQ(qlist=qlist)

# Make column with iteration number and sort by k and iteration 
t$iter <- sapply(strsplit(t$file, "\\-|\\."),
  function(x) as.numeric(gsub("^I", "", x[length(x) - 2])))
t <- t[order(t$k, t$iter), ]

# Get number of iterations with K=1 and subset t
nrows_k1 <- sum(t$k==1)
sub_t <- t[(nrows_k1 + 1): nrow(t), ]

# Align and merge subset of files
aligned <- alignK(qlist[(nrows_k1+1):length(qlist)])
merged <- mergeQ(aligned)

################################################################################
# If not K given, plot all runs, and output merged plot for each K
if (is.null(args$selectK)) {

  # Write merged qmatrix to csv file
  for (n in names(merged)) {
    write.csv(merged[[n]], paste0("qmats/", name, "-K-", n, ".csv"))
  }

  # Evanno
  s <- summariseQ(t)
  evanno <- evannoMethodStructure(data=s, exportplot=FALSE, returnplot=TRUE, 
      returndata=FALSE, basesize=12, linesize=0.7)
  pdf(file=paste0("plots/", name, "-evanno.pdf"))
  grid.arrange(evanno)
  invisible(dev.off())

  # Plot All Runs
  plotQ(
    aligned,
    imgoutput="join",
    returnplot=FALSE,
    exportplot=TRUE,
    imgtype="pdf",
    exportpath="plots",
    outputfilename=paste0(name, "-all-runs"),
    clustercol=colors,
    splab=paste0("K=", sub_t$k, "\nRun ", sub_t$iter),
    basesize=11
  )
  
  # Plot merged, all K
  plotQ(
      merged,
      imgoutput="join",
      outputfilename=paste0(name, "-merged-all-k"),
      exportpath="plots",
      imgtype="pdf",
      exportplot=T,
      returnplot=F,
      clustercol=colors,
      splab=paste0("K=", names(merged)),
      sortind="Cluster1",
      showindlab=args$showindlab,
      showticks=args$showindlab,
      useindlab=TRUE,
      sharedindlab=TRUE,
    #   exportplot=F, 
    #   basesize=11,
  )

################################################################################
  # Make plot for given value of K
} else {
  k <- args$selectK

  sampleData <- read.csv("../sample-data.csv")
  sampleData <- sampleData[!duplicated(sampleData$sample_id),] 
  sampleDataMerge <- merge(merged[[k]], sampleData, by.x=0, by.y="sample_id", all.x=TRUE) 
  sampleDataMerge$proj_id <- gsub("^_", "", sampleDataMerge$proj_id)
 
  path <- paste0("plots/", name, "-K-", k, ".pdf")

  ##############################################################################
    # Without popmap 
  if (is.null(args$popmap)) {
    rownames(merged[[k]]) <- sampleDataMerge$proj_id 
    p <- plotQ(
      merged[k], 
      exportplot=FALSE, 
      returnplot=TRUE, 
      clustercol=colors, 
      sortind="Cluster1",
      showindlab=args$showindlab,
      showticks=args$showindlab,
      useindlab=TRUE,
      indlabsize=10,
      splabsize=0,
      # ticksize=0.1,
      # indlabspacer=0.25,
      # barbordercolour="black",
    )

  ##############################################################################
  # Make plot, grouping by label
  } else {

    popmap <- read.table(args$popmap, header=FALSE, sep = "\t")
    pops <- merge(merged[k], popmap, by.x=0, by.y="V1", all.x=TRUE, all.y=FALSE)
    pops <- pops["V2"]  
    rownames(merged[[k]]) <- sampleDataMerge$proj_id 

    p <- plotQ(
      merged[k], 
      exportplot=FALSE, 
      returnplot=TRUE, 
      clustercol=colors, 
      sortind="Cluster1",
      grplab=pops,
      ordergrp=TRUE,
      grplabsize=5,
      showindlab=args$showindlab,
      showticks=args$showindlab,
      useindlab=TRUE,
      indlabsize=9,
      indlabvjust=1,
      splabsize=0,
      # splab="",
      # pointsize=6,
      # linesize=7,
      # linealpha=0.2,
      # pointcol="white",
      # grplabpos=0.5,
      # linepos=0.5,
      # grplabheight=0.75,
      # indlabspacer=0.25,
      # barbordercolour="black",
    )
  }
  ggsave(path, p$plot[[1]], width=width, heigh=height, units="in")
  print(paste("Plot written to ", path))
}
