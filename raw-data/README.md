Run:

```bash
module load stacks
./i7-demux.sh
sbatch -J concat -o %x-%j.out --wrap "./concatenate.fish"
```