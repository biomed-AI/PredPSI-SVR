#!/usr/bin/env python3

import sys, os
from utils import mark_seq

if "TOOL_PATH" in os.environ:
    TOOL_PATH = os.environ['TOOL_PATH']
else:
    TOOL_PATH = "./"

sys.path.append(os.path.join(TOOL_PATH, "src"))
from utils import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit("RUN mut_info")
    with open(sys.argv[1]) as infile:
        for l in infile:
            chrom, start, end, ref, alt, enst_id, strand, exon_start, exon_end = l.strip().split('\t')[0:9]
            ID = '_'.join([chrom, start, ref, alt])
            head = '>%s|%s|%s|%s-%s' % (ID, enst_id, strand, exon_start, exon_end)
            print(head)
            seq = mark_seq(chrom, strand, start, ref, alt, exon_start, exon_end)
            print(seq)
