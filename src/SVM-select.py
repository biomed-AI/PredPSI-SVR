#!/usr/bin/env python3

import argparse, os, re

def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('data', help="SVM data")
    parser.add_argument('-f', "--feature", help="Feature list, (default index is 0-based)")
    # parser.add_argument("--one", action="store_true", help="Change feature index to 1-based")
    return parser.parse_args()

def retrive_feature(data_fn, feature_list, tag=True):
    assert os.path.isfile(data_fn)
    feature_list = sorted(feature_list)
    with open(data_fn) as infile:
        for l in infile:
            fields = re.split(r'\s+', l.strip())
            print(fields[0], end='')
            # cnt = 0
            for f in fields[1:]:
                idx, val = f.split(':')
                if int(idx) in feature_list:
                    # cnt += 1
                    print(" %s:%s" % (feature_list.index(int(idx)) + 1, val), end='')
            print()



if __name__ == "__main__":
    args = get_args()
    with open(args.feature) as infile:
        feature_list = [int(x) + 1 for x in infile.readline().split(' ')]
    # print(feature_list)
    retrive_feature(args.data, feature_list)
