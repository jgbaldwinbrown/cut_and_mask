#!/bin/bash
set -e

./cut_mask_shift_rename_vcf.sh \
    test.vcf.gz \
    bigmask2.bed \
    8 \
> test_full.vcf.gz

wdiff <(gunzip -c test.vcf.gz) <(gunzip -c test_full.vcf.gz )  | grep 'scaffold_4_.*375973' > test_pos.txt
wdiff <(gunzip -c test.vcf.gz) <(gunzip -c test_full.vcf.gz )  | grep 'scaffold_8_.*12000026' >> test_pos.txt
