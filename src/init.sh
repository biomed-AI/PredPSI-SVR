#!/bin/bash

## Detailed description is available on https://github.com/chenkenbio/PredPSI-SVR


# Edit the following variables based on the configurations on your system
## ---------------------------------  python --------------------------------------- #
export python3="$HOME/miniconda3/bin/python3"
export python2="/usr/bin/python2"

## ---------------------------- ANNOVAR configuration ------------------------------ #
export annovar="$HOME/PredPSI-SVR/tools/annovar"
export humandb="${annovar}/humandb"
export annotate_variation="$annovar/annotate_variation.pl"
export convert2annovar="$annovar/convert2annovar.pl"
export table_annovar="$annovar/table_annovar.pl"
export hg19_ensGene="$humandb/hg19_ensGene.txt"

## ----------------------------------- samtools ------------------------------------ #
export samtools="$HOME/PredPSI-SVR/tools/samtools-1.9/samtools"

## ------------------------------------ LIBSVM ------------------------------------- #
# If 'svm_scale' or 'svm_predict' was not in your system PATH, 
# you need to edit the following variables
export svm_scale="$HOME/PredPSI-SVR/tools/libsvm-3.23/svm-scale"
export svm_predict="$HOME/PredPSI-SVR/tools/libsvm-3.23/svm-predict"

## ----------------------------- reference genome ---------------------------------- #
export hg19_genome="$HOME/PredPSI-SVR/genome/hg19.fasta"




## ------------------------ Check commands and data -------------------------------- #
# You don't need change the following commands
echo ">>== Check commands availablity ==<<" 1>&2
command -v $python2 || echo "** ERROR: check variable \"python2\" in src/init.sh" 1>&2
command -v $python3 || echo "** ERROR: check variable \"python3\" in src/init.sh" 1>&2
command -v perl || echo "** ERROR: \"perl\" can not be not found in system PATH" 1>&2
command -v $samtools || echo "** ERROR: check variable \"samtools\" in src/init.sh" 1>&2
command -v $svm_scale || echo "** ERROR: check variable \"svm_scale\" in src/init.sh" 1>&2
command -v $svm_predict || echo "** ERROR: check variable \"svm_predict\" in src/init.sh" 1>&2
py3_version=$($python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
if ! [[ "$py3_version" == 3* ]]; then
    echo "** Error: Check the variable \"python3\" in src/init.sh" 1>&2
    exit 1
fi
py2_version=$($python2 -V 2>&1 | grep -Po '(?<=Python )(.+)')
if ! [[ "$py2_version" == 2* ]]; then
    echo "** ERROR: Check the variable \"python2\" in src/init.sh" 1>&2
    exit 1
fi

if [ ! -f $hg19_genome ]; then
    echo "** ERROR: hg19 genome not found! check \"hg19_genome\" in src/init.sh" 1>&2
    exit 1
elif [ ! -f ${hg19_genome}.fai ]; then
    echo "** Indexing $hg19_genome, it may take a long time..." 1>&2
    $samtools faidx $hg19_genome && echo "** Indexing finished." 1>&2
fi
