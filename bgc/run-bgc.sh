#!/usr/bin/env bash

NAME=${1%/} # Remove trailing slash
CHAIN=$2
OUTDIR=out-$NAME/
# BGC_AMER=$NAME/bgc-americanus.bgc
# BGC_TERR=$NAME/bgc-terrestris.bgc
# BGC_ADM=$NAME/bgc-admixed.bgc

MCMC_SAMPLES=1000000
THIN=1000

sbatch \
  --job-name bgc-$NAME-$CHAIN \
  --output $OUTDIR"/%x-%j.out" \
  --partition jro0014_amd \
  --time=2-00:00:00 \
  --cpus-per-task 1 \
  --mem 20GB \
  --wrap "\
    bgc \
      -a $OUTDIR/data-americanus.bgc \
      -b $OUTDIR/data-terrestris.bgc \
      -h $OUTDIR/data-admixed.bgc \
      -x $MCMC_SAMPLES \
      -t $THIN \
      -p 1 \
      -q 1 \
      -s 1 \
      -F $OUTDIR/${NAME}_${CHAIN}"

# -a Infile with genetic data for parental population 0. 
# -b Infile with genetic data for parental population 1. 
# -h Infile with genetic data for admixed population(s).
# -F Prefix added to all outfiles.
# -x Number of MCMC steps for the analysis [default = 1000].
# -n Discard the first n MCMC samples as a burn-in [default = 0]. 
# -t Thin MCMC samples by recording every nth value [default = 1].
# -p Specifies which parameter samples to print: 0 = print log likelihood, alpha, beta, and hybrid index, 1 = also print precision parameters, 2 = also print eta and kappa [default = 0].
# -q Boolean,calculateandprintclineparameterquantiles[default=0].Clineparameter quantiles can be used to designate outlier loci.
# -i Boolean, calculate and print interspecific-heterozygosity [default = 0]. This option should only be turned on if most loci exhibit fixed or nearly fixed differences between the parental species.
# -s Boolean, sum-to-zero constraint on locus cline parameters [default = 1]. This con- strains all γ (locus affect on cline center, α) and ζ (locus affect on cline rate, β) to sum-to-zero. Population affects are not similarly constrained.
# -I Select algorithm to initialize MCMC [default = 1]. 0 = use information from the data to initialize ancestry and hybrid index, 1 = do not use information from the data to initialize ancestry and hybrid index.
# -T If non-zero, use a truncated gamma prior for tau with this upper bound [default = 0]. Otherwise use a full gamma prior.
# -u MCMC tuning parameter, maximum deviate from uniform for proposed hybridindex hybrid index [default = 0.1].
# -g MCMC tuning parameter, standard deviation for Gaussian proposal of cline parameter gamma [default = 0.05].
# -z MCMC tuning parameter, standard deviation for Gaussian proposal of cline parameter zeta [default = 0.05].
# -e MCMC tuning parameter, standard deviation for Gaussian proposal of cline parameters eta and kappa [default = 0.02].


# -N Boolean, use genotype-uncertainty model [default = 0]. This model should be used
# with next-generation sequence data.
# -m Boolean, use ICARrho model for linked loci [default = 0]. This model requires a
# physical or genetic map and implements the linkage model. The model uses the
# weight function from Gompert et al. (Eqn. S1.3; 2012b) with c1 = 1 , c2 = 0.6, 4NL
# and c3 = 20. Alternative weight models might be allowed in future versions of the
# software.
# -D Maximum distance between loci, free recombination [default = 0.5]. This is only used for the linkage model.
# -E Boolean, use sequence error model, only valid in conjunction with the genotype uncertainty model [default = 0]. A single error probability can be specified using the command-line (e.g., -E 0.001). Use -E 1 to provide locus-specific error proba- bilities, which are included in the infile for the admixed population(s).
