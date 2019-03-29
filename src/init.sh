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
export samtools="/usr/bin/samtools"


## ------------------------------------ LIBSVM ------------------------------------- #
export svm_scale="$HOME/PredPSI-SVR/tools/libsvm-3.23/svm-scale"
export svm_predict="$HOME/PredPSI-SVR/tools/libsvm-3.23/svm-predict"


## ----------------------------- reference genome ---------------------------------- #
# The path to reference genome fasta files
export hg19_genome="$HOME/PredPSI-SVR/genome/hg19/hg19.fa"
