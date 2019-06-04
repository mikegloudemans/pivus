for file in `ls /srv/gsfs0/projects/montgomery/bballiu/PIVUS/DATA/RNAseq/BAM_FILTERED/*_sorted.bam`; do
	f=`basename $file`
	sbatch get_coverage_sbatch.sh $f
done
