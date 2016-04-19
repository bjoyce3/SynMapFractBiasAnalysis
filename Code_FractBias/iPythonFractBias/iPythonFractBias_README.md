#Using the iPythonFractBias Code

##Installing iPython notebooks
1. Navigate to the Jupyter Notebooks website (http://jupyter.readthedocs.org/en/latest/install.html)
2. Follow the directions outlined for downloading and installation of Python 2.7

##Opening the iPython notebook file
1. Open a terminal (Mac) or open the CMD prompt (Windows)
2. Type ipython notebook
3. This will open a browser
4. Navigate to and open the iPythonFractBias.ipynb file

##Setting the variables
1. Download the necessary data files from CoGe (https://genomevolution.org/coge/SynMap.pl)
  1. Run a SynMap comparison with the Syntenic Depth option (under Analysis Options) set
  2. At the bottom of the SynMap figure, click the click here to see more... link next to "Links and Downloads"
  3. In the Results section, select "DAGCHAINER output in genomic coordinates"
  4. Select all and copy the data into a tab separated value (.tsv) file
  5. Download the GFF file for the target genome
    * Select the genome with the lower syntenic depth (a.k.a. the target genome) and bring up the GenomeInfo page
    * Under the Tools section in GenomeInfo, select Download: GFF to move the file to your local computer
2. Setting the variables for analysis
  1. Under Methods and Global Variables, set the paths to downloaded data
    * synmap_import_file = include the path to the SynMap DAGCHAINER output file saved previously
    * gff_target_import_file = include the path to the target genome GFF
  2. Under User Settings, include all of the user set arguments
    * args_target = Set the genomeID of the genome with the lower syntenic depth
    * args_query = Set the genomeID of the genome with the higher syntenic depth
    * args_all_genes = Set to either True or False (Boolean variable), if True then all genes are used, if False then only sytenic genes are used
    * window_size = Set to the number of genes to use in each sliding window
    * args_numtargetchr = Set to the number of target genome chromosomes to use in the analysis
    * args_numquerychr = Set to the number of query genome chromosomes to use in the analysis
    * args_remove_random_unknown = Set to either True or False (Boolean variable), if True then any chromosomes with random or unknown in their names will be removed from consideration
  3. Set paths for each of the output files in the Methods and Global Variables section
3. Run all cells and await figure output at the bottom cell
