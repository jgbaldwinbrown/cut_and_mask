#!/bin/bash
set -e

./cut_and_mask_vcf2.sh \
    test.vcf.gz \
    bigmask2.bed \
> test_masked.vcf.gz
