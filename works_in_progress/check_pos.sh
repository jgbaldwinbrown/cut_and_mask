#gunzip -c louseref.all.sprot.interproscan_tsv.clean.sorted.baccut2.gff.gz | grep 'maker-PGA_scaffold_8__64_contigs__length_16703611-augustus-gene-166.21-mRNA-1'
gunzip -c pigeon_lice_ctgs_breaks_final_baccut2.review.fasta.gz | fa2tab | grep 'scaffold_8_' | tab2fa | cut -c 16622335-16623146 | awk 'BEGIN{print ">baccut2"} {print $0}' > baccut2_test_gene.fa
gunzip -c pigeon_lice_ctgs_breaks_final.review.fasta.gz | fa2tab | grep 'scaffold_8_' | tab2fa | cut -c 16632727-16633538 | awk 'BEGIN{print ">orig"} {print $0}' > orig_test_gene.fa
blastn -subject orig_test_gene.fa -query baccut2_test_gene.fa
