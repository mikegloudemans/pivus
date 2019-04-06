# Author: Mike Gloudemans

#scp -r crick.stanford.edu:/srv/gsfs0/projects/montgomery/bballiu/PIVUS/RESULTS/eQTLAnalysis/MatrixEQTL/cis_eQTL_70_10SVA_setAge_MAFGeq5_MeanGeq5_ZeroLeq20_vsd.txt .
#scp -r crick.stanford.edu:/srv/gsfs0/projects/montgomery/bballiu/PIVUS/RESULTS/eQTLAnalysis/MatrixEQTL/cis_eQTL_80_10SVA_setAge_MAFGeq5_MeanGeq5_ZeroLeq20_vsd.txt .

echo -e "chr\tsnp_pos\tref\talt\tgene\tbeta\ttstat\tpvalue\tFDR" > eqtls_70.txt
echo -e "chr\tsnp_pos\tref\talt\tgene\tbeta\ttstat\tpvalue\tFDR" > eqtls_80.txt

sed s/_/\\t/g cis_eQTL_70_10SVA_setAge_MAFGeq5_MeanGeq5_ZeroLeq20_vsd.txt | tail -n +2 | sort -k1,1n -k2,2n >> eqtls_70.txt 
sed s/_/\\t/g cis_eQTL_80_10SVA_setAge_MAFGeq5_MeanGeq5_ZeroLeq20_vsd.txt | tail -n +2 | sort -k1,1n -k2,2n >> eqtls_80.txt 

bgzip -f eqtls_70.txt
bgzip -f eqtls_80.txt

tabix -f -s 1 -b 2 -e 2 -S 1 eqtls_70.txt.gz
tabix -f -s 1 -b 2 -e 2 -S 1 eqtls_80.txt.gz

