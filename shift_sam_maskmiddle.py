#!/usr/bin/env python3

import sys
import sympy
import copy
import re

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

def interval_union(interval_list):
    """ Union of a list of intervals e.g. [(1,2),(3,4)], reverse sorted by start, e.g., [(3,4), (1,2)] """
    intervals = [sympy.Interval(begin, end) for (begin, end) in interval_list]
    u = sympy.Union(*intervals)
    
    if isinstance(u, sympy.Interval):
        unsorted = [list(u.args[:2])]
    else:
        unsorted = list(u.args)
    
    return(unsorted)

def shift_line(sam_entry, chrom_mask, poscol):
    # HWI-D00294:150:C67DPANXX:5:2208:5272:71468      163     PGA_scaffold_1__81_contigs__length_22903049     2000615 60      85M     =       2000732 202     TAAGGAAAAAAGAAGAGAAAACTGGCGCTGACGGAACTTCATCTCCACCTACTTTGGAATCAAACCAAACTTTTTTTCCCACGTG   BBCCCCGGGGGGGGGGGGGGGGGGGGGGGGGGGGFGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGGGGG0FGGG   NM:i:0  MD:Z:85 AS:i:85 XS:i:0
    # HWI-D00294:150:C67DPANXX:5:1116:9547:24835      99      PGA_scaffold_1__81_contigs__length_22903049     2000616 60      85M     =       2000732 201     AAGGAAAAAAGAAGAGAAAACTGGCGCTGACGGAACTTCATCTCCACCTACTTTGGAATCAAACCAAACTTTTTTTCCCACGTGC   BCCCBGGGGDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFGGGGGGGGGGGGGGGGEGGGGGGGGGGGGGGGGG   NM:i:0  MD:Z:85 AS:i:85 XS:i:20
    # HWI-D00294:150:C67DPANXX:5:1116:9547:24835      99      PGA_scaffold_1__81_contigs__length_22903049     2000616 60      85M     =       2000732 201     AAGGAAAAAAGAAGAGAAAACTGGCGCTGACGGAACTTCATCTCCACCTACTTTGGAATCAAACCAAACTTTTTTTCCCACGTGC   BCCCBGGGGDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFGGGGGGGGGGGGGGGGEGGGGGGGGGGGGGGGGG   NM:i:0  MD:Z:85 AS:i:85 XS:i:20
    sam_entry_out = copy.deepcopy(sam_entry)
    init_start = int(sam_entry[poscol])
    start = init_start
    for interval_start, interval_end in chrom_mask:
        if interval_start < init_start and interval_end <= init_start:
            if interval_start <=0:
                span = interval_end - interval_start
            else:
                span = interval_end - interval_start - 100
            start = start - span
    sam_entry_out[poscol] = str(start)
    return(sam_entry_out)

def get_new_len(chr_mask, mylen):
    curlen = mylen
    for start, end in chr_mask:
        span = min(end, mylen) - max(start, 0)
        if start <= 0 or end <= 0 or start >= mylen or end >= mylen:
            curlen = curlen - span
        else:
            curlen = curlen - span + 100
    return(curlen)

def shift_header(inconn, mask, outconn):
#@SQ     SN:PGA_scaffold_345__1_contigs__length_15474    LN:15474
#@SQ     SN:PGA_scaffold_346__1_contigs__length_25197    LN:25197
#@SQ     SN:PGA_scaffold_347__1_contigs__length_6501     LN:6501
#@SQ     SN:PGA_scaffold_348__1_contigs__length_5826     LN:5826
#@SQ     SN:PGA_scaffold_349__1_contigs__length_28069    LN:28069
    contigre = re.compile(r"^@SQ")
    idre = re.compile(r"SN:(\S*)")
    lenre = re.compile(r"LN:([0-9]*)")
    nonlen_re = re.compile(r".*LN:")
    done_re = re.compile(r"^@PG")
    for l in inconn:
        l = l.rstrip('\n')
        newline = l
        if done_re.search(l):
            outconn.write(newline + "\n")
            break
        if contigre.search(l):
            myid = idre.search(l).group(1)
            if myid in mask:
                mylen = int(lenre.search(l).group(1))
                newlen = get_new_len(mask[myid], mylen)
                nonlen = nonlen_re.search(l).group(0)
                newline = nonlen + str(newlen)
        
        outconn.write(newline + "\n")
    
##contig=<ID=PGA_scaffold_71__1_contigs__length_1999,length=1999>
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	16125X2	16125X20	16125X29	16125X39	16204X50	16204X54	16204X70	16204X72
#PGA_scaffold_1__81_contigs__length_22903049	632	.	G	C	117.01	.	AC=0;AF=0.002;AN=16;BaseQRankSum=0.934;ClippingRankSum=-1.794;DP=18522;ExcessHet=4.3892;FS=1.491;InbreedingCoeff=-0.0177;MLEAC=1;MLEAF=0.002;MQ=51.32;MQRankSum=0.178;QD=2.05;ReadPosRankSum=0.283;SOR=0.323;CMH=nan;NLOG10CMH=nan	GT:AD:DP:GQ:PL	0/0:54,0:54:99:0,114,1800	0/0:54,0:54:99:0,120,1800	0/0:48,0:48:99:0,114,1750	0/0:53,0:53:99:0,100,1800	0/0:65,0:65:99:0,112,1800	0/0:76,0:76:99:0,120,1800	0/0:50,0:50:99:0,120,1800	0/0:55,0:55:99:0,108,1800

def shift_body(inconn, mask, outconn):
    for l in inconn:
        l = l.rstrip('\n')
        sl = l.split('\t')
        if sl[2] in mask:
            sl = shift_line(sl, mask[sl[2]], 3)
            if sl[6] == "=":
                sl = shift_line(sl, mask[sl[2]], 7)
        if sl[6] in mask:
            sl = shift_line(sl, mask[sl[6]], 7)
        outconn.write("\t".join(sl) + "\n")

def shift_sam(inconn, mask, outconn):
    shift_header(inconn, mask, outconn)
    shift_body(inconn, mask, outconn)

def main():
    with open(sys.argv[1], "r") as inconn:
        mask = read_bed(inconn)
    if len(sys.argv) >= 4:
        with open(sys.argv[2], "r") as inconn:
            with open(sys.argv[3], "w") as outconn:
                shift_sam(inconn, mask, outconn)
    else:
        shift_sam(sys.stdin, mask, sys.stdout)

if __name__ == "__main__":
    main()

