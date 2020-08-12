#!/bin/bash
set -e

if [ ! -s 15515X100_190116_A00421_0031_AHGYLMDSXX_S28_L004_R1_001_bcftools_hiqual_mini.vcf.gz ] ; then
    gunzip -c 15515X100_190116_A00421_0031_AHGYLMDSXX_S28_L004_R1_001_bcftools_hiqual.vcf.gz | \
    grep -E 'scaffold_[148]_|^#' | \
    awkf '($2>2000000 && $2 < 3000000) || /^#/ || ($2>12000000 && $2 < 13000000)' | \
    pigz -p 7 -c > 15515X100_190116_A00421_0031_AHGYLMDSXX_S28_L004_R1_001_bcftools_hiqual_mini.vcf.gz
fi

python3 shift_vcf_maskmiddle.py \
    kraken_mask_final2.bed \
    <(gunzip -c 15515X100_190116_A00421_0031_AHGYLMDSXX_S28_L004_R1_001_bcftools_hiqual_mini.vcf.gz) \
    15515X100_shifted_mini.vcf

pigz -p 7 15515X100_shifted_mini.vcf

diff \
    <(gunzip -c 15515X100_190116_A00421_0031_AHGYLMDSXX_S28_L004_R1_001_bcftools_hiqual_mini.vcf.gz) \
    <(gunzip -c 15515X100_shifted_mini.vcf.gz) | pigz -p 7 -c > diffs.txt.gz

