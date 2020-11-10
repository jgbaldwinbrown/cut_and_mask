#!/usr/bin/env python3

import sys
import sympy
import copy
import re

def shift_header(inconn, outconn):
    contigre = re.compile(r"^##contig=")
    idre = re.compile(r"ID=([^,]*)")
    chrnumre = re.compile(r"scaffold_([0-9]*)_")
    preidre = re.compile(r".*ID=")
    postidre = re.compile(r",length=.*")
    # lenre = re.compile(r"length=([0-9]*)")
    # nonlen_re = re.compile(r".*length=")
    done_re = re.compile(r"^#CHROM")
    for l in inconn:
        l = l.rstrip('\n')
        newline = l
        if done_re.search(l):
            outconn.write(newline + "\n")
            break
        if contigre.search(l):
            myid = idre.search(l).group(1)
            chrnum = chrnumre.search(myid).group(1)
            preid = preidre.search(l).group(0)
            postid = postidre.search(l).group(0)
            newid = "chr" + str(chrnum)
            newline = preid + str(newid) + postid
        
        outconn.write(newline + "\n")
    
##contig=<ID=PGA_scaffold_71__1_contigs__length_1999,length=1999>
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	16125X2	16125X20	16125X29	16125X39	16204X50	16204X54	16204X70	16204X72
#PGA_scaffold_1__81_contigs__length_22903049	632	.	G	C	117.01	.	AC=0;AF=0.002;AN=16;BaseQRankSum=0.934;ClippingRankSum=-1.794;DP=18522;ExcessHet=4.3892;FS=1.491;InbreedingCoeff=-0.0177;MLEAC=1;MLEAF=0.002;MQ=51.32;MQRankSum=0.178;QD=2.05;ReadPosRankSum=0.283;SOR=0.323;CMH=nan;NLOG10CMH=nan	GT:AD:DP:GQ:PL	0/0:54,0:54:99:0,114,1800	0/0:54,0:54:99:0,120,1800	0/0:48,0:48:99:0,114,1750	0/0:53,0:53:99:0,100,1800	0/0:65,0:65:99:0,112,1800	0/0:76,0:76:99:0,120,1800	0/0:50,0:50:99:0,120,1800	0/0:55,0:55:99:0,108,1800

def shift_body(inconn, outconn):
    chrnumre = re.compile(r"scaffold_([0-9]*)_")
    for l in inconn:
        l = l.rstrip('\n')
        sl = l.split('\t')
        oldchr = sl[0]
        chrnum = chrnumre.search(oldchr).group(1)
        newchr = "chr" + str(chrnum)
        sl[0] = newchr
        outconn.write("\t".join(sl) + "\n")

def shift_vcf(inconn, outconn):
    shift_header(inconn, outconn)
    shift_body(inconn, outconn)

def main():
    if len(sys.argv) >= 3:
        with open(sys.argv[1], "r") as inconn:
            with open(sys.argv[2], "w") as outconn:
                shift_vcf(inconn, outconn)
    else:
        shift_vcf(sys.stdin, sys.stdout)

if __name__ == "__main__":
    main()

