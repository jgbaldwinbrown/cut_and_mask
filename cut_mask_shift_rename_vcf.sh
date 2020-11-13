#!/bin/bash
set -e

# arguments:
# $1: gzipped VCF input file
# $2: .bed file containing all regions to remove from the genome
# $3: number of cores to use

# Generate temporary file to store uncompressed vcf:

TEMP="$(mktemp temp_vcf_XXXXXXXXXX.vcf)"

# identify bad items to remove, and generate a vcf with no bads:

gunzip -c "${1}" > "${TEMP}"

# shift vcf:

bedtools intersect \
    -header \
    -v \
    -a "${TEMP}" \
    -b "${2}" | \
python3 shift_vcf_maskmiddle.py "${2}" | \
python3 rename_vcf_chroms.py | \
pigz -p "${3}"

rm -f "${TEMP}"
