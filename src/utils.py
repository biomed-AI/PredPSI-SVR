#!/usr/bin/env python3

import sys, re, os
from subprocess import PIPE, Popen

samtools = os.environ['samtools']
ref_seqs = {
    # ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg19/ucsc.hg19.fasta.gz
    'hg19': os.environ['hg19_genome']
}

def DNA_trans(raw_seq):
    trans_table = str.maketrans("AGCTUagctu", "TCGAAtcgaa")
    seq = raw_seq[::-1].translate(trans_table)
    return seq

def genome_seq(chrom, start, length=1, version='hg19',
        rev=False, to_upper=True, formatted=False):
    # 1-based
    if not str(chrom).startswith('chr'):
        chrom = 'chr' + str(chrom)
    assert length > 0, "sequence lengh must above 0"
    assert version in {'hg19', 'hg38'}, "In 'utils.py':\
        get_genome(version, ...), 'version' must be 'hg19' or 'hg38'"
    cmd = [samtools, 'faidx', ref_seqs[version],
         "%s:%s-%s" % (chrom, start, start + length - 1)]
    info = Popen(cmd, stdout=PIPE, stderr=PIPE)
    msg = info.communicate()
    outmsg, errmsg = msg[0].decode('utf8'), msg[1].decode('utf8')
    assert errmsg is '', "Error in file 'utils.py':'get_genome': " + errmsg
    seq = ''.join(outmsg.strip().split('\n')[1:])
    if to_upper:
        seq = seq.upper()
    if rev:
        seq = DNA_trans(seq)
    if formatted:
        subseq = ['>' + chrom + ':' + str(start) + '-' + str(start+length-1)]
        bp_per_line = 60
        N = len(seq) // bp_per_line
        # print(len(seq), N)
        for i in range(N + 1):
            # print(i)
            subseq.append(seq[i * bp_per_line:(i + 1) * bp_per_line])
            # print(i, seq[i * bp_per_line: (i + 1) * bp_per_line])
        seq = '\n'.join(subseq)
    return seq

class Transcript:
    def __init__(self, *args, **kvargs):
        # assert len(args) * len(kvargs) is 0 and len(args) + len(kvargs) > 0 # either give a record line or give dictionay
        if len(args) is 0:
            pass
        else:
            # pass through string(include 'bin' field)
            if "assembly" in kvargs:
                self.assembly = kvargs["assembly"]
            else:
                self.assembly = "hg19"
            # print("===========", args[0], file=sys.stderr)
            self.transcript_id, self.chrom, self.strand, tx_start,\
                tx_end, cds_start, cds_end, exon_count,\
                exon_starts, exon_ends, self.score, self.gene_id,\
                self.cds_start_stat,self.cds_end_stat,\
                exon_frames = args[0].strip().split('\t')[1:]
            self.tx_start, self.tx_end = int(tx_start), int(tx_end)
            self.cds_start, self.cds_end = int(cds_start), int(cds_end)
            self.exon_count = int(exon_count)
            exon_starts = [int(x) \
                for x in exon_starts.rstrip(',').split(',')]
            exon_ends = [int(x) \
                for x in exon_ends.rstrip(',').split(',')]
            self.exons = tuple(zip(exon_starts, exon_ends))
            self.exon_frames = [int(x) \
                for x in exon_frames.rstrip(',').split(',')]

    def in_transcript(self, position, base_1=True):
        if base_1:
            pos = int(position) - 1
        else:
            pos = int(position)
        if pos < self.tx_start or pos >= self.tx_end:
            return False
        else:
            return True

    def i_th_exon(self, i):
        # i is 1-based
        i -= 1
        assert i >= 0 and i < self.exon_count, "\"%s\" only has %s exons" % (self.transcript_id, self.exon_count)
        if self.strand == '-':
            i = self.exon_count - 1 - i
        return self.exons[i]

    def i_th_intron(self, i):
        i = abs(i) - 1
        assert i >= 0 and i < self.exon_count - 1, "\"%s\" only has %s introns" % (self.transcript_id, self.exon_count - 1)
        if self.strand == '-':
            i = self.exon_count - 2 - i
        return (self.exons[i][1], self.exons[i+1][0])
    
    def locate_position(self, position, base_1=True):
        pos = int(position)
        if base_1:
            pos -= 1
        assert pos >= self.tx_start and pos <= self.tx_end, "%s out of transcript range [%s,%s)(0-based)" % (position, self.tx_start, self.tx_end)
        if pos >= self.exons[0][0] and pos < self.exons[0][1]:
            i_th = 1
        else:
            for i in range(1, self.exon_count):
                if pos >= self.exons[i-1][1] and pos < self.exons[i][0]:
                    # print("check: ", i, pos, self.exons[i-1], self.exons[i])
                    i_th = -(i)
                    break
                if pos >= self.exons[i][0] and pos < self.exons[i][1]:
                    i_th = i + 1
                    break
        # print("i_th = ", i_th, position)
        if self.strand is '-':
            if i_th > 0:
                i_th = self.exon_count + 1 - i_th
            else:
                i_th = - (self.exon_count + i_th)
        return i_th
    
    
    
    def details(self):
        info  = "%s - %s\n" % (self.transcript_id, self.gene_id)
        info += "Chrom: %s; Strand: %s\n" % (self.chrom, self.strand)
        info += "Transcript region: [%s, %s)\n" % (self.tx_start, self.tx_end)
        info += "CDS region: [%s, %s)\n" % (self.cds_start, self.cds_end)
        info += "Exon count: %s\n" % (self.exon_count)
        for i, exon_frame in enumerate(self.exon_frames):
            info += "[%s, %s)\t" % self.exons[i]
            info += "%s\n" % (exon_frame)
        return info

