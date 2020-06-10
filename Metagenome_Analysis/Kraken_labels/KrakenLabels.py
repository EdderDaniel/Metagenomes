#Please install ete3 module before runing the script

#Please make sure to give a well formed .kraken file as input, or 
#the script will either return a blank file or an error 

#The "taxdump.tar.gz" and this script file must be located in the same directory 
#If the "taxdump.tar.gz" file in not found in the script directory, the script will try to download it from the NCBI website,
#for which an internet conexion is requires

import sys
from ete3 import NCBITaxa

ncbi = NCBITaxa()

filepath = sys.argv[1]

unique_taxonomic_elements = {1: "Root", 2: "Bacteria"}          #This dictionary contains the unique taxonomic elements

with open(filepath) as f, open("output.labels", "w") as ff:     #Opens the .krakenfile given by the user and creates the "output.labels" file
	for line in f:

		kraken_arguments = line.split()                         #Splits every tab separed column in the .kraken file
		if (kraken_arguments[0] == "U"):                        #Since .labels files do not contain Unassigned contigs, these are overlooked 
			continue 
		contig_name = (kraken_arguments[1])                     #Takes the name of the conting, as given in the .kraken file
		taxid = int(kraken_arguments[2])						#Takes the taxonomic id of the contig, as given in the .kraken file
		if taxid in unique_taxonomic_elements:
			ff.write("{}	{}\n".format(contig_name, unique_taxonomic_elements[taxid]))    #If the taxomic id of a particular contig is in the unique_taxonomic_elements dictionary
			continue                                                                        #then its taxonomic information is retrived from there and the output line (contig name and taxonomic lineage) is written into the "output.labels" file
		else: 
			lineage = ncbi.get_lineage(taxid)
			names = ncbi.get_taxid_translator(lineage)                      #If the taxonomic id of a particular contig is not in the unique_taxonomic_elements dictionary, then the script will
			tax_info = (";".join([names[taxid] for taxid in lineage]))      #search for its taxonomic lineage in the "taxdump.tar.gz" file, put it in the .label format (; separated),
			unique_taxonomic_elements.update({taxid: tax_info})             #add it to the unique_taxonomic_elements dictionary and write the output line (contig name and taxonomic lineage) to the "output.labels" file
			ff.write("{}	{}\n".format(contig_name, tax_info))
