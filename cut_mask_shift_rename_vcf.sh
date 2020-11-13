#!/bin/bash
set -e

# arguments:
# $1: .bed file containing all regions to remove from the genome
# $2: number of cores to use

bedtools intersect \
    -header \
    -v \
    -a - \
    -b "${1}" | \
python3 shift_vcf_maskmiddle.py "${1}" | \
python3 rename_vcf_chroms.py | \
pigz -p "${2}"
