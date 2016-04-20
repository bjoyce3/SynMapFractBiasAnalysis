#SynMapFractBiasAnalysis
Fractionation bias analysis tool for investigating whole genome duplication gene loss. 

##Explanation of versions on GitHub repo
1. iPythonFractBias  
  A version of FractBias that can be used in an interactive iPython Jupyter Notebook (http://ipython.org/notebook.html).
2. CommandLineFractBias  
  The version of FractBias that includes arguements so that a web-based platform can pass variables to complete analysis. This version is installed on the CoGe (Comparative Genomics) platform here: https://genomevolution.org/CoGe/SynMap.pl . It can be run using the SynMap tool [1].

##Scientific Summary
Following polyploidy events, genomes undergo massive reduction in gene content through a process known as fractionation.  Importantly, the fractionation process is not random, and there is often a bias as to which homeologous chromosome retains or loses more genes.  The process of characterizing whole genome fractionation requires identifying syntenic regions across genomes followed by post-processing of those syntenic datasets to identify and plot gene retention patterns. We have developed a tool, FractBias, to calculate and visualize gene retention and fractionation patterns across whole genomes.  Through integration with SynMap and its parent platform CoGe, over 25,000 genomes are pre-loaded and available for analysis, as well as letting researchers integrate their own data with security options to keep them private or make them publicly available.

##Notes
1. Docuementation for using the web-based SynMap tool can be found here: https://genomevolution.org/wiki/index.php/SynMap
2. Documentation for using FractBias specifically can be found here: https://genomevolution.org/wiki/index.php/FractBias 
3. The SynMap Syntenic Depth option must be set for FractBias to work

##Publications
1. Lyons,E. et al. (2008) The value of nonmodel genomes and an example using SynMap within CoGe to dissect the hexaploidy that predates the ro-sids. Trop. Plant Biol., 1, 181–190
