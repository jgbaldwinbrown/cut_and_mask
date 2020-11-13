#!/bin/bash
set -e

# arguments:
# $1: .bed file containing all regions to remove from the genome

bedtools intersect \
    -header \
    -v \
    -a - \
    -b "${1}" | \
shift_vcf_maskmiddle "${1}" | \
rename_vcf_chroms
