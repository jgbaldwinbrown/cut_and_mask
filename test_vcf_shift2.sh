#!/bin/bash
set -e

./cut_and_mask_vcf2.sh \
    test.vcf.gz \
    bigmask2.bed \
> test_masked.vcf.gz

wdiff <(gunzip -c test.vcf.gz) <(gunzip -c test_masked.vcf.gz )  | grep 'scaffold_4_.*375973' > test_pos.txt
wdiff <(gunzip -c test.vcf.gz) <(gunzip -c test_masked.vcf.gz )  | grep 'scaffold_8_.*12000026' >> test_pos.txt
