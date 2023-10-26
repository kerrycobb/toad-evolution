
# Population structure figures
```bash
  ./gen_pop_struct_fig.py "A. americanus" pop-structure-americanus.tex americanus-minSamples99-mac3-popmap3 3 
  ./gen_pop_struct_fig.py "A. fowleri" pop-structure-fowleri.tex fowleri-minSamples1.0-mac3-popmap2 2 
  ./gen_pop_struct_fig.py "A. terrestris" pop-structure-terrestris.tex terrestris-minSamples1.0-mac3-popmap3 2 
  ./gen_pop_struct_fig.py "A. woodhousii" pop-structure-woodhousii.tex woodhousii-minSamples1.0-mac3-popmap3 2

  ./gen_pop_struct_fig.py "A. fowleri + A. woodhousii" pop-structure-fowleri-woodhousii.tex fowleri-woodhousii-minSamples1.0-mac3 2

```
Copy americanus file for also showing K=2
Edit the americanus .tex files, change title and remove PCA from plot with K=2
Rerun build

```bash
build-pop-struct.sh pop-structure-americanus.tex
build-pop-struct.sh pop-structure-americanus2.tex
```