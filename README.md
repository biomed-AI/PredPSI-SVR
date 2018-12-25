# SVR-DPSI

This tool was designed to predict ''percent spliced in (PSI, $\Psi$)'' change caused by mutations.  
You can give it VCF files and it will give a $\Delta\Psi$ like [SPANR](http://tools.genes.toronto.edu)


## Prerequisites
- OS: Linux  
- Python 2  
- Python 3  
    - Numpy package installed
- Perl
- LIBSVM: https://www.csie.ntu.edu.tw/~cjlin/libsvm, LIBSVM can be installed using linux package manager on Ubuntu, Debian, etc.  
- ANNOVAR: http://annovar.openbioinformatics.org/en/latest  
- Samtools: http://www.htslib.org. Samtools can also be installed with linux package manager.  

## Setup
1. Download and install LIBSVM, ANNOVAR and samtools  
2. Data preparation
    - hg19 reference genome:  
        ```shell
        wget -c http://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz
        tar -xzvf chromFa.tar.gz
        cat *.fa > hg19.fasta 
        samtools index hg19.fasta
        ```
    - Annovar databases:  
        - hg19_ensGene  
        ```
        annotate_variation.pl -buildver hg19 -downdb -webfrom annovar ensGene /path/to/humandb/
        ```
        - SPIDEX  
        http://www.openbioinformatics.org/annovar/spidex_download_form.php  
        This database should also be put in `/path/to/humandb`
4. Edit paths in `src/init.sh` file to match the path to files or programs on your computer.  

## Usage  
Example  

```shell
./main.sh example/sample.vcf -p example sample.psi -o example/outdir
```
