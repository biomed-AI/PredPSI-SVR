#!/usr/bin/env python3

import sys
from utils import *


if len(sys.argv) < 1:
    exit("usage: RUN transcript")

ts = load_transcripts()
with open(sys.argv[1]) as infile:
    for l in infile:
        if l.startswith('#'):
            continue
        t_id = l.strip()
        t = ts[t_id]
        print(t.strand)
