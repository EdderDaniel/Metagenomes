#!/usr/bin/env python3

import argparse               
import pandas as pd 

def get_name_taxa(taxassig_file):

	##############

	# Function to put the taxonomic assignment file in a pandas dataframe. It checks if the first element is a U or C, which is the first element of the output of 
	# kraken, kraken2 and kaiju. If the file is the output of one of those programs it’ll get the necessary information from them automatically. If not,  it’ll try to 
	# get the info from a tab separated file (without headers) with the name of the contig and the taxid assigned to it. 


	##############

	try:
		with open(taxassig_file) as checkfile:
			firstchar = checkfile.read(1)
	except:
		raise Exception("Error! Is this {} a valid file?".format(taxassig_file))

	if firstchar == "C" or firstchar == "U":
		taxassig_data = pd.read_csv(taxassig_file, sep="\t", error_bad_lines=False, usecols=[1,2], names=["NAME", "TAXID"])
	else:
		taxassig_data = pd.read_csv(taxassig_file, sep="\t", error_bad_lines=False, usecols=[0,1], names=["NAME", "TAXID"])

	return(taxassig_data)

def get_taxa_lineages(taxa_table):

	##############

	# Function to get the lineages of each taxid by using NCBI taxonomy. 
	# To do this, the script uses the ete3 library, so that one needs to be installed beforehand. 
	# Aside from getting the full taxonomic lineage, the function also removes any intermediate taxonomical group and
	# adds the lineage to the taxonomic info table
	# I couldn’t figure out an easy way to include sub-species since it’s not a recognized taxonomic group.


	##############

	from ete3 import NCBITaxa

	ncbi = NCBITaxa()    

	all_taxids_list = taxa_table["TAXID"].tolist()

	unique_taxa = {0: ['','','','','','',''], 1: ['Root','','','','','',''], 2: ['Bacteria','','','','','','']}
	list_of_ranks = ["superkingdom", "phylum", "class", "order", "family", "genus", "species", "subspecies"]

	all_lineages = []	

	for element in all_taxids_list:
		if element in unique_taxa:
			lineage2add = list(unique_taxa.get(element))
			lineage2add.insert(0,element)
			all_lineages.append(lineage2add)
		else:

			ordered_lineage = []

			lineage = ncbi.get_lineage(element)        #returns list of lineage taxids
			names = ncbi.get_taxid_translator(lineage) #returns dict in which the taxids of the lineage list become the keys (int) and the translations the values. Error if there is a 0 
			lineage2ranks = ncbi.get_rank(names)       #returns a dict in which the taxids of the names become the keys (int) and the the orders the values. Error if there is a 0. It is not ordered

			for rank in list_of_ranks:
				ordered_lineage.append("")
				for key, value in lineage2ranks.items():
					if rank == value:
						ordered_lineage.pop()
						ordered_lineage.append(names[key])
			
			unique_taxa.update({element: ordered_lineage})

			lineage2add = list(unique_taxa.get(element))
			lineage2add.insert(0,element)
			all_lineages.append(lineage2add)

	all_lineages_table = pd.DataFrame(all_lineages, columns=["TAXID", "SUPERKINGDOM", "PHYLUM", "CLASS", "ORDER", "FAMILY", "GENUS", "SPECIES", "SUB_SPECIES"])
	complete_taxa_lineages_table = taxa_table.merge(all_lineages_table, how = "inner", on="TAXID", left_index=True, right_index=True)

	return(complete_taxa_lineages_table)

def process_lineages(lineages_file, taxa_table):

	##############

	# Function that the reads the lineage file (tab separated, no headers and with two columns, one with the taxid and one with the lineage separated by “;” ).
	# The lineage file must have every taxid represented in the taxonomic assignment file at least once or the script will die.


	##############

	unique_taxa = {}
	all_lineages = []

	all_taxids_list = taxa_table["TAXID"].tolist()

	with open(lineages_file) as lineages:

		for line in lineages:
			taxid = int(line.split("	")[0])
			
			if taxid in unique_taxa:
				continue
			else:
				lineage = line.rstrip().split("	")[1].split(";") #If the lineages are separated by something other than ; change this line to be able to read them
				unique_taxa.update({taxid: lineage})

	for entrie in all_taxids_list:
		lineage2add = list(unique_taxa.get(entrie))
		lineage2add.insert(0,entrie)
		all_lineages.append(lineage2add)

	all_lineages_table = pd.DataFrame(all_lineages, columns=["TAXID", "SUPERKINGDOM", "PHYLUM", "CLASS", "ORDER", "FAMILY", "GENUS", "SPECIES", "SUB_SPECIES"])
	complete_taxa_lineages_table = taxa_table.merge(all_lineages_table, how = "inner", on="TAXID", left_index=True, right_index=True)

	return(complete_taxa_lineages_table)

