if [ ! -s pigeon_lice_ctgs_breaks_final.review.fasta ] ; then
    gunzip -c pigeon_lice_ctgs_breaks_final.review.fasta.gz > pigeon_lice_ctgs_breaks_final.review.fasta
fi

if [ ! -s pigeon_lice_ctgs_breaks_final_baccut3.review.fasta ] ; then
gunzip -c pigeon_lice_ctgs_breaks_final_baccut3.review.fasta.gz > pigeon_lice_ctgs_breaks_final_baccut3.review.fasta
fi

samtools faidx pigeon_lice_ctgs_breaks_final.review.fasta -r <(head -n 1 checkfile.txt ) > check_vcf1.fa
samtools faidx pigeon_lice_ctgs_breaks_final_baccut3.review.fasta -r <(tail -n 1 checkfile.txt ) > check_vcf2.fa

blastn -subject check_vcf1.fa -query check_vcf2.fa > checked_vcf.txt
