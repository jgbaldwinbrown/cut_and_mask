#!/usr/bin/env python3

import sys
import re

def get_ids(inconn):
    bads = set([])
    idre = re.compile(r"ID=([^;]*);")
    for l in inconn:
        l = l.rstrip('\n')
        sl = l.split('\t')
        nine = sl[8]
        id = idre.search(nine).group(1)
        bads.add(id)
    return(bads)

def print_if_good(header, seq, bads):
    if len(header) >= 2 or len(seq) >= 1:
        id = header.split()[0][1:]
        if id not in bads:
            print(header)
            print(seq)

def strip_bads(inconn, bads):
    header = ""
    seq = ""
    for l in inconn:
        l = l.rstrip('\n')
        if len(l) == 0:
            continue
        if l[0] == ">":
            print_if_good(header, seq, bads)
            header = l
            seq = ""
        else:
            seq = seq + l
    print_if_good(header, seq, bads)

def main():
    with open(sys.argv[1], "r") as inconn:
        bads = get_ids(inconn)
    strip_bads(sys.stdin, bads)

if __name__ == "__main__":
    main()
