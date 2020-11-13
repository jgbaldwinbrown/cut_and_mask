#!/bin/bash
set -e

# remove bad entries:

bedtools intersect \
    -v \
    -abam ill_aligned_mini2.bam \
    -b bigmask2.bed | \
tee masked.bam | \
samtools view -h | python3 shift_sam_maskmiddle.py kraken_mask_final2.bed | \
samtools view -bS > ill_aligned_mini2_masked_shifted.bam

diff \
    <(samtools view -h ill_aligned_mini2.bam) \
    <(samtools view -h masked.bam) \
> sam_mask_diffs.txt

samtools index ill_aligned_mini2.bam
samtools index ill_aligned_mini2_masked_shifted.bam
