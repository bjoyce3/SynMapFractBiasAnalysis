#Using the Command Line FractBias Code

##Download fractionation_bias.py script to a local directory
1. Download the git repo by bringing up a terminal (Mac) or CMD prompt (Windows)
2. Type command: git clone https://github.com/bjoyce3/SynMapFractBiasAnalysis.git

##Downloading the data
1. Download the necessary data files from CoGe (https://genomevolution.org/coge/SynMap.pl)
  1. Run a SynMap comparison with the Syntenic Depth option (under Analysis Options) set
    * Select two genomes to compare by typing the scientific name of the organism into the two search bars
    * Select the Analysis options tab
    * Select Quota Align on the drop down menu in the Syntenic Depth section
    * Input the syntenic depth ratio of the two genomes (e.g. 1 to 2 if one genome has experienced a whole genome duplication)
    * Run the SynMap comparison by pressing the Generate SynMap button
    * Detailed documentation on how to run SynMap can be found here: https://genomevolution.org/wiki/index.php/SynMap
  2. At the bottom of the SynMap figure, click the click here to see more... link next to "Links and Downloads"
  3. In the Results section, select "DAGCHAINER output in genomic coordinates"
  4. Select all and copy the data into a tab separated value (.tsv) file
  5. Download the GFF file for the target genome
    * Select the genome with the lower syntenic depth (a.k.a. the target genome) and bring up the GenomeInfo page
    * Under the Tools section in GenomeInfo, select Download: GFF to move the file to your local computer

##Running the Python 2.7 fractionation_bias.py script
1. Download and install Python 2.7 here: https://www.python.org/downloads/
2. After installation, open a terminal (Mac) or the CMD prompt (Windows)
3. Navigate to the CommandLineFractBias directory
4. Run the code
python fractionation_bias.py -align -gff -target -windowsize -query -output -allgenes -numtargetchr -numquerychr -remove_random_unknown -syndepth

##Explaination of fractionation_bias.py arguments in command
1. align = include the path to the SynMap DAGCHAINER output file saved previously as "path/to/SynMapoutput"
2. gff = include the path to the target genome GFF saved previously as "path/to/GFFfile"
3. target = Set the genomeID of the genome with the lower syntenic depth
4. window_size = Set to the number of genes to use in each sliding window input as an integer, e.g. 100
5. query = Set the genomeID of the genome with the higher syntenic depth
6. output = path to output folder for data files as "path/to/output"
7. all_genes = Set to either True or False (Boolean variable), if True then all genes are used, if False then only sytenic genes are used
8. numtargetchr = Set to the number of target genome chromosomes to use in the analysis as an integer, e.g. 20
9. numquerychr = Set to the number of query genome chromosomes to use in the analysis as an integer, e.g. 20
10. remove_random_unknown = Set to either True or False (Boolean variable), if True then any chromosomes with random or unknown in their names will be removed from consideration
