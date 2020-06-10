# Script to generate a .labels file from a kraken output

This script generates a .labels files from a .kraken standard file, obtained through Kraken. 

Before running the script please make sure that you have Python 3.0 or above (https://www.python.org) and the ETE Toolkit libraries (http://etetoolkit.org). 

To run the script please use the following instruction:

`python labels.py $KRAKEN_FILE`

If the file "taxdump.tar.gz" is not in the same directory as the labels.py file, or if it is the first time you use the script, the script will attempt to download it. Once it is downloaded, please leave it in the same directory as the labels.py file, so you don't have to download it again. 

The script will generate a file called "output.labels" as an output. 
