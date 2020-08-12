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

def shift_line(vcf_entry, chrom_mask):
    vcf_entry_out = copy.deepcopy(vcf_entry)
    init_start = int(vcf_entry[1])
    start = init_start
    for interval_start, interval_end in chrom_mask:
        if interval_start < init_start and interval_end <= init_start:
            if interval_start <=0:
                span = interval_end - interval_start
            else:
                span = interval_end - interval_start + 100
            start = start - span
    vcf_entry_out[1] = str(start)
    return(vcf_entry_out)

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
    contigre = re.compile(r"^##contig=")
    idre = re.compile(r"ID=([^,]*)")
    lenre = re.compile(r"length=([0-9]*)")
    nonlen_re = re.compile(r".*length=")
    done_re = re.compile(r"^#CHROM")
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
                newline = nonlen + str(newlen) + ">"
        
        outconn.write(newline + "\n")
    
##contig=<ID=PGA_scaffold_71__1_contigs__length_1999,length=1999>
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	16125X2	16125X20	16125X29	16125X39	16204X50	16204X54	16204X70	16204X72
#PGA_scaffold_1__81_contigs__length_22903049	632	.	G	C	117.01	.	AC=0;AF=0.002;AN=16;BaseQRankSum=0.934;ClippingRankSum=-1.794;DP=18522;ExcessHet=4.3892;FS=1.491;InbreedingCoeff=-0.0177;MLEAC=1;MLEAF=0.002;MQ=51.32;MQRankSum=0.178;QD=2.05;ReadPosRankSum=0.283;SOR=0.323;CMH=nan;NLOG10CMH=nan	GT:AD:DP:GQ:PL	0/0:54,0:54:99:0,114,1800	0/0:54,0:54:99:0,120,1800	0/0:48,0:48:99:0,114,1750	0/0:53,0:53:99:0,100,1800	0/0:65,0:65:99:0,112,1800	0/0:76,0:76:99:0,120,1800	0/0:50,0:50:99:0,120,1800	0/0:55,0:55:99:0,108,1800

def shift_body(inconn, mask, outconn):
    for l in inconn:
        l = l.rstrip('\n')
        sl = l.split('\t')
        if sl[0] in mask:
            sl = shift_line(sl, mask[sl[0]])
        outconn.write("\t".join(sl) + "\n")

def shift_vcf(inconn, mask, outconn):
    shift_header(inconn, mask, outconn)
    shift_body(inconn, mask, outconn)

def main():
    with open(sys.argv[1], "r") as inconn:
        mask = read_bed(inconn)
    if len(sys.argv) >= 4:
        with open(sys.argv[2], "r") as inconn:
            with open(sys.argv[3], "w") as outconn:
                shift_vcf(inconn, mask, outconn)
    else:
        shift_vcf(sys.stdin, mask, sys.stdout)

if __name__ == "__main__":
    main()

