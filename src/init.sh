#!/bin/bash
## -------------------------------------------------------------- ##
## You should edit this file to make variables and aliases match
## configurations on your device
## -------------------------------------------------------------- ##

# ANNOVAR
export annovar="$HOME/Tools/annovar"
export humandb="$HOME/Data/annovar/humandb"
export annotate_variation="$annovar/annotate_variation.pl"
export convert2annovar="$annovar/convert2annovar.pl"
export table_annovar="$annovar/table_annovar.pl"
export hg19_ensGene="$HOME/Data/annovar/humandb/hg19_ensGene.txt"

# python
alias python3='/usr/bin/env python3'
alias python2='/usr/bin/env python2'

# samtools
export samtools="/usr/bin/samtools"

# LIBSVM

export svm_scale="/home/chenken/tmp/test_PredPSI-SVR_repo/libsvm-3.23/svm-scale"
export svm_predict="/home/chenken/tmp/test_PredPSI-SVR_repo/libsvm-3.23/svm-predict"

# reference genome
export hg19_genome="/home/chenken/db/hg19/hg19.fa"
