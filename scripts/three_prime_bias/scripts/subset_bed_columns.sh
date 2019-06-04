awk '{if ($3 == "gene") print $0}' /srv/gsfs0/projects/montgomery/lfresard/WHI_rawdata/gencode.v19.annotation.gtf | cut -f1,4,5 > /srv/gsfs0/projects/montgomery/mgloud/projects/pivus/data/annot.bed
