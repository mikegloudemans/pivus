data = read.csv("/users/mgloud/projects/pivus/data/colocDEgenes_clpp5prc_with_gwas.csv", stringsAsFactors=FALSE)
data$eqtl_ref = NA
data$eqtl_alt = NA
data$eqtl_beta = NA

for (i in 1:dim(data)[1])
{
	#print(i)
	snp_chrom = strsplit(data$ref_snp[i], "_")[[1]][1]
	snp_pos = strsplit(data$ref_snp[i], "_")[[1]][2]
	gene = data$EnsemblID[i]

	eqtl_info = strsplit(system(paste0("tabix /users/mgloud/projects/brain_gwas/data/eqtls/gtex_v7/Whole_Blood.allpairs.txt.gz ", snp_chrom, ":", snp_pos, "-", snp_pos, " | grep ", gene), intern=TRUE), "\t")[[1]]

	gwas_header = strsplit(system(paste0("zcat /mnt/lab_data/montgomery/mgloud/gwas/data/munged/", gsub("_txt_gz", ".txt.gz ", data$base_gwas_file[i]), "| head -n 1 "), intern=TRUE), "\t")[[1]]
	gwas_info = strsplit(system(paste0("tabix /mnt/lab_data/montgomery/mgloud/gwas/data/munged/", gsub("_txt_gz", ".txt.gz ", data$base_gwas_file[i]), snp_chrom, ":", snp_pos, "-", snp_pos), intern=TRUE), "\t")

	#print(data$base_gwas_file[i])
	#print(gwas_header)
	#print(gwas_info)

	data$eqtl_ref[i] = eqtl_info[4]
	data$eqtl_alt[i] = eqtl_info[5]
	data$eqtl_beta[i] = eqtl_info[12]
}

same_dir = (paste(data$GWAS.non.effect.SNP, data$GWAS.effect..tested..SNP, sep="") == paste(data$eqtl_ref, data$eqtl_alt, sep=""))
flipped_dir = (paste(data$GWAS.non.effect.SNP, data$GWAS.effect..tested..SNP, sep="") == paste(data$eqtl_alt, data$eqtl_ref, sep=""))

# Find the ones that don't match between eQTL and GWAS...why?
same_dir | flipped_dir
# They're all for SCAMP2, the same SNP
# For some reason this SNP in the GWAS is annotated by - strand instead of + strand, don't ask me why

# Manually switch them to what they should be
data$GWAS.non.effect.SNP[c(23,24,28)] = "A"
data$GWAS.effect..tested..SNP[c(23,24,28)] = "C"
same_dir = (paste(data$GWAS.non.effect.SNP, data$GWAS.effect..tested..SNP, sep="") == paste(data$eqtl_ref, data$eqtl_alt, sep=""))
flipped_dir = (paste(data$GWAS.non.effect.SNP, data$GWAS.effect..tested..SNP, sep="") == paste(data$eqtl_alt, data$eqtl_ref, sep=""))

data$eqtl_effect_matches_gwas = (same_dir & ((data$Effect.direction == "+") == (data$eqtl_beta > 0))) | (flipped_dir & ((data$Effect.direction == "+") == (data$eqtl_beta < 0)))

data = data[,-which(colnames(data)=="Code")]

de_table = read.csv("/users/mgloud/projects/pivus/data/SupFile1_DE_SummaryStatisticsPIVUS.csv")

data_with_de = merge(data, de_table, by="EnsemblID")
data_with_de$aging_effect = ((data_with_de$Age.effect.size > 0) == data_with_de$eqtl_effect_matches_gwas)

write.csv(data_with_de, file="/users/mgloud/projects/pivus/output/PIVUS_coloc_plus_DE_sumstats.csv", quote=FALSE)

