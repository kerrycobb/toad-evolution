
# Interactive maps
```bash
./interactive-map.py ../popmap-all.txt out/interactiv-samples-all.html 
./interactive-map.py ../popmap-hybrid-zone.txt out/interactive-samples-hybrid-zone.html 
```

# Sample Maps
```bash
./sample-map.py \
  ../popmap-all.txt \
  out/samples-all.pdf

./sample-map.py \
  ../popmap-americanus-group.txt \
  out/samples-americanus.pdf

./sample-map.py \
  ../popmap-non-americanus-group.txt \
  out/samples-non-americanus-group.pdf
```

# Structure Maps
```bash

## Americanus group
./structure-map.py americanus-group-minSamples1.0-mac3-popmap2-K-4
./structure-map.py americanus-group-minSamples1.0-mac3-popmap2-K-5

./structure-map.py americanus-group-minSamples95-mac3-popmap2-K-4
./structure-map.py americanus-group-minSamples95-mac3-popmap2-K-5

## Americanus
./structure-map.py americanus-minSamples1.0-mac3-popmap2-K-2
./structure-map.py americanus-minSamples1.0-mac3-popmap2-K-3
./structure-map.py americanus-minSamples1.0-mac3-popmap2-K-4

./structure-map.py americanus-minSamples99-mac3-popmap3-K-2
./structure-map.py americanus-minSamples99-mac3-popmap3-K-3
./structure-map.py americanus-minSamples99-mac3-popmap3-K-4

## Fowleri
./structure-map.py fowleri-minSamples1.0-mac3-popmap2-K-2
./structure-map.py fowleri-minSamples1.0-mac3-popmap2-K-3
./structure-map.py fowleri-minSamples1.0-mac3-popmap2-K-4

./structure-map.py fowleri-minSamples95-mac3-popmap2-K-2
./structure-map.py fowleri-minSamples95-mac3-popmap2-K-3
./structure-map.py fowleri-minSamples95-mac3-popmap2-K-4

## Terrestris
./structure-map.py terrestris-minSamples1.0-mac3-popmap2-K-2
./structure-map.py terrestris-minSamples1.0-mac3-popmap2-K-3
./structure-map.py terrestris-minSamples1.0-mac3-popmap2-K-4

./structure-map.py terrestris-minSamples1.0-mac3-popmap3-K-2
./structure-map.py terrestris-minSamples1.0-mac3-popmap3-K-3
./structure-map.py terrestris-minSamples1.0-mac3-popmap3-K-4

## Woodhousii
./structure-map.py woodhousii-minSamples1.0-mac3-popmap3-K-2
./structure-map.py woodhousii-minSamples1.0-mac3-popmap3-K-3
./structure-map.py woodhousii-minSamples1.0-mac3-popmap3-K-4

./structure-map.py woodhousii-minSamples80-mac3-K-2
./structure-map.py woodhousii-minSamples80-mac3-K-3
./structure-map.py woodhousii-minSamples80-mac3-K-4

./structure-map.py woodhousii-minSamples80-mac3-popmap2-K-2
./structure-map.py woodhousii-minSamples80-mac3-popmap2-K-3
./structure-map.py woodhousii-minSamples80-mac3-popmap2-K-4
```

# Hybrid Zone Structure Maps
```bash
./structure-map-hybrid.py hybrid-zone-minSamples1.0-mac3-popmap2-K-2 \
--labels "americanus,terrestris"

./structure-map-hybrid.py hybrid-zone-minSamples95-mac3-popmap2-K-2 \
--labels "americanus,terrestris"

./structure-map-hybrid.py hybrid-zone-minSamples1.0-mac3-popmap3-K-2 \
--labels "americanus,terrestris"

./structure-map-hybrid.py hybrid-zone-minSamples95-mac3-popmap3-K-2 \
--labels "americanus,terrestris"
```