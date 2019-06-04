for file in `ls /scratch/users/mgloud/pileup/*pileup.gz`; do
	f=`basename $file`
	sbatch submit_quant.sh $f
done
