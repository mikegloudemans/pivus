#!/bin/bash

# See `man sbatch` or https://slurm.schedmd.com/sbatch.html for descriptions
# of sbatch options.
#SBATCH --job-name=pivus_quant_bias
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=interactive
#SBATCH --account=default
#SBATCH --time=20:00:00
#SBATCH --mem=50GB

module load htslib
bgzip -f $1
tabix -f -s 1 -b 2 -e 2 $1.gz
