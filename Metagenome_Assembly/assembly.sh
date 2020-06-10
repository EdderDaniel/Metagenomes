#!/bin/bash

#This program requies that the user specify 3 things in order. The first one is the name of the reads file with the forward sequences
#The sencond one is the name of the reads file with the reverse sequences. The third one is a the suffix that will be added at the begenning of each output file
#If the reads files are not in the same directory as this script, please provide it   

FILE1=$1 #Reads file with the forward sequences 
FILE2=$2 #Reads file with the reverse sequences 
prefix=$3 #Suffix to be appended at the begenning of the files 

root=$(pwd) #Gets the path to the directory of this file, on which the outputs ought to be created 
sign='$'    

#Creates the outputs directories 
mkdir ASSEMBLIES
mkdir ASSEMBLY_STATS
mkdir ASSEMBLY_STATS/OUTPUTS
mkdir ASSEMBLY_STATS/SCRIPTS

#Creates the file that will run the Metaspades and spades assemblers
#While the metaspades assembler runs with standard parameters, the spades assembler uses the best k-mer found by metaspades,
#and two more values, one smaller and one bigger. For example, if the best k-mer value found by metaspades was 51, the values that 
#spades will uses will be 49, 51, and 53.  
cat > runMETASPADES_SPADES.sh <<EOF
#PBS -N ${prefix}_META&SPADES
#PBS -q ensam
#PBS -l nodes=1:ppn=16,mem=80g,vmem=80g
#PBS -q ensam
#PBS -e ${root}/ASSEMBLY_STATS/OUTPUTS/${prefix}_META_SPADES.error
#PBS -o ${root}/ASSEMBLY_STATS/OUTPUTS/${prefix}_META_SPADES.output
#PBS -V

module load SPAdes/3.10.1

cd $root

metaspades.py --pe1-1 $FILE1 --pe1-2 $FILE2 -o METASPADES

KMER_SCAFFOLD=$sign(grep '/scaffolds' $root/METASPADES/spades.log | head -n 1 | cut -d'/' -f10 | tr -dc '0-9')

KMER_SCAFFOLD_Minus2=$sign(echo "$sign((KMER_SCAFFOLD - 2))")
KMER_SCAFFOLD_Plus2=$sign(echo "$sign((KMER_SCAFFOLD + 2))")
KMER_SCAFFOLD_Minus4=$sign(echo "$sign((KMER_SCAFFOLD - 4))")
KMER_SCAFFOLD_Plus4=$sign(echo "$sign((KMER_SCAFFOLD + 4))")

spades.py -1 $FILE1 -2 $FILE2 -k ${sign}KMER_SCAFFOLD_Minus4,${sign}KMER_SCAFFOLD_Minus2,${sign}KMER_SCAFFOLD,${sign}KMER_SCAFFOLD_Plus2,${sign}KMER_SCAFFOLD_Plus4 --cov-cutoff auto -o SPADES || spades.py -1 $FILE1 -2 $FILE2 --cov-cutoff auto -o SPADES

cp METASPADES/scaffolds.fasta ASSEMBLIES/${prefix}_metaspades_scaffolds.fasta 2>>/dev/null || cp METASPADES/contigs.fasta ASSEMBLIES/${prefix}_metaspades_contigs.fasta
cp SPADES/scaffolds.fasta ASSEMBLIES/${prefix}_spades_scaffolds.fasta 2>>/dev/null || cp SPADES/contigs.fasta ASSEMBLIES/${prefix}_spades_contigs.fasta
EOF

#Creates the file that will run the IDBA-UD assembler. 
cat > runIDBA.sh <<EOF1
#PBS -N ${prefix}_IDBA-UD
#PBS -q ensam
#PBS -l nodes=1:ppn=16,mem=80g,vmem=80g
#PBS -q ensam
#PBS -e ${root}/ASSEMBLY_STATS/OUTPUTS/${prefix}_idba.error
#PBS -o ${root}/ASSEMBLY_STATS/OUTPUTS/${prefix}_idba.output
#PBS -V

module load idba/2.0

cd $root
mkdir IDBA-UD

fq2fa --merge --filter $FILE1 $FILE2 $root/IDBA-UD/MERGED_READS.fa
idba_ud -r $root/IDBA-UD/MERGED_READS.fa --num_threads 16 -o $root/IDBA-UD
cp IDBA-UD/scaffold.fa ASSEMBLIES/${prefix}_idbaud_scaffolds.fasta 2>>/dev/null || cp IDBA-UD/contig.fa ASSEMBLIES/${prefix}_idbaud_contigs.fasta
EOF1

#Creates the file that will run the MEGAHIT assembler
cat > runMEGAHIT.sh <<EOF2
#PBS -N ${prefix}_MEGAHIT
#PBS -q ensam
#PBS -l nodes=1:ppn=16,mem=80g,vmem=80g
#PBS -q ensam
#PBS -e ${root}/ASSEMBLY_STATS/OUTPUTS/${prefix}_MEGAHIT.error
#PBS -o ${root}/ASSEMBLY_STATS/OUTPUTS/${prefix}_MEGAHIT.output
#PBS -V

module load megahit/1.1.2

cd $root

megahit -1 $FILE1 -2 $FILE2 -t 16 -o $root/MEGAHIT
cp MEGAHIT/final.contigs.fa ASSEMBLIES/${prefix}_megahit_contigs.fasta 2>>/dev/null
EOF2

#Loop that submit all the assembly jobs.
for i in run*; do
        qsub $i
done

#Moves the assembly scripts to the corresponding folder
mv run* ASSEMBLY_STATS/SCRIPTS