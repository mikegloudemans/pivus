import glob
import pickle

# Get the length of each transcript
transcript_lengths = {}	
transcript_genes = {}
with open("/srv/gsfs0/projects/montgomery/lfresard/WHI_rawdata/gencode.v19.annotation.gtf") as f:
	for line in f:
		if line.startswith("#"):
			continue
		data = line.strip().split()
		if not data[2] == "exon":
			continue
		gene = data[11].replace('"', '').replace(";", "")
		actual_gene = data[9].replace('"', '').replace(";", "")
		transcript_genes[gene] = actual_gene

		start = int(data[3])
		end = int(data[4])

		if gene not in transcript_lengths:
			transcript_lengths[gene] = 0
		transcript_lengths[gene] += (abs(end - start) + 1)


# For each individual...
biases = {}
for indiv in glob.glob("/srv/gsfs0/projects/montgomery/mgloud/projects/pivus/output/pickle/*all_counts.pkl"):

	print indiv

	# Make a dictionary containing bias measurements
	all_counts = pickle.load(open(indiv))
	three_counts = pickle.load(open(indiv.replace("all_counts", "three_prime_counts")))

	biases[indiv] = {}
	for ac in all_counts:
		# I didn't think this was possible with our settings, but it actually does happen sometimes
		if all_counts[ac] == 0:
			continue
		all_ratio = all_counts[ac] * 1.0 / transcript_lengths[ac]
		if ac in three_counts:
			three_ratio = three_counts[ac] * 1.0 / min(transcript_lengths[ac], 100)
		else:
			three_ratio = 0

		biases[indiv][ac] = three_ratio / all_ratio
all_inds = glob.glob("/srv/gsfs0/projects/montgomery/mgloud/projects/pivus/output/pickle/*all_counts.pkl")
short = [ai.replace("/srv/gsfs0/projects/montgomery/mgloud/projects/pivus/output/pickle/", "").replace(".Aligned.out_mapq255_sorted.bam.pileup.gz_all_counts.pkl", "") for ai in all_inds]

# Get all transcripts
genes = set([])

for indiv in biases:
	for gene in biases[indiv]:
		genes.add(gene)

genes = list(genes)

with open("/srv/gsfs0/projects/montgomery/mgloud/projects/pivus/output/bias_matrix.tsv", "w") as w:

	w.write("transcript\tgene\t" + "\t".join(short) + "\n")

	# Output to a rectangular matrix of biases per individual
	for g in genes:
		w.write(g + "\t")
		w.write(transcript_genes[g])
		for ai in all_inds:
			if g in biases[ai]:
				w.write("\t" + str(biases[ai][g]))
			else: 
				w.write("\tNA")
		w.write("\n")
