#!/bin/bash

# See `man sbatch` or https://slurm.schedmd.com/sbatch.html for descriptions
# of sbatch options.
#SBATCH --job-name=pivus_pileup
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=interactive
#SBATCH --account=default
#SBATCH --time=6:00:00

module load samtools

samtools mpileup -l /srv/gsfs0/projects/montgomery/mgloud/projects/pivus/data/annot.bed -s /srv/gsfs0/projects/montgomery/bballiu/PIVUS/DATA/RNAseq/BAM_FILTERED/$1 > /scratch/users/mgloud/pileup/$1.pileup

