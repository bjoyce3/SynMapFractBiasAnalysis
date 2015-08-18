'''Imports'''


#For importing data and parsing data
from operator import itemgetter

#For output to csv
import csv
from itertools import islice, izip

#For analyzing data


"""Methods and variables"""


#For importing data and parsing
synmap_import_file = '/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/SynMapKsMerge120Sdepth10_Osativa2-Acomosus1.txt'
gff_import_file = '/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/Ananasgff.gff'

#For out to csv


#For analyzing data



"""Importing
Reads SynMap and GFF CDS files and parse data into columns in array
"""


d = {}  # initialize dictionary to contain the array of syntenic genome1_chrs, genome1_genes, genome2_chrs, and genome2_genes

with open(synmap_import_file, 'r') as f:  # open SynMap file containing syntenic genes
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

with open(gff_import_file, 'r') as g:  # opens gff file
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


"""Output """

with open("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/ALL_output_gff.txt", 'w+') as j:
	j.write(str(gff_genes))

'''Need to sort genes within chr by start position'''

for chr in gff_genes:
    gff_genes_sorted = sorted(gff_genes[chr], key=itemgetter('start'))  #Creates dictionary for searching genes against::CONSIDER sorting on midpoint of genes rather than
    gff_genes[chr] = gff_genes_sorted
    #CONSIDER WRITING A CHECK PROGRAM TO RETURN TRUE IF ALL VALUES ARE SORTED OR FALSE

'''Writes out sorted GFF gene list to document'''
with open("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/ALL_sorted_output_gff.txt", 'w') as h:
	h.write(str(gff_genes))
with open("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/ALL_dictionary_syntenic genes", 'w+') as i:
    i.write(str(d))




'''Output CSV file for data recording and downstream analysis CONSIDER ELIMINATING ANYTHING WITH MORE THAN 2 GENE MATCHES'''


P_chr1_sub1 = []
P_chr1_sub2 = []
P_chr1_sub3 = []
P_chr1_sub4 = []
P_chr1_sub5 = []
P_chr1_sub6 = []
P_chr1_sub7 = []
P_chr1_sub8 = []
P_chr1_sub9 = []
P_chr1_sub10 = []


'''sub_2 = []
sub_3 = []
sub_4 = []
sub_5 = []
sub_6 = []
sub_7 = []
sub_8 = []
sub_9 = []
sub_10 = []'''



with open("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/ALL_fractbias_output.csv", 'w') as csvfile:
    headers = ['Pineapple Chromosome', 'Pineapple Gene Name', 'Pineapple Gene Order', 'Rice Chr 1', 'Rice Chr 2',
               'Rice Chr 3', 'Rice Chr 4', 'Rice Chr 5', 'Rice Chr 6', 'Rice Chr 7', 'Rice Chr 8', 'Rice Chr 9',
               'Rice Chr 10', 'Rice Subgenome 1 gene name', 'Rice Subgenome 2 gene name', 'Rice Subgenome 3 gene name',
               'Rice Subgenome 4 gene name', 'Rice Subgenome 5 gene name', 'Rice Subgenome 6 gene name', 'Rice Subgenome 7 gene name',
               'Rice Subgenome 8 gene name', 'Rice Subgenome 9 gene name', 'Rice Subgenome 10 gene name']
    writer = csv.writer(csvfile, dialect='excel', delimiter=',', lineterminator='\n')
    writer.writerow(headers)

    for chr in gff_genes:
        col0 = chr #writes Pineapple chr number
        count = 0
        for diction in gff_genes[chr]:
            gene = diction['gene_name']
            col1 = gene #writes pineapple gene name
            count += 1
            col2 = count #writes pineapple gene number on pineapple chr
            #Find the Rice Chr 1 genes
            try:
                rice_gene1 = d[chr][gene]['Chr1']
                col3 = True
                col13 = rice_gene1
            except KeyError:
                col3 = False
                col13 = '.'
            try:
                rice_gene2 = d[chr][gene]['Chr2']
                col4 = True
                col14 = rice_gene2
            except KeyError:
                col4 = False
                col14 = '.'
            try:
                rice_gene3 = d[chr][gene]['Chr3']
                col5 = True
                col15 = rice_gene3
            except KeyError:
                col5 = False
                col15 = '.'
            try:
                rice_gene4 = d[chr][gene]['Chr4']
                col6 = True
                col16 = rice_gene4
            except KeyError:
                col6 = False
                col16 = '.'
            try:
                rice_gene5 = d[chr][gene]['Chr5']
                col7 = True
                col17 = rice_gene5
            except KeyError:
                col7 = False
                col17 = '.'
            #Finds the Rice subgenome 2 genes
            try:
                rice_gene6 = d[chr][gene]['Chr6']
                col8 = True
                col18 = rice_gene6
            except KeyError:
                col8 = False
                col18 = '.'
            try:
                rice_gene7 = d[chr][gene]['Chr7']
                col9 = True
                col19 = rice_gene7
            except KeyError:
                col9 = False
                col19 = '.'
            try:
                rice_gene8 = d[chr][gene]['Chr8']
                col10 = True
                col20 = rice_gene8
            except KeyError:
                col10 = False
                col20 = '.'
            try:
                rice_gene9 = d[chr][gene]['Chr9']
                col11 = True
                col21 = rice_gene9
            except KeyError:
                col11 = False
                col21 = '.'
            try:
                rice_gene10 = d[chr][gene]['Chr10']
                col12 = True
                col22 = rice_gene10
            except KeyError:
                col12 = False
                col22 = '.'

            rows = col0, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20, col21, col22 + '\n'
            writer.writerow(rows)

            if col0 == 1:
                #Writes to pineapple chr 1 file - needs all ten rice chr
                P_chr1_sub1.append(col3)
                P_chr1_sub2.append(col4)
                P_chr1_sub3.append(col5)
                P_chr1_sub4.append(col6)
                P_chr1_sub5.append(col7)
                P_chr1_sub6.append(col8)
                P_chr1_sub7.append(col9)
                P_chr1_sub8.append(col10)
                P_chr1_sub9.append(col11)
                P_chr1_sub10.append(col12)

