#!/bin/bash
set -e

# generate masked assembly:

gunzip -c pigeon_lice_ctgs_breaks_final.review.fasta.gz | \
python3 cutfasta_maskmiddle.py kraken_mask_final2.bed | \
python3 del_chroms_fasta.py kraken_del_final2.bed | \
pigz -p 7 -c > pigeon_lice_ctgs_breaks_final_baccut2.review.fasta.gz

# identify bad items to remove, and generate a gff with no bads:

cat kraken_mask_final2.bed kraken_del_final2.bed > bigmask2.bed
gunzip -c louseref.all.sprot.interproscan_tsv.clean.sorted.gff.gz > temp2.gff
bedtools intersect -a temp2.gff -b bigmask2.bed > bads2.gff

bedtools intersect -v -a temp2.gff -b bigmask2.bed | \
python3 shift_gff_maskmiddle.py kraken_mask_final2.bed | \
pigz -p 7 > louseref.all.sprot.interproscan_tsv.clean.sorted.baccut2.gff.gz
rm temp2.gff

# use bads identified above to remove unwanted proteins

gunzip -c louseref_untwelve.all.maker.proteins.fasta.gz | \
python3 remove_bads.py bads2.gff | \
gzip -c > louseref_untwelve.all.maker.baccut2.proteins.fasta.gz

# use bads identified above to remove unwanted transcripts

gunzip -c louseref_untwelve.all.maker.transcripts.fasta.gz | \
python3 remove_bads.py bads2.gff | \
gzip -c > louseref_untwelve.all.maker.baccut2.transcripts.fasta.gz

#kraken_del_final.bed
#kraken_mask_final.bed
#cutfasta_maskmiddle.py
#del_chroms_fasta.py
#shift_gff_maskmiddle.py

