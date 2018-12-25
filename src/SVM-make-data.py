#!/usr/bin/env python3

import argparse, os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('data', help='tag feature1 feature2 ...')
    return parser.parse_args()

def svm_format(fn):
    assert os.path.isfile(fn)
    with open(fn) as infile:
        for l in infile:
            if l.startswith('#'):
                continue
            fields = l.strip().split('\t')
            print(fields[0], end='')
            for i, t in enumerate(fields[1:]):
                print("\t%s:%s" % (i + 1, t), end='')
            print()

if __name__ == "__main__":
    args = get_args()
    svm_format(args.data)