#!/usr/bin/env python3

import argparse, os               
import pandas as pd  

def only_files(path):

	#### returns only the files in a directory, not subdirectories ####

	#Input: the path of the input directory
	#Output: yields only filenames

	for file in os.listdir(path):
		if os.path.isfile(os.path.join(path,file)):
			yield file

def get_lineages(otus):

	#### makes the lineage file (lineages.tsv). Requires ete3 ####

	#Input: list of the otus in the table obtained from the get_otus function
	#Output: makes the lineages.tsv file 

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
		lineage = ncbi.get_lineage(entrie)                  #returns list of lineage taxids
		names = ncbi.get_taxid_translator(lineage).values() #returns dict in which the taxids of the lineage list become the keys (int) and the translations the values. Error if there is a 0 
		all_names = ";".join(names)
		lineages.update({entrie: all_names})

	lineages_df = pd.DataFrame(lineages.items(), columns=["OTU", "lineage"])
	lineages_df.to_csv("lineages.tsv", sep="\t", index=False, header=True)
	print("lineage file created")

def get_otus(input_dir,list_files):

	#### process the files, gets how many reads/contigs are in every file, and makes a table with that info ####

	#Input: the input directory and the list of files to process
	#Output: returns a table with every taxid on all of the processed files as keys and the number of 
	#repeats of each taxid per file as columns

	count = 0

	for file in list_files:
		
		full_filepath = input_dir + file
		filename = file.split(".")[0]

		print("processing file {}".format(full_filepath))

		with open(full_filepath) as f:
			first_char = f.readline()[0]
			if first_char == "C" or first_char == "U":        #This part recognizes kaiju, kraken, and kraken2 output 
				taxids = pd.read_csv(full_filepath, sep= "\t", usecols=[2], names=[filename])
				taxids_counts = taxids[filename].value_counts().to_frame()
			else:
				taxids = pd.read_csv(full_filepath, sep= "\t", usecols=[1], names=[filename])
				taxids_counts = taxids[filename].value_counts().to_frame()

		if count == 0:
			merged_table = taxids_counts
			count = 1
		else:
			merged_table = pd.merge(taxids_counts, merged_table, how="outer", left_index=True, right_index=True)

	return(merged_table)

def main():


	####### Arguments ####### 

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_dir", default="./", 
		help="Directory from which classified reads are taken. Supported formats: Kraken2 output and Kaiju output")
	parser.add_argument("-o", "--output", default= "output.tsv", 
		help="ouput filename. Default is output.tsv")
	parser.add_argument("-u", "--unclassified", default="yes", choices=["yes", "no"], 
		help="Includes unclassified reads/contigs. Default is yes")
	parser.add_argument("-e", "--extension", default="*", 
		help="Use files with the given extension only. If it is not specified, all files will be used")
	parser.add_argument("-l", "--lineage", choices=["yes", "no"], default = "no",
		help="Generates an additional file (lineages.tsv) with the taxids lineages. Requires the ete3 library")
	args = parser.parse_args()

	####### Arguments #######


	try:

		## Gets the files with the selected extension ##

		if args.extension == "*":
			list_files = [x for x in only_files(args.input_dir)]
		else:
			list_files = [x for x in only_files(args.input_dir) if x.endswith(args.extension)]	
	except:
		raise Exception("Couldn't find the files. Please check the directory path and the extension")

	## Makes the table ##

	merged_table = get_otus(args.input_dir,list_files)
	merged_table = merged_table.rename_axis(index="OTU")

	## If you don't want to have unclassified reads in the table, this thing just drops that row from the table ###

	if args.unclassified == "no":
		merged_table.drop(0, inplace=True) 

	## Changes the N/A in the table for zeroes ##

	merged_table = merged_table.fillna(0.0).astype(int)

	## Makes the file for the table ##

	merged_table.to_csv(args.output, sep="\t", header=True)
	print("summary table created")

	## If you want a file with the full lineages this thing will make it ##

	if args.lineage == "yes":
		list_of_otus = merged_table.index.tolist()
		otu_lineages = get_lineages(list_of_otus)

if __name__ == "__main__":
    main()