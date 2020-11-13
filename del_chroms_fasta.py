#!/usr/bin/env python3

import sys
import sympy

def read_bed(inconn):
    """Read a bed file, return a dictionary with chromosome names for keys
and a list of coordinate pairs tuples for values."""
    out = {}
    for l in inconn:
        l = l.rstrip('\n')
        sl = l.split('\t')
        if sl[0] not in out:
            out[sl[0]] = []
        out[sl[0]].append((int(sl[1]), int(sl[2])))
    return(out)

def mask_and_print_if_good(header, seq, mask):
    if len(header) > 0 and len(seq) > 0:
        chrname = header[1:]
        if chrname not in mask:
            print(header)
            print(seq)

def del_chroms_fasta(inconn, mask):
    """Read a fasta file from inconn. If part of the fasta file is found in the
mask, cut those parts of the fasta out and print the remainder."""
    header = ""
    seq = ""
    for l in inconn:
        l = l.rstrip('\n')
        
        if len(l) < 1:
            continue
        
        if l[0] == ">":
            mask_and_print_if_good(header, seq, mask)
            header = l
            seq = ""
        else:
            seq = seq + l
    mask_and_print_if_good(header, seq, mask)

def main():
    with open(sys.argv[1], "r") as inconn:
        mask = read_bed(inconn)
    del_chroms_fasta(sys.stdin, mask)

if __name__ == "__main__":
    main()
