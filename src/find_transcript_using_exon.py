#!/usr/bin/env python3

import os, sys, re
from utils import *

if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit("usage: RUN annovar_variant_function exon_list")
    transcripts = load_transcripts()
    genes = load_gene_from_transcripts(transcripts)
    exon_list = list()
    with open(sys.argv[2]) as infile:
        for l in infile:
            if l.startswith('#'):
                continue
            left, right = re.split(r'\s+', l.strip())
            exon_left, exon_right = int(left), int(right)
            exon = (exon_left, exon_right)
            exon_list.append(exon)
    with open(sys.argv[1]) as infile:
        cnt = 0
        for l in infile:
            chrom, start, end, ref, alt = l.split('\t')[2:7]
            exon = exon_list[cnt]
            cnt += 1
            if l.startswith('#'):
                continue
            annovar_ans = parse_annovar_gene_anno(l)
            if annovar_ans['enst'] == None:
                ensg_list = annovar_ans['ensg']
                enst_list = list()
                for ensg_id in ensg_list:
                    enst_list += genes[ensg_id]
            candidate_enst_id, strand = None, None
            for enst_id in enst_list:
                t = transcripts[enst_id]
                # print(exon, t.details())

                if (exon[0] - 1, exon[1]) in t.exons:
                    candidate_enst_id = enst_id
                    strand = t.strand
                    break
            if candidate_enst_id == None:
                candidate_enst_id = "NAN"
            print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (chrom, start, end, ref, alt, candidate_enst_id, strand, exon[0], exon[1]))

