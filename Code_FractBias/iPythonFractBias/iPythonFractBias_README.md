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
    *Select the genome with the lower syntenic depth (a.k.a. the target genome) and bring up the GenomeInfo page
    *Under the Tools section in GenomeInfo, select Download: GFF to move the file to your local computer
2. Setting the variables for analysis
