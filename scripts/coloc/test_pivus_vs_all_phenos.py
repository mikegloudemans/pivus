#!/usr/bin/python
# Author: Mike Gloudemans
# 4/2/2018

import glob
import gzip
import subprocess

#GWAS_list = glob.glob("/users/mgloud/projects/gwas/data/prepared/*20*.gz")
GWAS_list = glob.glob("/users/mgloud/projects/gwas/data/prepared/*GCLC*.gz")
GWAS_list += glob.glob("/users/mgloud/projects/gwas/data/prepared/*AllSNPs*.gz")
GWAS_list += ["/users/mgloud/projects/gwas/data/prepared/CHD_CARDIoGRAMplusC4D_Mixed.prepared.txt.gz"]

for GWAS in GWAS_list:

    with gzip.open(GWAS) as f:
        data = f.readline().strip().split()
        if "chr" not in data or "snp_pos" not in data or "pvalue" not in data:
            with open("/users/mgloud/projects/brain_gwas/scripts/auxiliary/pivus/log.log", "a") as a:
                a.write("GWAS file {0} not analyzed due to incorrect format.\n")
            continue

    # Specify config file for colocalization tests -- only variables here
    # are which GWAS to use, and whether it reports effect size or odds ratio
    config_json = '''{{
            "gwas_experiments": {{"{0}": {{"ref": "1kgenomes", "gwas_format": "pval_only"}}}},
            "eqtl_experiments": {{"/users/mgloud/projects/brain_gwas/scripts/auxiliary/pivus/eqtls_70.txt.gz": {{"ref": "1kgenomes", "eqtl_format": "tstat", "selection_subset": "/users/mgloud/projects/brain_gwas/data/gene_lists/pivus/pivus_examples.txt"}},
                                    "/users/mgloud/projects/brain_gwas/scripts/auxiliary/pivus/eqtls_80.txt.gz": {{"ref": "1kgenomes", "eqtl_format": "tstat", "selection_subset": "/users/mgloud/projects/brain_gwas/data/gene_lists/pivus/pivus_examples.txt"}}}},
            
            "selection_basis":
                    "eqtl",
            "gwas_threshold": 1,
            "eqtl_threshold": 1,
            "methods": {{
                    "finemap":{{}}
            }},
            "plot_all": "True",
            "window": 2000000,
            "ref_genomes": {{
                   "1kgenomes": {{
                            "file": "/mnt/lab_data/montgomery/shared/1KG/ALL.chr{{0}}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz",
                            "af_attribute": "AF",
                            "N": 2504
                    }}

            }}
    }}'''.format(GWAS)

    # Write config to a file
    with open("/users/mgloud/projects/brain_gwas/scripts/auxiliary/pivus/pivus_paper_loci.config", "w") as w:
        w.write(config_json)

    # Now run that test. For now, don't worry about whether it works or not
    subprocess.call(["python" , "/users/mgloud/projects/brain_gwas/scripts/dispatch.py", "/users/mgloud/projects/brain_gwas/scripts/auxiliary/pivus/pivus_paper_loci.config"])

    # We'll look at results later. Continue along.
