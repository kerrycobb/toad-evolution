import dendropy as dp


tree = dp.Tree.get(path="TreePL-Rooted_Anura_bestTree_confidence_intervals.tre", 
                   schema="nexus", extract_comment_metadata=True)

inci_anax = tree.mrca(taxon_labels=["Anaxyrus punctatus", "Incilius nebulifer"]) 
print(inci_anax.annotations["height"])

punc_amer = tree.mrca(taxon_labels=["Anaxyrus punctatus", "Anaxyrus americanus"])
print(punc_amer.annotations["height"])