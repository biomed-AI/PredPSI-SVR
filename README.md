# PredPSI-SVR

`PredPSI-SVR` was originally designed to predict ''percent spliced in (PSI, $\Psi$)'' change caused by mutations for [CAGI 5 vex-seq](https://genomeinterp,etation.org/content/vex-seq) challenge). It can be used to predict PSI change (<img src="https://latex.codecogs.com/svg.latex?\Large&space;$\Delta\Psi$" >delta PSI</img>)


## Prerequisites
- OS: Linux  
- Python 2  
- Python 3 (with `numpy` package installed)
- Perl
- ANNOVAR: http://annovar.openbioinformatics.org/en/latest  
- LIBSVM: https://www.csie.ntu.edu.tw/~cjlin/libsvm
- Samtools: http://www.htslib.org  

LIBSVM and samtools can be installed with the package manager:  
```
sudo apt install libsvm-tools samtools # Debian/Ubuntu
```



## Setup
1. Download and install LIBSVM, ANNOVAR and samtools  
2. Data preparation
    - hg19 reference genome:  
        ```shell
        wget -c http://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz
        tar -xzvf chromFa.tar.gz
        cat *.fa > hg19.fasta 
        samtools faidx hg19.fasta
        ```
    - Annovar databases:  
        `humandb` is the data folder of annovar, the default path is `annovar/humandb`
        - hg19_ensGene  
        ```
        ./annotate_variation.pl -buildver hg19 -downdb -webfrom annovar ensGene ./humandb/
        ```
        - SPIDEX  
        http://www.openbioinformatics.org/annovar/spidex_download_form.php  
        This database should also be put in `humandb`
4. Edit paths in `src/init.sh` to match the path to files or programs on your computer.  

## Usage  
Example:  

```shell
./main.sh example/sample.vcf -p example/sample.psi -o example/outdir
```
Result file is `example/outdir/OUTPUT.dpsi`

## Notes

`tools/ese3/ese3_mod.py` is modified based a script in [SilVA](http://compbio.cs.toronto.edu/silva/) tool