def load_transcripts(version="ensembl", assembly="hg19"):
    # use annovar ensembl/ncbi gene file
    # files = {"hg19_ensGene": HOME + "/Data/annovar/humandb/hg19_ensGene.txt"}
    # file_id = "hg19_ensGene"

    src_file = os.environ['hg19_ensGene']
    transcripts_dict = dict()
    with open(src_file) as infile:
        for l in infile:
            t = Transcript(l, assembly="hg19")
            transcripts_dict[t.transcript_id] = t
    return transcripts_dict

def load_gene_from_transcripts(transcripts_dict):
    gene_dict = dict()
    for tx_id in transcripts_dict:
        t = transcripts_dict[tx_id]
        gene_id = t.gene_id
        if gene_id not in gene_dict:
            gene_dict[gene_id] = list()
        gene_dict[gene_id].append(tx_id)
    return gene_dict


def find_exon(tx_id, position, transcripts, base_1=True):
    # position is 1-based
    pos = int(position) - 1
    t = transcripts[tx_id]
    ans = dict()
    ans['valid'] = True
    ans['strand'] = t.strand
    if not t.in_transcript(pos, base_1=False):
        ans['valid'] = False
    else:
        loc = t.locate_position(pos, base_1=False)
        # print(pos, loc)
        if loc > 0:
            ans['exon'] = t.i_th_exon(loc)
            ans['type'] = 'exon'
            ans['dist'] = min(pos - ans['exon'][0], ans['exon'][1] - pos)
        else:
            ans['type'] = 'intron'
            if ans['strand'] == '+':
                if pos - t.i_th_exon(abs(loc))[1] < t.i_th_exon(abs(loc) + 1)[0] - pos:
                    ans['exon'] = t.i_th_exon(abs(loc))
                    ans['dist'] = pos - t.i_th_exon(abs(loc))[1]
                else:
                    ans['exon'] = t.i_th_exon(abs(loc) + 1)
                    ans['dist'] = t.i_th_exon(abs(loc) + 1)[0] - pos
            else:
                if pos - t.i_th_exon(abs(loc) + 1)[1] < t.i_th_exon(abs(loc))[0] - pos:
                    ans['exon'] = t.i_th_exon(abs(loc) + 1)
                    ans['dist'] = pos - t.i_th_exon(abs(loc) + 1)[1]
                else:
                    ans['exon'] = t.i_th_exon(abs(loc))
                    ans['dist'] = t.i_th_exon(abs(loc))[0] - pos
    if ans['valid'] and ans['dist'] > 200:
        ans['valid'] = False
    if ans['valid'] and ans['exon'][1] - ans['exon'][0] < 4:
        ans['valid'] = False
    return ans # dict: valid type(exon/intron) exon dist

def parse_annovar_gene_anno(line):
    # return gene or transcripts list
    # ensembl hg19 annotation
    region, gene_info, chrom, start, end, ref, alt = line.split('\t')[0:7]
    ans = dict()
    ans['chrom'] = chrom
    ans['start'] = start
    ans['end'] = end
    ans['ref'] = ref
    ans['alt'] = alt
    re_enst = re.compile(r'ENST\d{11}')
    re_ensg = re.compile(r'ENSG\d{11}')
    ENST_list = re_enst.findall(line)
    # print(line, end='')
    # print(ENST_list)
    if len(ENST_list) > 0:
        ans['enst'] = ENST_list
        ans['ensg'] = None
    else:
        ans['enst'] = None
        ans['ensg'] = re_ensg.findall(line)
        # print(line, ans['ensg'])
    return ans

