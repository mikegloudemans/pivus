for f in `ls /scratch/users/mgloud/pileup/*pileup`; do
	sbatch bgzip.sh $f
done
