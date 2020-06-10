# Metagenomas-EvoDivMet
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

The script requires two files, one (multi)fasta file and one with the taxonomic assignment file of kraken, kraken2, kaiju or any other program from which you can get a tab separated table (without headers) with the name of contig and the taxonomic id assigned to it. If you want to include the coverage of each contig you can also give the script a file with this info (must be a tab separated file without headers with the name of the contig and the coverage value).  

To run the script you’ll need the pandas library and the ete3 library. The later is used to translate the taxid and get their associated lineages to fill the table, but if you can’t install it, you can give the script a file with the taxid lineage info (again, must be a tab separated file without headers with the taxid and the lineage with each level separated by “;” (e.g. Bacteria;Proteobacteria;Gammaproteobacteria;Enterobacterales;Enterobacteriaceae;Escherichia;Escherichia coli;Escherichia coli 1240)). 

Run python3 mtg_table.py -h for more info on other options. 
