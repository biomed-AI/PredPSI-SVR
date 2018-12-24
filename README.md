# SVR-DPSI

## Requirements  
- OS: Linux  
- Python environment:  
    - Python 2
    - Python 3 & Numpy
- Perl

## Other Tools Involved  
- [LIBSVM](https://www.csie.ntu.edu.tw/~cjlin/libsvm/)  
- [ANNOVAR](http://annovar.openbioinformatics.org/en/latest/)  
- [Samtools](http://www.htslib.org/)  

## Preparation before Using
1. Download and install LIBSVM, ANNOVAR and samtools  
2. Download data needed  
    - hg19 reference genome  
    - Annovar databases:  
        - SPIDEX
        - hg19_ensGene
3. Index the reference genome  
    `$ samtools index /path/to/hg19/genome.fasta` (This step takes about 1 hour at least)
4. Edit paths in src/init.sh file to match your computer's settings