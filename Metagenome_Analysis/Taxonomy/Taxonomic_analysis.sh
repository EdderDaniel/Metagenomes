#!/bin/bash

#To use this script please specify the name of the fastq files, first the forward file and then reverse file. 
#Please also specify the suffix that is going to be added at the beginning of each output file
#and the pathway to the directory in which the assemblies are located. 

root=$(pwd)
sign='$'

#User defined variables
FILE1=$1
FILE2=$2
suffix=$3
ASSEMBLY_dir=$4

#checks if the user gave a pathway to the assemblies directory. If it is not given, the script will assume that the assemblies are located in a directory called ASSEMBLIES 
if [ -z ${ASSEMBLY_dir+x} ]; then ASSEMBLY_dir=$4; else ASSEMBLY_dir=$root/ASSEMBLIES; fi 

#makes output directories
mkdir TAXONOMY 
mkdir TAXONOMY_LOGS
mkdir TAXONOMY_LOGS/OUTPUTS
mkdir TAXONOMY_LOGS/SCRIPTS


#This script will run the kraken taxonomic assignment for the read files and for every assembly. 
#The kraken and kraken.report files are located in TAXONOMY/KRAKEN
#This script also run the bracken taxonomic correction for the kraken output. 
#The bracken file is located in TAXONOMY/BRACKEN and the bracken.report is outputed in TAXONOMY/KRAKEN
cat  > txnmKRAKEN_BRACKEN.sh <<EOF

#PBS -N ${suffix}_KRAKEN&BRACKEN
#PBS -q ensam
#PBS -l nodes=1:ppn=12,mem=50g,vmem=50g
#PBS -q ensam
#PBS -e ${root}/TAXONOMY_LOGS/OUTPUTS/${suffix}_KRAKEN_BRACKEN.error
#PBS -o ${root}/TAXONOMY_LOGS/OUTPUTS/${suffix}_KRAKEN_BRACKEN.output
#PBS -V

module load kraken/2.0.7
module load Braken/2.0

cd $root

mkdir TAXONOMY/KRAKEN
mkdir TAXONOMY/BRACKEN

kraken2 --db kraken-db --threads 12 --paired --fastq-input $FILE1 $FILE2 --output TAXONOMY/KRAKEN/${suffix}_kraken.kraken --report TAXONOMY/KRAKEN/${suffix}_kraken.report
for i in $ASSEMBLY_dir/*fasta; do OUTPUTNAME=$sign(echo ${sign}i | sed "s/.*\///" | cut -d'.' -f1); kraken2 --db kraken-db --fasta-input ${sign}i --threads 12 --output TAXONOMY/KRAKEN/${suffix}_"${sign}OUTPUTNAME"_kraken.kraken --report TAXONOMY/KRAKEN/"${sign}OUTPUTNAME"_kraken.report; done 
for a in TAXONOMY/KRAKEN/*.report; do OUTPUTNAMEBRACKEN=${sign}(echo ${sign}a | sed "s/.*\///" | cut -d'.' -f1); bracken -d kraken-db -i ${sign}a -o TAXONOMY/BRACKEN/"${sign}OUTPUTNAMEBRACKEN".bracken; done
EOF

#Submits the TAXONOMY scripts to the cluster
for i in txnm*; do
        qsub $i
done

#moves the TAXONOMY scripts to the corresponding sub-folder
mv txnm* TAXONOMY_LOGS/SCRIPTS