def find_transcripts(annovar_gene_anno):
    # print(annovar_gene_anno)
    transcripts = load_transcripts()
    genes = load_gene_from_transcripts(transcripts)
    with open(annovar_gene_anno) as infile:
        for line in infile:
            # print(line)
            anno = parse_annovar_gene_anno(line)
            # print(anno)
            chrom, start, end, ref, alt = anno['chrom'], anno['start'], anno['end'], anno['ref'], anno['alt']
            enst_list = anno['enst']
            if enst_list == None:
                ensg_list = anno['ensg']
                assert len(ensg_list), line
                enst_list = genes[ensg_list[0]]
            min_dist = 99999999
            candidate_ensg_id = None
            for enst in enst_list:
                exon_info = find_exon(enst, start, transcripts)
                if not exon_info['valid']:
                    # print('invalid', exon_info)
                    continue
                # print('\t'.join(["result:", enst, chrom, start, end, ref, alt]))
                if exon_info['dist'] < min_dist:
                    min_dist = exon_info['dist']
                    candidate_ensg_id = enst
            if candidate_ensg_id == None:
                candidate_ensg_id = "NAN"
                exon_start, exon_end = '.', '.'
                dist = "."
                strand = "."
            else:
                exon_info = find_exon(candidate_ensg_id, start, transcripts)
                strand = exon_info['strand']
                exon_start, exon_end = exon_info['exon'] # WARNING: exon_info['exon'] is 0-based: [exon_start, exon_end)
                dist = exon_info['dist']

                exon_start += 1
            print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (chrom, start, end, ref, alt, candidate_ensg_id, strand, exon_start, exon_end, dist))

def mark_seq(chrom, strand, position, ref, alt, exon_start, exon_end, flanking_size=300, buildver="hg19"):
    # all use 1 based coordinates
    # exon interval is closed interval: [exon_start, exon_end]
    # mark variant seqeunce with exon-intron junctions in format "intron|exon|intron e.g. AGCT|AGCT[A/GCT]|AGCT"
    position = int(position)
    exon_start, exon_end = int(exon_start), int(exon_end)
    base = exon_start - flanking_size
    length = flanking_size * 2 + exon_end - exon_start
    # stop = position + flanking_size
    raw_seq = genome_seq(chrom, base, length, version=buildver)
    # base_0 = 0
    mut_start_0 = position - base
    mut_end_0 = mut_start_0 + len(ref) # [xxx, xxx)
    if ref == '-':
        mut_end_0 -= 1
    exon_start_0 = exon_start - base
    exon_end_0 = exon_end - base + 1 # attention: in this step exon interval transfered to [xxx, xxx) instead of closed interval
    seq_ss = raw_seq[0:exon_start_0] + '|' + raw_seq[exon_start_0:exon_end_0] + '|' + raw_seq[exon_end_0:]
    shift = 0
    if mut_end_0 <= exon_start_0:
        shift = 0
    elif mut_start_0 >= exon_start_0 and mut_end_0 <= exon_end_0:
        shift = 1
    elif mut_start_0 >= exon_end_0:
        shift = 2
    else:
        print(chrom, position, position + len(ref), exon_start, exon_end)
        exit("Mutation crosses splice site")
    if strand is '+':
        seq_ss_mut = seq_ss[0:mut_start_0+shift] + '[' + ref + '/' + alt + ']' + seq_ss[mut_end_0+shift:]
    else:
        seq_ss_mut = DNA_trans(seq_ss[mut_end_0+shift:]) + '[' + DNA_trans(ref) + '/' + DNA_trans(alt) + ']' + DNA_trans(seq_ss[0:mut_start_0+shift])
    if ref == '-':
        ref = ""
    # assert ref == raw_seq[mut_start_0:mut_end_0], "raw_ref=%s : get_ref=%s" % (ref, raw_seq[mut_start_0:mut_end_0])
    assert ref == raw_seq[mut_start_0:mut_end_0], ValueError
    # # test:
    # test_seq = seq_ss_mut.replace('|', '')
    # left, right = test_seq.split('/')
    # pre, ref = left.split('[')
    # alt, post = right.split(']')
    # reverse_seq = pre + ref + post
    # reverse_seq = reverse_seq.replace('-', '')
    # if strand is '-':
    #     reverse_seq = DNA_trans(reverse_seq)
    # assert reverse_seq == raw_seq, "\n%s\n%s" % (raw_seq, reverse_seq)
    return seq_ss_mut
 

if __name__ == '__main__':
    pass
