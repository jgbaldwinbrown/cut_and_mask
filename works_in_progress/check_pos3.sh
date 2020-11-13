gunzip -c louseref.all.sprot.interproscan_tsv.clean.sorted.baccut3.gff.gz | grep 'maker-PGA_scaffold_8__64_contigs__length_16703611-augustus-gene-166.21-mRNA-1'
gunzip -c pigeon_lice_ctgs_breaks_final_baccut3.review.fasta.gz | fa2tab | grep 'scaffold_8_' | tab2fa | cut -c 16622535-16623346 | awk 'BEGIN{print ">baccut2"} {print $0}' > baccut2_test_gene.fa
gunzip -c pigeon_lice_ctgs_breaks_final.review.fasta.gz | fa2tab | grep 'scaffold_8_' | tab2fa | cut -c 16632727-16633538 | awk 'BEGIN{print ">orig"} {print $0}' > orig_test_gene.fa
cat orig_test_gene.fa
cat baccut2_test_gene.fa
blastn -subject orig_test_gene.fa -query baccut2_test_gene.fa

# gunzip -c louseref.all.sprot.interproscan_tsv.clean.sorted.baccut3.gff.gz | grep 'scaffold_4_' | grep 'exon' | tail -n 50 | head -1
# gunzip -c louseref.all.sprot.interproscan_tsv.clean.sorted.gff.gz | grep 'scaffold_4_' | grep 'exon' | tail -n 50 | head -1
# gunzip -c pigeon_lice_ctgs_breaks_final_baccut3.review.fasta.gz | fa2tab | grep 'scaffold_4_' | tab2fa | cut -c 16354912-16354944 | awk 'BEGIN{print ">baccut2"} {print $0}' > baccut2_test_gene.fa
# gunzip -c pigeon_lice_ctgs_breaks_final.review.fasta.gz | fa2tab | grep 'scaffold_4_' | tab2fa | cut -c 17979153-17979185 | awk 'BEGIN{print ">orig"} {print $0}' > orig_test_gene.fa
# cat orig_test_gene.fa
# cat baccut2_test_gene.fa
# blastn -subject orig_test_gene.fa -query baccut2_test_gene.fa

#16354912	16354944	.	-	.	ID=maker-PGA_scaffold_4__56_contigs__length_18046996-augustus-gene-179.33-mRNA-1:12;Parent=maker-PGA_scaffold_4__56_contigs__length_18046996-augustus-gene-179.33-mRNA-1
#PGA_scaffold_4__56_contigs__length_18046996	maker	exon	17979153	17979185
# 16354912-16354944
# 17979153-17979185
