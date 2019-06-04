# PIVUS 3' bias quantification pipeline
# Author: Mike Gloudemans
# Date completed: 6/4/2019

# Create BED file for samtools mpileup (fast)
bash subset_bed_columns.sh

# Run samtools mpileup to get coverage (takes a few hours
# and creates 5+ TB of files)
bash get_coverage.sh

# Bgzip and tabix coverage files for easy access
# (takes a little while, but only required the first time)
bash bgzip.sh

# Get per-sample reads in each transcript (takes a few hours)
bash get_feature_counts_wrapper.sh

# Make matrix of 3' biases (fast, runs in minutes)
python make_bias_matrices.py

# Visualize data in R
Rscript visualize.R

