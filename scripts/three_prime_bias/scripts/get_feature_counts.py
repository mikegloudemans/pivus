import os
import sys
import pickle
import subprocess

if sys.version_info[0] < 3:
   from StringIO import StringIO
else:
   from io import StringIO

indiv = sys.argv[1]

# Create a dictionary to store counts per gene
gene_counts = {}

# Create a dictionary to store 3' counts per gene
three_counts = {}

# Load feature list from annotation file
# Keep track of all bases that fall within each gene

for current_chrom in ["chr" + str(num) for num in range(1, 23)]:

	bases_to_genes = {}
	gene_map = {}
	three_map = {}

	# Build gene index
	with open("/srv/gsfs0/projects/montgomery/lfresard/WHI_rawdata/gencode.v19.annotation.gtf") as f:
		for line in f:
			if line.startswith("#"):
				continue
			data = line.strip().split()
			if not data[2] == "exon":
				continue
			gene = data[11].replace('"', '').replace(";", "")

			chrom = data[0]
			if chrom != current_chrom:
				continue
			start = int(data[3])
			end = int(data[4])
			strand = data[6]

			if gene not in gene_map:
				gene_map[gene] = {}
				gene_map[gene]["bases"] = set([])
				gene_map[gene]["strand"] = strand

			for i in xrange(start, end+1):
				gene_map[gene]["bases"].add(i)
				if i not in bases_to_genes:
					bases_to_genes[i] = []
				bases_to_genes[i].append(gene)

	# Build 3' index
	for gene in gene_map:
		if gene_map[gene]["strand"] == "+":
			three_map[gene] = set(sorted(list(gene_map[gene]["bases"]), reverse=True)[:min(100, len(list(gene_map[gene]["bases"])))])
		else:
			three_map[gene] = set(sorted(list(gene_map[gene]["bases"]))[:min(100, len(list(gene_map[gene]["bases"])))])

	subprocess.check_output("tabix /scratch/users/mgloud/pileup/{1} {0}:1-1000000000 > /scratch/users/mgloud/{1}.tmp".format(current_chrom, indiv), shell=True)

	with open("/scratch/users/mgloud/{0}.tmp".format(indiv)) as f:

		# Go through the file one line at a time, reading counts and position only

		i=0
		for line in f:
			i += 1
			if i%100000 == 0: 
				print i

			data = line.strip().split()
			chrom = data[0]
			pos = int(data[1])
			coverage = int(data[3])

			if pos not in bases_to_genes:
				continue

			# Check whether the position falls within an exon of any gene; if so, count it
			for gene in bases_to_genes[pos]:

				if gene not in gene_counts:
					gene_counts[gene] = 0
				gene_counts[gene] += coverage
		
				# Repeat this check for the last 100 bp
				if pos in three_map[gene]:
					if gene not in three_counts:
						three_counts[gene] = 0
					three_counts[gene] += coverage

pickle.dump(gene_counts, open("/srv/gsfs0/projects/montgomery/mgloud/projects/pivus/output/pickle/{0}_all_counts.pkl".format(indiv), "wb"))	
pickle.dump(three_counts, open("/srv/gsfs0/projects/montgomery/mgloud/projects/pivus/output/pickle/{0}_three_prime_counts.pkl".format(indiv), "wb"))	
