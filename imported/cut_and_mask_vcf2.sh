#!/bin/bash
set -e

# identify bad items to remove, and generate a vcf with no bads:

gunzip -c 15515X100_190116_A00421_0031_AHGYLMDSXX_S28_L004_R1_001_bcftools_hiqual.vcf.gz > temp2.vcf

# shift vcf:

bedtools intersect \
    -header \
    -v \
    -a temp2.vcf \
    -b bigmask2.bed \
> masked.vcf

cat masked.vcf | python3 shift_vcf_maskmiddle.py kraken_mask_final2.bed | \
pigz -p 7 > 15515X100_190116_A00421_0031_AHGYLMDSXX_S28_L004_R1_001_bcftools_hiqual_masked_shifted.vcf.gz
