
# Repository of scripts used in the analysis of metagenomic data 

This repository contains scripts used to analyze metagenomic data. Most of the scripts are written in Python 3 and require the pandas and ETE toolkit libraries. Please install them before using the scripts. 

### Summary of the scripts 

1. **Kraken_labels**: This script generates the labels file that was deprecated in Kraken2

2. **Metagenome_Info_Table**: This script generates a CSV table with taxonomic data (previously generated with a profiling program) and intrinsic data (such as length or GC %) of each contig or scaffold in an assembly

3. **Taxids_counts**: Makes a summary table with a count of how many reads/contigs are assigned to each taxid from the output of different taxonomic profilers

