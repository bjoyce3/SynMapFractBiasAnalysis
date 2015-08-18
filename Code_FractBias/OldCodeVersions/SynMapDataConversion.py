'''Imports'''

from operator import itemgetter
import csv
from itertools import islice, izip

"""Read SynMap output file and parse data into columns in array"""

d = {}  # initialize dictionary to contain the array of syntenic genome1_chrs, genome1_genes, genome2_chrs, and genome2_genes

with open('/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/RiceChr2and6.txt', 'r') as f:  # open SynMap file containing syntenic genes
    cols = []  # list for parsing columns from SynMap data
    for line in f:  # for loop to parse columns
        new_line = line.replace('||', '\t')  #converts || into tabs for universal delimination
        if line[0] != '#' and line[0] != '\n':  #sorts out columns containing syntenic block information/headings
            cols = new_line.split('\t', )  #splits all syntenic gene pair lines into parsed columns in a list
            #print cols
            global pa_chr
            global pa_gene
            global rice_chr
            global rice_gene
            pa_chr = str(cols[15])  #puts all genome1_chrs into a list
            if pa_chr.startswith('LG'):
                #Removes the name specific to Pineapple chromosomes DOUBLE CHECK LATER
                pa_chr = int(pa_chr[2:4])
            pa_gene = str(cols[18])  #puts all genome1_genes with synteny into a list
            rice_chr = str(cols[3])  #puts all genome2_chrs with synteny to genes in genome1 into a list
            rice_gene = str(cols[6])  #puts all genome2_genes with synteny to genes in a genome1 into a list

            if not pa_chr in d:
                d[pa_chr] = {}  #initializes the nested dictionary-primary level at genome1_chromosome
            if not pa_gene in d[pa_chr]:
                d[pa_chr][pa_gene] = {}  #initializes first nesting in dictionary-second level at genome1_genes
            if not rice_chr in d[pa_chr][pa_gene]:
                d[pa_chr][pa_gene][rice_chr] = rice_gene  #initializes nested dictionary-third level at genome2_chr
#            if not rice_gene in d[pa_chr][pa_gene][rice_chr]:
#                d[pa_chr][pa_gene][rice_chr][rice_gene] = 1  #initializes nested dictionary-fourth level at genome2_genes

'''Reads gff from genome1 and orders genes into chromosomes of gff'''

gff_genes = {}  # initializes dictionary for organization of genes on chromosomes within genome1 according to start bp

with open('/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/Ananasgff.gff', 'r') as g:  # opens gff file
    gffcols = []  #list of parsed gff columns
    chr = []  #initialize list of chromosomes present in genome1 gff file
    for line in g:
        new_line = line.replace(';', '\t')  #makes subdelims universal in gff file from CoGe
        new_line = new_line.replace('Name=', '')  #strips Name= off gene_name in gff file from CoGe
        new_line = new_line.replace('LG', '')

        if new_line[0] != '#' and new_line[0] != '\n':  #selects only lines with CDS information
            gffcols = new_line.split('\t', )  #parses all columns
            if gffcols[2] == 'mRNA' and 'scaffold' not in gffcols[0]:  #selects only 'mRNA' lines for consideration
                chr = int(gffcols[0])  #adds genome1_chrs to list
                gene_name = gffcols[10]  #adds genome1_genes to list
                start = int(gffcols[3])  #adds genome1_gene start bp to list for ordering as integer
                stop = int(gffcols[4])  #adds genome1_gene stop bp to list ?for ordering? as integer
                if not chr in gff_genes:
                    gff_genes[chr] = []  #initializes chr list in dictionary if chr doesnot exist yet
                gff_genes[chr].append(dict(gene_name=gene_name, start=start, stop=stop))


with open("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/output_gff.txt", 'w+') as j:
	j.write(str(gff_genes))

'''Need to sort genes within chr by start position'''

for chr in gff_genes:
    gff_genes_sorted = sorted(gff_genes[chr], key=itemgetter('start'))  #Creates dictionary for searching genes against::CONSIDER sorting on midpoint of genes rather than
    gff_genes[chr] = gff_genes_sorted
    #CONSIDER WRITING A CHECK PROGRAM TO RETURN TRUE IF ALL VALUES ARE SORTED OR FALSE

'''Writes out sorted GFF gene list to document'''
with open("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/sorted_output_gff.txt", 'w') as h:
	h.write(str(gff_genes))
with open("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/dictionary_syntenic genes", 'w+') as i:
    i.write(str(d))




'''Output CSV file for data recording and downstream analysis CONSIDER ELIMINATING ANYTHING WITH MORE THAN 2 GENE MATCHES'''

subgenome_1 = []
subgenome_2 = []
both_subgenome = []

with open("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/fractbias_output.csv", 'w') as csvfile:
    headers = ['Pineapple Chromosome', 'Pineapple Gene Name', 'Pineapple Gene Order', 'Rice Subgenome 1', 'Rice Subgenome 2', 'Both Subgenomes', 'Rice Subgenome 1 gene name', 'Rice Subgenome 2 gene name']
    writer = csv.writer(csvfile, dialect='excel', delimiter=',', lineterminator='\n')
    writer.writerow(headers)

    for chr in gff_genes:
        col0 = chr
        count = 0
        for diction in gff_genes[chr]:
            gene = diction['gene_name']
            col1 = gene
            count += 1
            col2 = count
            #Find the Rice subgenome 1 genes
            try:
                rice_gene2 = d[chr][gene]['Chr2']
                col3 = True
                col5 = rice_gene2
            except KeyError:
                col3 = False
                col5 = '.'
            #Finds the Rice subgenome 2 genes
            try:
                rice_gene6 = d[chr][gene]['Chr6']
                col4 = True
                col6 = rice_gene6
            except KeyError:
                col4 = False
                col6 = '.'
            finally:
                if col3 == True and col4 == True:
                    col7 = True
                else:
                    col7 = False

            rows = col0, col1, col2, col3, col4, col7, col5, col6 + '\n'
            writer.writerow(rows)
            if col0 == 14:
                subgenome_1.append(col3)
                subgenome_2.append(col4)
                both_subgenome.append(col7)

print len(subgenome_1)
print len(subgenome_2)

'''Analysis: for each chromosome in genome1 read the genes on a chromosome and compare to subgenome array of syntenic genes'''


#http://stackoverflow.com/questions/6822725/rolling-or-sliding-window-iterator-in-python
def window(seq, n):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

raw_outcol0 = []
raw_outcol1 = []
raw_outcol2 = []
raw_outcol3 = []

with open("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/raw_xy_PA14_R2_6.csv", 'w') as csvf:
    headers = ['Iteration (x)', 'Subgenome 1 % Presence', 'Subgenome 2 % Presence', '% Present in Both']
    writer = csv.writer(csvf, dialect='excel', delimiter=',', lineterminator='\n')
    writer.writerow(headers)
    counter = 0
    for each in window(subgenome_1, 100):
        counter += 1
        raw_outcol0.append(counter)
        col1 = sum(each)
        raw_outcol1.append(col1)
    for each in window(subgenome_2, 100):
        col2 = sum(each)
        raw_outcol2.append(col2)
    for each in window(both_subgenome, 100):
        col3 = sum(each)
        raw_outcol3.append(col3)

    writer.writerows(izip(raw_outcol0, raw_outcol1, raw_outcol2, raw_outcol3))