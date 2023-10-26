import phylogeni

var 
  n = parseNexusFile("TreePL-Rooted_Anura_bestTree_confidence_intervals.tre")
  t = n[1].trees[0].tree

for i in t.preorder:
  if i.isLeaf:
    i.label = n[1].translate[i.label]

let 
  nebu = t.find("Incilius_nebulifer")
  punc = t.find("Anaxyrus_punctatus")
  cano = t.find("Anaxyrus_canorus")
  amer = t.find("Anaxyrus_americanus")
  micr = t.find("Anaxyrus_microscaphus")
  incil_anax = mrca(nebu, punc) 
  anax = mrca(cano, amer) 
  punc_anax = mrca(punc, amer)
  amer_group = mrca(amer, micr)

echo anax.ascii

echo "\nIncilius-Anaxyrus split: " & $incil_anax.data
echo "\nAnaxyruys MRCA: " & $anax.data
echo "\nAnaxyrus-punctatus split: " & $punc_anax.data
echo "\namer_group.data: " & $amer_group.data
