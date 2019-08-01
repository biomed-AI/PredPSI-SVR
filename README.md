# PredPSI-SVR

`PredPSI-SVR` was designed to predict the change of percent spliced in (delta-PSI or <img src="https://latex.codecogs.com/svg.latex?\Delta\Psi" />) caused by genetic variants for the [CAGI 5 vex-seq](https://genomeinterpretation.org/content/vex-seq) challenge.  
- About <img src="http://latex.codecogs.com/svg.latex?\Psi" /> and <img src="https://latex.codecogs.com/svg.latex?\Delta\Psi" />: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3037023/  

Send questions and comments to chenkenbio@gmail.com

## Requirements
- Operation system: Unix/Linux  
- Memory: 4GB at least
- `Perl` in your PATH  
- `Python 2`  
- `Python 3` (with `numpy` package installed)  
If you have trouble installing `python 3` or `numpy`, you can try `miniconda`  
    ```shell
    cd ~/Downloads
    wget -c https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    chmod +x Miniconda3-latest-Linux-x86_64.sh
    ./Miniconda3-latest-Linux-x86_64.sh             #pay attention to path of installation, we'll use the default path "$HOME/miniconda3" in this tutorial 
    source $HOME/miniconda/bin/activate
    pip install numpy
    ```

## Getting started
### Preparation  
Note: If you have the following packages installed on your system, you can skip installing them and just edit path in `src/init.sh`   
**We put PrePSI-SVR in $HOME directory as default**   
1. Download `PredPSI-SVR`, 
    ```shell
    cd ~
    git clone https://github.com/chenkenbio/PredPSI-SVR
    ```
2. Download `ANNOVAR` (http://annovar.openbioinformatics.org/en/latest/user-guide/download/), `libsvm` (https://www.csie.ntu.edu.tw/~cjlin/libsvm), and `samtools` (http://www.htslib.org/download/). And move them to `PredPSI-SVR/tools`.  
3. Extract packages:  
    ```shell
    cd ~/PredPSI-SVR/tools
    tar -xzvf annovar.latest.tar.gz
    tar -xzvf libsvm-3.23.tar.gz
    tar -xjvf samtools-1.9.tar.bz2
    cd libsvm-3.23
    make all
    cd ../samtools-1.9
    make all
    cd ..
    ```

4. Download basic annotation databases for `ANNOVAR`  

    ```shell

    cd ~/PredPSI-SVR/tools/annovar        # PredPSI-SVR/tools
    ./annotate_variation.pl -buildver hg19 -downdb -webfrom annovar ensGene ./humandb/
    ```

5. Download third-party database [SPIDEX](http://tools.genes.toronto.edu/) from http://www.openbioinformatics.org/annovar/spidex_download_form.php. Move it to `~/PredPSI-SVR/tools/annovar/humandb/` and decompress with `unzip`:
```shell
unzip hg19_spidex.zip        #working directory: PredPSI-SVR/tools/annovar/humandb
```


6. Download hg19 genome  
```shell
cd ~/PredPSI-SVR/genome
wget -c http://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz
cat *.fa > hg19.fasta
$HOME/PredPSI-SVR/tools/samtools-1.9/samtools faidx hg19.fasta
```

7. **Finally**, check variables in `src/init.sh`, edit them to fit your system  

### Usage  
Example:  

```shell
cd ~/PredPSI-SVR/
## PredPSI-SVR, with "-p" option
./main.sh example/sample.vcf -p example/sample.psi -o example/outdir
## PredPSI-SVR-noPSI, with out "-p"
./main.sh example/sample.vcf -o example/outdir
```
Result file is `example/outdir/OUTPUT.dpsi`

### Attention:  
The `PredPSI-SVR` will filter the VCF file at first to remove variants in intergenic regions or distant to splice sites (more than 200 bp ). Threrefore sometimes you will find that there are fewer variants in `OUTPUT.psi` than your input VCF file.  

## References

`PredPSI-SVR/tools/ese3/ese3_mod.py` is modified based a script in [SilVA](http://compbio.cs.toronto.edu/silva/) package (Paper: https://www.ncbi.nlm.nih.gov/pubmed/23736532, GitHub: https://github.com/buske/silva)
