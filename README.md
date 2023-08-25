# MATES
A Deep Learning-Based Model for Quantifying Transposable Elements in Single-Cell Sequencing Data

## Overview
<img title="Model Overview" alt="Alt text" src="/figures/Model-figure-01.png">

## Installation
### Prerequisites
samtools == 1.17
```sh
conda install -c bioconda samtools
```
bedtools == 2.31.0
```sh
conda install -c bioconda bedtools
```
For other dependencies you san simply run:
```sh
pip3 install -r requirements.txt 
```

### Installing MATES
To install MATES, you can run the following command:
```sh
    git clone https://github.com/mcgilldinglab/MATES.git
    pip3 install MATES==0.1
```
## Usage
### Step 0: Alignment
The raw fastq files are aligned using STAR-Solo for 10X scRNA-seq / scATAC-seq Data and STAR for Smart-Seq2 scRNA-seq Data to reserve multimapping reads. 

- A sample alignment command line for **10X scRNA/scATAC** Data:
```sh
STAR --soloType CB_UMI_Simple --soloCBwhitelist barcode_whitelist \
	--soloMultiMappers EM --runThreadN 64 --genomeDir path_to_genome \
	--outFileNamePrefix STAR_Solo/sample_name --readFilesCommand zcat \
	--readFilesIn sample_name_R1_001.fastq.gz sample_name_R3_001.fastq.gz sample_name_R2_001.fastq.gz \
	--outSAMtype BAM SortedByCoordinate --quantMode GeneCounts \
	--outSAMattributes CR UR CY UY CB UB NH HI
```
> The barcode whitelist can be found at **barcode_whitelist** folder, the original data can be obtained from  https://kb.10xgenomics.com/hc/en-us/articles/115004506263-What-is-a-barcode-whitelist- \
> The filtered cell barcodes file provide by STAR-Solo will be at **STAR_Solo/sample_name/sample_name.out/Gene/filtered/barcodes.tsv**, if you have your own filtered barcodes file, you can simply replace it at the same location.

- A sample alignment command line for **Smaert-seq2 scRNA** Data:
```sh
STAR --runThreadN 64 --genomeDir path_to_genome --readFilesCommand zcat \
        --outFileNamePrefix STAR_Solo/sample/sample_ \
        --readFilesIn sample/sample_1.fastq.gz sample/sample_2.fastq.gz \
        --outSAMtype BAM SortedByCoordinate --quantMode GeneCounts
```

## Tutorial:
### Training MATES on 10x scRNA-seq dataset
<!-- ### Training MATES on Smart-seq2 scRNA dataset -->
### Training MATES on 10x scATAC-seq dataset

<!-- ### Step 1: Building Transposon Element(TE) Reference
The default option of our tool/procedure involves the removal of all transposable element (TE) regions that share overlapping base pairs with gene references. This step is taken to prevent any potential information leakage. The TE reference data is sourced from repeatmasker and the Gene reference data is sourced from ebi.

To build the reference:
```sh
## for human data
python build_reference.py Human 
## for mouse data
python build_reference.py Mouse 
```
If you have your own TE/Gene reference, you can only run the last command, make sure they are at the csv format with following columns:
```sh
## for mouse, name refernce to mm_TEs.csv and mm_Genes.csv
## for human, name reference to hg_TEs.csv and hg_Genes.csv
##Note: The first column of TE reference must be index and score column is optional.
cat mm_TEs.csv | head -n 3
,TE_chrom,start,end,score,strand,TE_Name,TE_Fam
0,chr1,10001,10468,(248945954),+,(TAACCC)n,Simple_repeat
1,chr1,10469,11447,(248944975),-,TAR1,Satellite/telo

cat mm_Genes.csv | head -n 3
Chromosome,Feature,Start,End,Strand,gene_id,gene_name
chr1,gene,3073252,3074322,+,ENSMUSG00000102693.1,4933401J01Rik
chr1,transcript,3073252,3074322,+,ENSMUSG00000102693.1,4933401J01Rik
``` -->

<!-- ### Step 2: Training Preparation
#### For scRNA data and scATAC data
The follwing procedure not require GPU usage.
```sh
sh training_preparation.sh -t threads_num -f file_name -p path_to_bam --TE_mode TE_mode --data_mode data_mode --bin_size bin_size --proportion proportion

##Usage
# -t Threads number
# -f File contains sample name
# -p Path to STAR/STAR_Solo aligned bam folder
# --TE_mode exlusive or inclusive, represents whether keep the TE instances with gene, the default will be exclusive
# --data_mode 10X or Smart_seq
# --bin_size Bin size for identifying U/M region
# --proportion Proportion of dominating U/M reads in region
```
#### For Multi-omics Data

### Step 3: Training and Prediction
This step **requires GPU availablity**, after running the below command, will provide the resulted TE matrices inclusing unique TE matrix, multi TE matrix and combined final matrix.
#### For scRNA data and scATAC data
``` sh
sh model_training.sh -f file_name --data_mode data_mode --bin_size bin_size --proportion proportion

##Usage
# -f File contains sample name
# --data_mode 10X or Smart_seq
# --bin_size Bin size for identifying U/M region
# --proportion Proportion of dominating U/M reads in region
```
#### For Multi-omics Data

### Step 4: Downstrem Analysis -->

