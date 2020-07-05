#!/usr/bin/env python3

import argparse               
import pandas as pd 

def get_ranked_lineage(otus):

	### Makes the updated lineage file (ranked_lineages_updated.tsv), requires the ete3 library

	## Input: List with the keys of the updated_input_dic
	## Output: Generates the file ranked_lineages_updated.tsv


	from ete3 import NCBITaxa

	ncbi = NCBITaxa()    

	unique_taxa = {0: ['','','','','','',''], 1: ['Root','','','','','',''], 2: ['Bacteria','','','','','','']}
	list_of_ranks = ["superkingdom", "phylum", "class", "order", "family", "genus", "species", "subspecies"]

	ranked_lineages = []	

	for element in otus:
		if element in unique_taxa:
			lineage2add = list(unique_taxa.get(element))
			lineage2add.insert(0,element)
			ranked_lineages.append(lineage2add)
		else:

			ordered_lineage = []
			last_one = []

			lineage = ncbi.get_lineage(element)        #returns list of lineage taxids

			last_taxid = lineage[-1]
			last_one.append(last_taxid)
			last_one_name = ncbi.get_taxid_translator(last_one)
			last_taxid_name = last_one_name[last_taxid]
			how_long = len(last_taxid_name.split())

			names = ncbi.get_taxid_translator(lineage) #returns dict in which the taxids of the lineage list become the keys (int) and the translations the values. Error if there is a 0 
			lineage2ranks = ncbi.get_rank(names)       #returns a dict in which the taxids of the names become the keys (int) and the the orders the values. Error if there is a 0. It is not ordered

			for rank in list_of_ranks:
				ordered_lineage.append("")
				for key, value in lineage2ranks.items():
					if rank == value:
						last_rank = rank
						ordered_lineage.pop()
						ordered_lineage.append(names[key])
			
			if how_long == 2 and ordered_lineage[-2] == "":
				ordered_lineage[-2] = last_taxid_name

			if how_long >= 3 and ordered_lineage[-1] == "" and last_rank == "species" and ordered_lineage[-2] != last_taxid_name:
				ordered_lineage[-1] = last_taxid_name
			
			unique_taxa.update({element: ordered_lineage})

			lineage2add = list(unique_taxa.get(element))
			lineage2add.insert(0,element)
			ranked_lineages.append(lineage2add)

	ranked_lineages_table = pd.DataFrame(ranked_lineages, columns=["TAXID", "SUPERKINGDOM", "PHYLUM", "CLASS", "ORDER", "FAMILY", "GENUS", "SPECIES", "SUB_SPECIES"])
	ranked_lineages_table.to_csv("ranked_lineages_updated.tsv", sep="\t", index=False, header=True)

def get_full_lineage(otus):

	### Makes the updated lineage file (full_lineages_updated.tsv), requires the ete3 library

	## Input: List with the keys of the updated_input_dic
	## Output: Generates the file full_lineages_updated.tsv

	from ete3 import NCBITaxa

	ncbi = NCBITaxa()  

	lineages = {}  

	if 0 in otus:
		lineages.update({0: ""})
		otus.remove(0)
	if 1 in otus:
		lineages.update({1: "root"})
		otus.remove(1)
	if 2 in otus:
		lineages.update({2: "root;Bacteria"})
		otus.remove(2)

	for entrie in otus:
		lineage = ncbi.get_lineage(entrie)        #returns list of lineage taxids
		names = ncbi.get_taxid_translator(lineage).values() #returns dict in which the taxids of the lineage list become the keys (int) and the translations the values. Error if there is a 0 
		all_names = ";".join(names)
		lineages.update({entrie: all_names})

	lineages_df = pd.DataFrame(lineages.items(), columns=["OTU", "lineage"])
	lineages_df.to_csv("full_lineages_updated.tsv", sep="\t", index=False, header=True)

def updates(taxid_value,taxids2replace):

	### Reads the file with the lineages to update and make the necessary changes in the dict

	## Input: the taxid_value dic and the filename for the output
	## Output: the updated taxid_value dic 

	with open(taxids2replace) as f:
		for line in f:
			origen = int(line.split("\t")[0])
			destino = int(line.split("\t")[1])

			if origen in taxid_value and destino in taxid_value:
				suma = [sum(x) for x in zip(taxid_value[origen], taxid_value[destino])]
				taxid_value.update({destino: suma})
				del taxid_value[origen]

			else:
				taxid_value.update({destino: taxid_value[origen]})
				del taxid_value[origen]

	return(taxid_value)

def make_output(taxid_value, headers, output_file):

	### Makes the output file

	## Input: the updated taxid_value dic, the table headers and the output filename
	## Output: the output tsv file


	with open(output_file, "w") as file:
		file.write(headers+"\n")
		for key, value in taxid_value.items():
			file.write(str(key) + "\t")
			rest = '\t'.join(str(y) for y in value)
			file.write(rest+"\n")

def main():

	#### Arguments ####

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_file", required=True, 
		help="Input file (the output from get_abundances.py)")
	parser.add_argument("-t", "--taxids2replace", required = True,
		help="File with the list of taxids to change")
	parser.add_argument("-o", "--output", default= "updated_output.tsv", 
		help="Ouput filename. Default is updated_output.tsv")
	parser.add_argument("-l", "--lineage", choices=["full", "ranked"], default = "no",
		help="Generates an updated version of the lineage file (lineages_updated.tsv) with the full or ranked lineages")
	args = parser.parse_args()

	#### Arguments ####

	#### Read input file ####

	taxid_value = {}

	with open(args.input_file) as ff:
		headers = ff.readline().rstrip()
		for lines in ff:
			elements = lines.rstrip().split("\t")
			taxid_value.update({int(elements[0]): [int(x) for x in elements[1:]]})

	#### Updates taxid values and counts and prints the output ####

	updated_input_dic = updates(taxid_value, args.taxids2replace)
	make_output(updated_input_dic,headers,args.output)

	#### Makes the lineage file ####

	if args.lineage == "ranked":
		get_ranked_lineage(list(updated_input_dic.keys()))
	elif args.lineage == "full":
		get_full_lineage(list(updated_input_dic.keys()))

if __name__ == "__main__":
    main()