def get_coverage(coverage_file,fasta_table):

	##############

	# Reads the coverage file and add that info to the table. 
	# The coverage file be a tab separated file without headers, and with 2 columns: The first one for the name of the contig and one for the coverage value


	##############

	coverage_table = pd.read_csv(coverage_file, sep="\t", error_bad_lines=False, names=["NAME", "COVERAGE"])
	fasta_coverage_table = fasta_table.merge(coverage_table, how="inner", on="NAME")
	return(fasta_coverage_table)

def fasta_process(fasta_file):

	##############

	# Function that reads the fasta file, gets each contig's name, length, GC % and sequence and put them in a pandas dataframe


	##############

	names = []
	all_GC = []
	all_sequences = []
	all_lengths = []
	sequence = "GC"

	with open(fasta_file) as fasta:              
		for line in fasta:
			if line[0] == ">":

				header = line.rstrip()
				seq_len = int(len(sequence))
				GC_content = float((sequence.count('G') + sequence.count('C'))) / seq_len * 100
				
				names.append(header[1:])
				all_sequences.append(sequence)
				all_lengths.append(seq_len)
				all_GC.append(GC_content)

				sequence = ""

			else:
				sequence += line.upper().rstrip()

		all_GC.pop(0)
		all_lengths.pop(0)
		all_sequences.pop(0)

		fasta_data = pd.DataFrame(list(zip(names,all_lengths,all_GC,all_sequences)), columns=["NAME", "LENGTH", "GC", "SEQUENCE"])

		return(fasta_data)

def fasta_process_noseq(fasta_file):

	##############

	# Function that reads the fasta file, gets each contig's name, length and GC % and put them in a pandas dataframe


	##############

	names = []
	all_GC = []
	all_lengths = []
	sequence = "GC"

	with open(fasta_file) as fasta:              
		for line in fasta:
			if line[0] == ">":

				header = line.rstrip()
				seq_len = int(len(sequence))
				GC_content = float((sequence.count('G') + sequence.count('C'))) / seq_len * 100
				
				names.append(header[1:])
				all_lengths.append(seq_len)
				all_GC.append(GC_content)

				sequence = ""

			else:
				sequence += line.upper().rstrip()

		all_GC.pop(0)
		all_lengths.pop(0)

		fasta_data = pd.DataFrame(list(zip(names,all_lengths,all_GC)), columns=["NAME", "LENGTH", "GC"])

		return(fasta_data)

def main():


	####### Arguments #######

	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--fasta", dest="fasta_file", required=True, 
		help="Direction to the assembly file")
	parser.add_argument("-t", "--taxa_assig", dest="taxassig_file", required=True, 
		help="Direction to the taxonomic assignment file. Can be kraken, kraken2, kaiju or a tsv with the contig name and the taxid, without headers")
	parser.add_argument("-l", "--lineages", dest="lineages_file", default=" ",
		help="if you have a lineages file you can use it and the script will not compute them. Otherwhise, the scirpt will attempt to get them using the ete3 library")
	parser.add_argument("-c", "--coverage", dest="coverage_file", default=" ",
		help="Direction to the coverage file")
	parser.add_argument("-o", "--output", default= "output.csv", 
		help="Ouput filename. Default is output.csv")
	parser.add_argument("-s", "--seq_in_table", dest="seqsin", default="yes", choices=["yes", "no"], 
		help="Add whole contig sequence as a column. Default is yes")
	
	args = parser.parse_args()

	####### Arguments #######
	

	####### Call the functions according to the passed arguments #######

	taxa_table = get_name_taxa(args.taxassig_file)

	if args.seqsin == "yes":
		fasta_table = fasta_process(args.fasta_file)
	else:
		fasta_table = fasta_process_noseq(args.fasta_file)

	if args.coverage_file != " ":
		fasta_table = get_coverage(args.coverage_file,fasta_table)

	if args.lineages_file == " ":
		taxa_lineages_table = get_taxa_lineages(taxa_table)
	else:
		taxa_lineages_table = process_lineages(args.lineages_file, taxa_table)


	####### 

	# Merge of the taxa dataframe (name of the contig and lineage ) with the 
	# fasta info dataframe (name of the contig, sequence, length, coverage (if given), GC %)
	# by NAME, so if the names doesn’t coincide the script will die. 

	#######


	final_table = fasta_table.merge(taxa_lineages_table, how='inner', on="NAME")
	final_table.to_csv(args.output, index=False, header=True)
	
if __name__ == "__main__":
    main()