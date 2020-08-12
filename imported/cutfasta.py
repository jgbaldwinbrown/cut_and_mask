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

def revsorted_interval_union(interval_list):
    """ Union of a list of intervals e.g. [(1,2),(3,4)], reverse sorted by start, e.g., [(3,4), (1,2)] """
    intervals = [sympy.Interval(begin, end) for (begin, end) in interval_list]
    u = sympy.Union(*intervals)
    
    if isinstance(u, sympy.Interval):
        unsorted = [list(u.args[:2])]
    else:
        unsorted = list(u.args)
    
    sorted_intervals = sorted(unsorted, reverse = True, key = lambda x: x[0])
    return(sorted_intervals)

def mask_seq(seq, chrom_mask):
    ovl_mask = revsorted_interval_union(chrom_mask)
    for start, end in ovl_mask:
        if end <= 0 or start >= len(seq):
            pass
        elif start <= 0:
            seq = seq[end:]
        elif end >= len(seq):
            seq = seq[:start+1]
        else:
            seq = seq[:start+1] + seq[end:]
    return(seq)

def mask_and_print_if_good(header, seq, mask):
    if len(header) > 0 and len(seq) > 0:
        chrname = header[1:]
        if chrname in mask:
            seq = mask_seq(seq, mask[chrname])
        print(header)
        print(seq)

def cut_fasta(inconn, mask):
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
    cut_fasta(sys.stdin, mask)

if __name__ == "__main__":
    main()
