
# Assignment of taxonomic identity  

## Run this script in a cluster

This script does the taxonomic profiling of the given assemblies, as well as the raw reads data. To make the taxonomic profiling, the script uses the programs Kraken (v 2.0.7) coupled with Bracken (v 2.0). The script requires that these specific versions are installed in the cluster beforehand. 

To run the script please follow the following format:

    sh Taxonomic_analysis.sh $READS_FORWARD.fastq $READS_REVERSE.fastq prefix $DIRECTORY_OF_ASSEMBLIES

THE $READS_FORWARD.fastq is the file that contains the forward raw reads.
THE $READS_REVERSE.fastq is the file that contains the reverse raw reads.
The prefix, or identifier, is added to the beginning of each output file.
The $DIRECTORY_OF_ASSEMBLIES is the location of the directory that contains the assemblies to which taxonomic annotation is done, if no path is given, the script will assume that the assemblies are located in a directory called ASSEMBLIES (the default output of the assembly script)

The outputs are organized into two folders, TAXONOMY, and TAXONOMY_LOGS. The first one contains the assemblies and the other one contains the scripts used to run the assemblers, as well as the error and output files generated during the run. 