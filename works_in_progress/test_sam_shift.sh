#!/bin/bash
set -e

python3 shift_sam_maskmiddle.py \
    kraken_mask_final2.bed \
    ill_aligned_mini.sam \
    ill_aligned_mini_shifted.sam

diff \
    ill_aligned_mini.sam \
    ill_aligned_mini_shifted.sam | \
pigz -p 7 -c \
> samdiffs.txt.gz

