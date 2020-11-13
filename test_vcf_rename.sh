#!/bin/bash
set -e

gunzip -c test.vcf.gz | \
python3 rename_vcf_chroms.py | \
gzip -c \
> test_renamed.vcf.gz

wdiff <(gunzip -c test.vcf.gz) <(gunzip -c test_renamed.vcf.gz ) | gzip -c > rename_diff.txt.gz
