#!/bin/bash

outdir="output"
buildver="hg19"
no_ref="true"
cwd=$(pwd)

while [ -n "$1" ]; do
    if [ "$1" = "-t" ]; then
        shift
        transcript_list="$1"
    elif [ "$1" = "-e" ]; then
        shift
        exon_list="$1"
    elif [ "$1" = "-o" ]; then
        shift
        outdir="$1"
    elif [ "$1" = "-p" ]; then
        shift
        PSI="$1"
    else
        vcf="$1"
    fi
    shift
done

if [ -z $vcf ] || [ ! -f $vcf ] || [ ! -f $exon_list ] || [ ! -f $transcript_list ] || [ ! -f $PSI ]; then
    echo "usage: $0 VCF [-p PSI(wild type)] [-e exon_list] [-t transcript_list] [-o outdir]"
    exit 1
fi

export TOOL_PATH=$(readlink -f `dirname $0`)

export working=$(readlink -f $outdir)

if [ ! -d $working ]; then
    mkdir -p $working
fi

# echo $buildver $vcf $working $exon_list $transcript_list

if [ ! -f "$TOOL_PATH/src/init.sh" ]; then
    echo "$TOOL_PATH/src/init.sh not found"
    exit 1
else
    source $TOOL_PATH/src/init.sh
fi

## preprocess
input_vcf="$working/input.vcf"
grep -v '^#' $vcf | cut -f 1-5 | awk '{print $0"\t.\t.\t."}' > "$working/input.vcf"

input_avinput="$working/input.avinput"
echo "** ANNOVAR annotating......"
perl $convert2annovar -format vcf4 $input_vcf > $input_avinput
perl $annotate_variation -buildver $buildver -dbtype ensGene $input_avinput $humandb -out $working/annovar
echo "    DONE"
## output: variant_function


## prepare mut_info: 
echo "** Preparing mutation info..."
## mut_info format: chrom start end ref alt enst_id exon_start exon_end (dist)
mut_info="$working/mut_info"
if [ -n "$exon_list" ]; then # known exon
    # echo "===== exon_list ====="
    if [ -n "$transcript_list" ]; then # known transcript
        # echo "===== transcript_list ====="
        # exon, transcript
        # touch $working/strand.list
        strand=$(mktemp -p $working strand_XXXXXX)
        python $TOOL_PATH/src/get_strand.py $transcript_list > $strand
        echo "  - exon transcript available ..."
        cut -f 1-5 $input_avinput | paste - $transcript_list $strand $exon_list > $mut_info || exit 1
        rm -f $strand
    else
        # exon only
        echo "  - exon only, finding exon..."
        python $TOOL_PATH/src/find_transcript_using_exon.py $working/annovar.variant_function $exon_list > $mut_info || exit 1
    fi
else
    # only have vcf information
    echo "  - only vcf, finding exon transcript..."
    python3 $TOOL_PATH/src/get_transcript_exon.py $working/annovar.variant_function  > $mut_info || exit 1
    # echo "python $TOOL_PATH/src/get_transcript_exon.py $working/annovar.variant_function  > $mut_info"
fi

grep -v "NAN" $mut_info > "${mut_info}.valid"
paste "$working/input.vcf" $mut_info | grep -v "NAN" | cut -f 1-5  > "$working/input.valid.vcf"
 
if [ -n "$PSI" ]; then
    tmp_psi=$(mktemp -p $working psi_XXXXXX)
    grep -v '#' $PSI > $tmp_psi
    PSI_valid=$working/PSI
    echo "#PSI" > $PSI_valid
    paste $mut_info $tmp_psi | grep -v "NAN" | awk '{print $NF}' >> $PSI_valid
    PSI=$PSI_valid
    rm -f $tmp_psi
fi

# Extract sequences
echo "** Extracting sequence...... "
input_seq_fa="$working/input.seq_fa"
python $TOOL_PATH/src/mark_seq.py "${mut_info}.valid" > $input_seq_fa || exit 1
echo "    DONE"

## Prepare features
echo "** Preparing features"
# MaxEntScan
echo "  - MaxEntScan... "
python $TOOL_PATH/src/maxent_score.py $input_seq_fa > $working/maxent
echo "    DONE"

# Exonic Splicing Enhancer
echo "  - ESE... "
cd $TOOL_PATH/tools/ese3
# echo "PWD1: $(pwd), PWD: $cwd"
python2 $TOOL_PATH/tools/ese3/ese3_mod.py -q $input_seq_fa > $working/ese
cd $cwd
echo "    DONE"
# echo "PWD2: $(pwd), PWD: $cwd"

# spidex
echo "  - SPIDEX... "
echo "    using ANNOVAR..."
awk '{print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t.\t.\t."}' ${mut_info}.valid > $working/input.valid.avinput
perl $table_annovar $working/input.valid.avinput $humandb -buildver hg19 -out $working/spidex -remove -protocol spidex -operation f -nastring na -csvout -polish
printf "#" > $working/spidex
cut -d ',' -f 6 $working/spidex.hg19_multianno.csv >> $working/spidex 
echo "    DONE"

## Prepare features: tag-features.tsv
echo "** Merging features...... "
printf "#tag\t" > $working/tag-features.tsv
paste $working/maxent $working/spidex $working/ese $PSI | head -n 1 >> $working/tag-features.tsv
paste $working/maxent $working/spidex $working/ese $PSI | grep -v "#" | awk '{print 0"\t"$0}' | sed 's/na/0/g' >> $working/tag-features.tsv

python3 $TOOL_PATH/src/SVM-make-data.py $working/tag-features.tsv > $working/tag-features.svm
echo "    DONE"

#
#export svm_scale=$TOOL_PATH/tools/libsvm-3.23/svm-scale
#export svm_predict=$TOOL_PATH/tools/libsvm-3.23/svm-predict

## SVM: scaling
echo "** SVM...... "
$svm_scale -r $TOOL_PATH/models/scale.paras  $working/tag-features.svm > $working/tag-features.scaled.svm

if [ -n "$PSI" ]; then
    model=$TOOL_PATH/models/PSI.model
    feature=$TOOL_PATH/models/PSI.feature
else
    model=$TOOL_PATH/models/NOPSI.model
    feature=$TOOL_PATH/models/NOPSI.feature
fi
python3 $TOOL_PATH/src/SVM-select.py -f $feature $working/tag-features.scaled.svm > $working/tag-features.scaled.select.svm

$svm_predict $working/tag-features.scaled.select.svm $model $working/out-prediction.raw

cut -f 1 $working/out-prediction.raw > $working/out.dpsi.raw

printf "#Chrom\tPosition\tID\tRef\tAlt\tdelta-PSI\n" > $working/OUTPUT.dpsi
python3 $TOOL_PATH/src/SVR-rescale.py -s $TOOL_PATH/models/scale.paras $working/out.dpsi.raw | paste $working/input.valid.vcf - >> $working/OUTPUT.dpsi 
echo "    DONE"

## clean
test -d $working/others || mkdir $working/others
mv -f $working/annovar.* $working/spidex.hg* $working/others
mv -f $working/ese $working/spidex $working/maxent $working/others
test -e $working/PSI && mv $working/PSI $working/others
mv -f $working/input* $working/mut_info* $working/others
mv -f $working/tag-features* $working/out* $working/others

printf "\n=================================================================\n\n"
echo "Finished at $(date)"
echo "Prediction file: $working/OUTPUT.dpsi"
printf "\n=================================================================\n\n"
