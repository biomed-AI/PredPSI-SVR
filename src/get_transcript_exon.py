#!/usr/bin/env python3

import sys, os

if "TOO_PATH" in os.environ:
    TOOL_PATH = os.environ['TOOL_PATH']
else:
    TOOL_PATH = "./"

sys.path.append(os.path.join(TOOL_PATH, "src"))
from utils import *


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit("RUN avinput")
    
    find_transcripts(sys.argv[1])