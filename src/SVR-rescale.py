#!/usr/bin/env python3

import argparse, re
import numpy as np

def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file', metavar='file', help="File for reverse scaling")
    parser.add_argument('-s', metavar='scale_file', required=True, help='svm scale parameter file')
    return parser.parse_args()

def read_scale_fn(fn):
    # fn is LIBSVM format scaling parameter file
    para_dict = dict()
    state = None
    with open(fn) as infile:
        for l in infile:
            if not state:
                if l.startswith('y'):
                    state = 'y'
                    content = 'range'
                elif l.startswith('x'):
                    state = 'x'
                    content = 'range'
            elif state == 'y':
                if content == 'range':
                    y_lower, y_upper = l.rstrip().split()
                    para_dict['y_lower_upper'] = (float(y_lower), float(y_upper))
                    content = 'min_max'
                elif content == 'min_max':
                    y_min, y_max = l.rstrip().split()
                    para_dict['y'] = (float(y_min), float(y_max))
                    state = None
            elif state == 'x':
                if content == 'range':
                    x_lower, x_upper = l.rstrip().split()
                    para_dict['x_lower_upper'] = (float(x_lower), float(x_upper))
                    content = 'min_max'
                elif content == 'min_max':
                    idx, x_min, x_max = l.rstrip().split()
                    para_dict["x_%s" % idx] = (float(x_min), float(x_max))

    return para_dict

def reverse_scale(val, minv, maxv, lower=-1, upper=1):
    raw_val = (maxv - minv) * (val - lower) / (upper - lower) + minv
    return raw_val

def simple_rescaling(fn, scale_fn):
    scale_para = read_scale_fn(scale_fn)
    y_lower, y_upper = scale_para['y_lower_upper']
    y_min, y_max = scale_para['y']
    with open(fn) as infile:
        for l in infile:
            if l.startswith('#'):
                continue
            val = float(re.split(r'\s+', l)[0])
            print(reverse_scale(val, y_min, y_max, y_lower, y_upper))

if __name__ == '__main__':
    args = get_args()
    simple_rescaling(args.file, args.s)
