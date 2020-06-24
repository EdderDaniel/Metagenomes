# Taxid counts 

## Get abundances 

This tool allows you to merge the output of many classifiers in one table which can be used in downstream analyses. 

The **get_abundances.py** script takes as input the output files of taxonomic profilers such as [kraken2](https://github.com/DerrickWood/kraken2) or [kaiju](http://kaiju.binf.ku.dk) (both of which are automatically detected) or any other taxonomic profilers from which you can obtain a tsv file (with no headers) in which you have the reads/contigs in one column and their respective assigned taxid in another. This excludes profilers that only report back the percentages per taxonomic group, for example. 

### Required arguments

| Option          | Description                                |
|-----------------|--------------------------------------------|
| -i, --input_dir | Path to the location of the files to merge |

### Optional arguments

| Option             | Description                                                                                                                                                                                                                                                                                                                                                                                           |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -o, --output       | Name of the output file. The default output name is “output.tsv”                                                                                                                                                                                                                                                                                                                                      |
| -u, --unclassified | The default is to include the unclassified reads/contigs from the output, but if you don’t want them specify the no option for this argument                                                                                                                                                                                                                                                          |
| -e, --extension    | Add the extension (without the dot) of the files that you want to merge. By default the script will use every file in the directory.                                                                                                                                                                                                                                                                  |
| -l, --lineage      | Generates a second output file (lineages.tsv) with the taxonomic lineage of each taxid present in the table.  There are two options, full and ranks. **full** gives the full taxonomic lineage,  while **ranks** eliminates every non ranked group and gives back only the lineage with these ranks:  superkingdom, phylum, class, order, family, genus, species and sub-species (most of the times). |
| -h                 | Shows the available options and exits                                                                                                                                                                                                                                                                                                                                                                 |

## Update abundances

If your local copy of the NCBI taxonomy (which is downloaded and used by the etet3 library) and the taxonomy used by the classier differs, you might see something like this in your terminal when running the **get_abundances.py** script:

		~/ete3/ncbi_taxonomy/ncbiquery.py:240: UserWarning: taxid 2219703 was translated into 2650924
  	warnings.warn("taxid %s was translated into %s" %(taxid, merged_conversion[taxid]))

To deal with this problem you can use the **update_taxonomy.sh** script. 

First, copy all of the warnings and put them in a tsv file (without headers) in which you have the original taxid in one column and the translation in another. For previous example the table should look like this:

| 2219703 | 2650924 |
|---------|---------|

With this file and the output file from the **get_abundances.py** you can now run the  **update_taxonomy.sh** script.

### Required arguments

| Option               | Description                                                |
|----------------------|------------------------------------------------------------|
| -i, --input_file     | Path to the input file obtained from **get_abundances.py** |
| -t, --taxids2replace | Path to the file with the taxis that need to be changed (the tsv file that i mentioned earlier)    |

### Optional arguments

| Option        | Description                                                                                                                                                                                            |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -o, --output  | Output filename. The default is updated_output.tsv                                                                                                                                                     |
| -l, --lineage | If you want to generate an updated lineage file you can use this option. As in the previous script, the options are ranked, to get only the named taxonomical order, and full, to get the full lineage |
| -h            | Shows the available options and exits                                                                                                                                                                  |
