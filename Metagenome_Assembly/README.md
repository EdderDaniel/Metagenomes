
# Metagenome assembly 

## Run this script in a cluster

This script assembly pair-end short reads using four assemblers: MEGAHIT (v 1.1.2), IDBA-UD (v 2.0), MetaSPAdes and SPAdes (v 3.10.1). The script requires that these specific versions are installed in the cluster beforehand. 

To run the script please follow the following format:

    sh assembly.sh $READS_FORWARD.fastq $READS_REVERSE.fastq prefix

THE $READS_FORWARD.fastq is the file that contains the forward raw reads.
THE $READS_REVERSE.fastq is the file that contains the reverse raw reads.
The prefix, or assembly's name, is added to the beginning of each output file.  

The outputs are organized into two folders, ASSEMBLIES, and ASSEMBLY_LOGS. The first one contains the assemblies and the other one contains the scripts used to run the assemblers, as well as the error and output files generated during the run. 