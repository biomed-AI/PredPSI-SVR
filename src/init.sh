#!/bin/bash


## ---------------------------------  python --------------------------------------- #
## Both python 2 and python 3 are required, 
export python3="$HOME/miniconda3/bin/python3"
export python2="/usr/bin/python2"

## ---------------------------- ANNOVAR configuration ------------------------------ #
# You should edit the following variables to match path on your computer
export annovar="$HOME/PredPSI-SVR/tools/annovar"
export humandb="${annovar}/humandb"
# If you have configured the annovar and humandb path correctly, you don't need 
# to editfollowing variables
export annotate_variation="$annovar/annotate_variation.pl"
export convert2annovar="$annovar/convert2annovar.pl"
export table_annovar="$annovar/table_annovar.pl"
export hg19_ensGene="$humandb/hg19_ensGene.txt"


## ----------------------------------- samtools ------------------------------------ #
# If samtools was not in your system PATH, you need to edit the following 
# variable manually to set the path to samtools
export samtools="$HOME/PredPSI-SVR/tools/samtools-1.9/samtools"


## ------------------------------------ LIBSVM ------------------------------------- #
export svm_scale="$HOME/PredPSI-SVR/tools/libsvm-3.23/svm-scale"
export svm_predict="$HOME/PredPSI-SVR/tools/libsvm-3.23/svm-predict"


## ----------------------------- reference genome ---------------------------------- #
# The path to reference genome fasta files
export hg19_genome="$HOME/PredPSI-SVR/genome/hg19.fa"


## ----------------------------- Check command ------------------------------------- #
# You don't need change the following commands
>&2 echo ">>== Check commands availablity ==<<"
command -v $python2 || echo "** ERROR: check variable \"python2\" in src/init.sh" 
command -v $python3 || echo "** ERROR: check variable \"python3\" in src/init.sh" 
command -v perl || echo "** ERROR: \"perl\" can not be not found in system PATH"
command -v $samtools || echo "** ERROR: check variable \"samtools\" in src/init.sh"
command -v $svm_scale || echo "** ERROR: check variable \"svm_scale\" in src/init.sh" 
command -v $svm_predict || echo "** ERROR: check variable \"svm_predict\" in src/init.sh"
py3_version=$($python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
if ! [[ "$py3_version" == 3* ]]; then
    >&2 echo "** Error: Check the variable \"python3\" in src/init.sh"
    exit 1
fi
py2_version=$($python2 -V 2>&1 | grep -Po '(?<=Python )(.+)')
if ! [[ "$py2_version" == 2* ]]; then
    >&2 echo "** ERROR: Check the variable \"python2\" in src/init.sh"
    exit 1
fi