print P_chr1_sub1
print len(P_chr1_sub2)
print len(P_chr1_sub3)
print len(P_chr1_sub4)
print len(P_chr1_sub5)
print len(P_chr1_sub6)
print len(P_chr1_sub7)
print len(P_chr1_sub8)
print len(P_chr1_sub9)
print len(P_chr1_sub10)

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
raw_outcol4 = []
raw_outcol5 = []
raw_outcol6 = []
raw_outcol7 = []
raw_outcol8 = []
raw_outcol9 = []
raw_outcol10 = []

with open("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/All_raw_xy_PA1_ALLRice.csv", 'w') as csvf:
    headers = ['Iteration (x)', 'Rice Chr 1 % Presence', 'Rice Chr 2 % Presence', 'Rice Chr 3 % Presence',
               'Rice Chr 4 % Presence', 'Rice Chr 5 % Presence', 'Rice Chr 6 % Presence', 'Rice Chr 7 % Presence',
               'Rice Chr 8 % Presence', 'Rice Chr 9 % Presence', 'Rice Chr 10 % Presence']
    writer = csv.writer(csvf, dialect='excel', delimiter=',', lineterminator='\n')
    writer.writerow(headers)
    counter = 0
    for each in window(P_chr1_sub1, 100):
        counter += 1
        raw_outcol0.append(counter)
        col1 = sum(each)
        raw_outcol1.append(col1)
    for each in window(P_chr1_sub2, 100):
        col2 = sum(each)
        raw_outcol2.append(col2)
    for each in window(P_chr1_sub3, 100):
        col3 = sum(each)
        raw_outcol3.append(col3)
    for each in window(P_chr1_sub4, 100):
        col4 = sum(each)
        raw_outcol4.append(col4)
    for each in window(P_chr1_sub5, 100):
        col5 = sum(each)
        raw_outcol5.append(col5)
    for each in window(P_chr1_sub6, 100):
        col6 = sum(each)
        raw_outcol6.append(col6)
    for each in window(P_chr1_sub7, 100):
        col7 = sum(each)
        raw_outcol7.append(col7)
    for each in window(P_chr1_sub8, 100):
        col8 = sum(each)
        raw_outcol8.append(col8)
    for each in window(P_chr1_sub9, 100):
        col9 = sum(each)
        raw_outcol9.append(col9)
    for each in window(P_chr1_sub10, 100):
        col10 = sum(each)
        raw_outcol10.append(col10)
    writer.writerows(izip(raw_outcol0, raw_outcol1, raw_outcol2, raw_outcol3, raw_outcol4, raw_outcol5,
                          raw_outcol6, raw_outcol7, raw_outcol8, raw_outcol9, raw_outcol10))

