# Metagenome info table

The script **mtg_table.py** creates a csv table with the following columns:

  1. Contig name
  2. Length 
  3. Coverage (optional)
  4. GC %
  5. Contig sequence (optional)
  6. Superkingdom
  7. Phylum
  8. Order
  9. Family
  10. Genus
  11. Species
  12. Sub-species

The script requires at least two files, one (multi)fasta file and one with the taxonomic assignment file of kraken, kraken2, kaiju or any other program from which you can get a tab separated table (without headers) with the name of contig and the taxonomic id assigned to it. If you want to include the coverage of each contig you can also give the script a file with this info (must be a tab separated file without headers with the name of the contig and the coverage value).  

To run the script you’ll need the pandas library and the ete3 library. The later is used to translate the taxid and get their associated lineages to fill the table, but if you can’t install it, you can give the script a file with the taxid lineage info (again, must be a tab separated file without headers with the taxid and the lineage with each level separated by “;” (e.g. Bacteria;Proteobacteria;Gammaproteobacteria;Enterobacterales;Enterobacteriaceae;Escherichia;Escherichia coli;Escherichia coli 1240)). 

## Required arguments

| Option           | Description                                                                                                                                                                                                                                           |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -t, --taxa_assig | Taxonomy assignment file. Can be the standard output of kraken, kraken2 or kaiju, or any other program from which you can obtain a table with the name and the contig and the taxid assigned to it. That table must be tab separated and lack headers |
| -f, --fasta      | Multi-fasta file with the contigs. The contig names in this file must be same as the contig names in the taxonomy file                                                                                                                                |

## Optional arguments

| Option             | Description                                                                                                                                                                                                                                                                                                                                                                          |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -l, --lineages     | If you already have a tab separated file with the taxid in one column and the lineage in another (the lineage must be in this format: Bacteria;Proteobacteria;Gammaproteobacteria;Enterobacterales;Enterobacteriaceae;Escherichia;Escherichia coli;Escherichia coli 1240), you can specify it with this option and the script will use it to make the table without the ete3 library |
| -c, --coverage     | If you have a file with the coverage of each contig (tab separated and header; the contig names must coincide with the names in the fasta file the taxonomy assignment file) you can specify it with this option and the script will add that information to the table                                                                                                               |
| -o, --output       | Names the output file                                                                                                                                                                                                                                                                                                                                                                |
| -s, --seq_in_table | You can insert the whole sequence of each contig in the table as a field. This makes the table heavier                                                                                                                                                                                                                                                                               |
| -h, --help         | Shows the available options and exits                                                                                                                                                                                                                                                                                                                                                |

