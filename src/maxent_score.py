#!/usr/bin/env python

import sys, os
from subprocess import Popen, PIPE

TOOL_PATH = os.environ['TOOL_PATH']

MAXENT_PATH = os.path.join(TOOL_PATH, 'tools/maxent')

score5 = MAXENT_PATH + '/score5.pl'
score3 = MAXENT_PATH + '/score3.pl'

def ref_alt_seq(seq):
    left, right = seq.strip().replace('-','').split('/')
    pre, ref = left.split('[')
    alt, post = right.split(']')
    return (pre + ref + post, pre + alt + post)

def score_ss(seq, score3, score5):
    assert len(seq) is 23 or len(seq) is 9
    if len(seq) is 23:
        score = score3
    else:
        score = score5
    p = Popen([score, '-'], stdin=PIPE, stdout=PIPE, close_fds=True, cwd=MAXENT_PATH)
    stdout = p.communicate(seq.encode())[0]
    return float(stdout.decode('utf8').strip().split('\t')[-1])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit('usage: RUN marked_seqs')

    print("#ss3_ref\tss5_ref\tss3_alt\tss5_alt\tdelta_ss3\tdelta_ss5")
    with open(sys.argv[1]) as infile:
        for l in infile:
            if l.startswith('>') or l.startswith('#'):
                continue
            ref_seq, alt_seq = ref_alt_seq(l)
            ref_chunks = ref_seq.split('|')
            alt_chunks = alt_seq.split('|')
            ref_seq_ss3 = ref_chunks[0][-20:] + ref_chunks[1][0:3]
            ref_seq_ss5 = ref_chunks[1][-3:] + ref_chunks[2][0:6]
            alt_seq_ss3 = alt_chunks[0][-20:] + alt_chunks[1][0:3]
            alt_seq_ss5 = alt_chunks[1][-3:] + alt_chunks[2][0:6]
            score_ref3 = score_ss(ref_seq_ss3, score3, score5)
            score_ref5 = score_ss(ref_seq_ss5, score3, score5)
            score_alt3 = score_ss(alt_seq_ss3, score3, score5)
            score_alt5 = score_ss(alt_seq_ss5, score3, score5)
            print("%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f" % (score_ref3, score_ref5, score_alt3, score_alt5, score_alt3 - score_ref3, score_alt5 - score_ref5))
