#!/bin/bash
set -e

# mkdir -p temp && {
#     gunzip -c pigeon_lice_ctgs_breaks_final_baccut.review.fasta.gz | fa2tab | head -n 4 | tail -n 1 | tab2fa > temp/chr4_new.fa
#     gunzip -c pigeon_lice_ctgs_breaks_final.review.fasta.gz | fa2tab | head -n 4 | tail -n 1 | tab2fa > temp/chr4_old.fa
#     cd temp/ && {
#         blastn -subject chr4_new.fa -query chr4_old.fa -outfmt 6 > bl
#         head -n 1 bl 
#         echo "14593361 - 12858588" | bc -l
#         cat ../mask.bed 
#     }
# }

gunzip -c louseref.all.sprot.interproscan_tsv.clean.sorted.gff.gz | \
grep '^\S*scaffold_4_' | \
datamash min 4 max 4 min 5 max 5

gunzip -c louseref.all.sprot.interproscan_tsv.clean.sorted.baccut.gff.gz | \
grep '^\S*scaffold_4_' | \
datamash min 4 max 4 min 5 max 5

# count removed transcripts

gunzip -c louseref_untwelve.all.maker.transcripts.fasta.gz | grep ">" | wc -l
gunzip -c louseref_untwelve.all.maker.baccut.transcripts.fasta.gz | grep ">" | wc -l
cat bads.gff | awk '$3=="mRNA"' | wc -l
