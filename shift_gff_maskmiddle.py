#!/usr/bin/env python3

import sys
import sympy
import copy

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

def shift_line(gff_entry, chrom_mask):
    gff_entry_out = copy.deepcopy(gff_entry)
    init_start = int(gff_entry[3])
    init_end = int(gff_entry[4])
    start = init_start
    end = init_end
    for interval_start, interval_end in chrom_mask:
        if interval_start < init_start and interval_end <= init_end:
            if interval_start <=0:
                span = interval_end - interval_start
            else:
                span = interval_end - interval_start + 100
            start = start - span
            end = end - span
    gff_entry_out[3] = str(start)
    gff_entry_out[4] = str(end)
    return(gff_entry_out)

def shift_gff(inconn, mask):
    for l in inconn:
        l = l.rstrip('\n')
        sl = l.split('\t')
        if sl[0] in mask:
            sl = shift_line(sl, mask[sl[0]])
        print("\t".join(sl))

def main():
    with open(sys.argv[1], "r") as inconn:
        mask = read_bed(inconn)
    shift_gff(sys.stdin, mask)

if __name__ == "__main__":
    main()

#
#
#import gffutils.biopython_integration as bpi
## Update a database with features from a GenBank file
#def gen():
#    "yields gffutils.Feature objects from a genbank file"
#    for rec in Bio.SeqIO.parse('ex.gb', 'genbank'):
#        for seqfeature in rec.features:
#            yield bpi.from_seqfeature(seqfeature)
#
#db.update(gen())
#
## Delete features from within a region
#db.delete(db.region('scaffold_13:271666-273390'))
#
#
## -----------------------------------------------------
## Shift the start/stop coords of features by the deletion size
##
#def gen2(features, n):
#    "yields features with coords shifted by n bp"
#    for feature in features:
#        feature.start += n
#        feature.stop += n
#        yield feature
#
## select features that come after the deletion region
#features_to_adjust = db.region('scaffold_13:273390-99999999')
#
## adjust 'em
#n = 271666 - 273390
#adjusted_features = gen2(features_to_adjust, n)
#
## update db, replacing existing features with new adjusted ones
#db.update(adjusted_features, merge_strategy='replace')
