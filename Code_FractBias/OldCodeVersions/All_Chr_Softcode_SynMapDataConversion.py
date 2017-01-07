"""Imports"""
#Notes for GitHub demo

#For importing data and parsing data
from operator import itemgetter
import pprint

#Converting parsed data into raw parsed data output to csv
import csv
from itertools import islice, izip

#For analyzing raw parsed data

#had to install this using pip on local computer
from natsort import natsorted, natsort_key



"""Methods and Global Variables"""


#For importing data and parsing
synmap_import_file = '/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/SynMapKsMerge120Sdepth10_Osativa2-Acomosus1.txt'
gff_import_file = '/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/Ananasgff.gff'
d = {}  # initialize dictionary to contain the array of syntenic genome1_chrs, genome1_genes, genome2_chrs, and genome2_genes
genus_species = ''
with open(gff_import_file) as gff_file:
    for line in gff_file:
        if line[0:15] == '##Organism name':
            genus_species = line[17:-1]
            species_name = genus_species.replace(' ','_')
            species_name_filter = species_name.translate(None, '(){}[]')

#Parsed data and raw output to csv
gff_sort_output_file = ("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/ALL_GFF_sorted_"+str(species_name_filter)+ ".txt")
synmap_dictionary_output_file = ("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/ALL_dictionary_syntenic genes_" +str(species_name_filter)+ ".txt")
gff_genes = {}  # initializes dictionary for organization of genes on chromosomes within genome1 according to start bp
fract_bias_raw_output_file = ("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/ALL_fractbias_" +str(species_name_filter)+ "output.csv")

#Analysis of parsed data
retention_calc_output_file = ("/Users/bjoyce3/Desktop/SynMapFractBiasAnalysis/Analysis_output/Window_output_"+str(species_name_filter))
target_lst = []
query_lst = []

def chr_id(input_dict):
    for item in input_dict:
        if not item in target_lst:
            target_lst.append(item)
        for gene in input_dict[item]:
            for chr in input_dict[item][gene]:
                if not chr in query_lst:
                    query_lst.append(chr)

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


"""Importing
Reads SynMap and GFF CDS files and parse data into columns in array
"""


with open(synmap_import_file, 'r') as f:  # open SynMap file containing syntenic genes
    cols = []  # list for parsing columns from SynMap data
    for line in f:  # for loop to parse columns
        new_line = line.replace('||', '\t')  #converts || into tabs for universal delimination
        if line[0] != '#' and line[0] != '\n':  #sorts out columns containing syntenic block information/headings
            cols = new_line.split('\t', )  #splits all syntenic gene pair lines into parsed columns in a list
            global target_chr
            global target_gene
            global query_chr
            global query_gene
            target_chr = cols[15]
            if target_chr.startswith('LG'):
                #Removes the name specific to Pineapple chromosomes DOUBLE CHECK LATER
                target_chr = int(target_chr[2:4])
            target_gene = str(cols[18])  #puts all genome1_genes with synteny into a list
            query_chr = str(cols[3])  #puts all genome2_chrs with synteny to genes in genome1 into a list
            query_gene = str(cols[6])  #puts all genome2_genes with synteny to genes in a genome1 into a list

            if not target_chr in d:
                d[target_chr] = {}  #initializes the nested dictionary-primary level at genome1_chromosome
            if not target_gene in d[target_chr]:
                d[target_chr][target_gene] = {}  #initializes first nesting in dictionary-second level at genome1_genes
            if not query_chr in d[target_chr][target_gene]:
                d[target_chr][target_gene][query_chr] = query_gene  #initializes nested dictionary-third level at genome2_chr

'''Reads GFF from genome1 (target) and parses data'''
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
                    gff_genes[chr] = []  #initializes chr list in dictionary if chr does not exist yet
                gff_genes[chr].append(dict(gene_name=gene_name, start=start, stop=stop))

'''Sorts GFF genes within chromosome by start position'''
for chr in gff_genes:
    gff_genes_sorted = sorted(gff_genes[chr], key=itemgetter('start'))  #Creates dictionary for searching genes against::CONSIDER sorting on midpoint of genes rather than
    gff_genes[chr] = gff_genes_sorted

    #CONSIDER WRITING A CHECK PROGRAM TO RETURN TRUE IF ALL VALUES ARE SORTED OR FALSE

'''Writes out SynMap dictionary and sorted GFF gene list to document for parsed output'''
with open(str(gff_sort_output_file), 'w') as h:
	h.write(str(gff_genes))
with open(synmap_dictionary_output_file, 'w+') as i:
    i.write(str(d))

'''Determine syntenic gene pairs present and output Raw Data CSV file from parsed data'''

chr_id(d)
target_lst = natsorted(target_lst)
query_lst = natsorted(query_lst)
windanalysis_input_dict = {}

with open(str(fract_bias_raw_output_file), 'w') as csvfile:
    headers = ['Target Chromosome', 'Target Gene Name', 'Gene Order on Target Chromosome']
    headers.extend(query_lst)
    headers.extend(query_lst)
    writer = csv.writer(csvfile, dialect='excel', delimiter=',', lineterminator='\n')
    writer.writerow(headers)

    for tchr in gff_genes:
        col0 = chr #writes Pineapple chr number
        count = 0
        for diction in gff_genes[tchr]:
            gene = diction['gene_name']
            col1 = gene #writes pineapple gene name
            count += 1
            col2 = count #writes pineapple gene number on pineapple chr
            #Find the query chr genes and output to columns: first gff info (col0-3), query chr (col 4-n), query chr-gene (col n+1-m)
            syntenic_query_gene_presence_data = []
            syntenic_query_gene_name = []
            for qchr in query_lst:
                if not tchr in windanalysis_input_dict:
                    windanalysis_input_dict[tchr] = {}  #initializes the nested dictionary-primary level at genome1_chromosome
                if not qchr in windanalysis_input_dict[tchr]:
                    windanalysis_input_dict[tchr][qchr] = []  #initializes first nesting in dictionary-second level at genome1_genes
                try:
                    syn_gene = d[tchr][gene][qchr]
                    syntenic_query_gene_presence_data.append(True)
                    syntenic_query_gene_name.append(syn_gene)
                    windanalysis_input_dict[tchr][qchr].append(True)
                except KeyError:
                    syntenic_query_gene_presence_data.append(False)
                    syntenic_query_gene_name.append(".")
                    windanalysis_input_dict[tchr][qchr].append(False)
            rows = [tchr, col1, col2]
            rows.extend(syntenic_query_gene_presence_data)
            rows.extend(syntenic_query_gene_name)
            writer.writerow(rows)


'''Analysis: for each chromosome in genome1 read the genes on a chromosome and compare to subgenome array of syntenic genes'''

'''for tchr in windanalysis_input_dict:
    for key in natsorted(windanalysis_input_dict[tchr].iterkeys()):
        print key
#pprint.pprint(windanalysis_input_dict)'''

data_output0 = []
data_output1 = []
data_output2 = []
output_dict = {}

for tchr in windanalysis_input_dict:
    with open(str(retention_calc_output_file) + str(tchr) + ".csv", 'wb') as csvf:
        headers = ['Target Chromosome', 'Window Iteration (x-axis)']
        headers.extend(query_lst)
        writer = csv.writer(csvf, dialect='excel', delimiter=',', lineterminator='\n')
        writer.writerow(headers)
        tchr_counter = tchr
        for qchr in windanalysis_input_dict[tchr]:
            if not tchr in output_dict:
                output_dict[tchr] = {}  #initializes the nested dictionary-primary level at genome1_chromosome
            if not qchr in output_dict[tchr]:
                output_dict[tchr][qchr] = []  #initializes first nesting in dictionary-second level at genome1_genes
                natsorted(output_dict)
            counter = 0
            if (len(windanalysis_input_dict[tchr][qchr])) >= 100:
                for each in window(windanalysis_input_dict[tchr][qchr], 100):
                    counter += 1
                    data_output0.append(tchr_counter)
                    data_output1.append(counter)
                    data_output2 = sum(each)
                    output_dict[tchr][qchr].append(data_output2)
                    #Prints into two columns
                    writer.writerows(izip(data_output0, data_output1, output_dict))

#pprint.pprint(output_dict)


#http://stackoverflow.com/questions/28015044/python-nested-list-in-dict-to-csv-files
import csv
import itertools

'''csv_dict = {'label1': ['val1', 'val2', 'val3'],
            'label2': ['otherval1', 'otherval2'],
            'label3': ['yetanotherval1']}
keys = output_dict.keys()
csvrows = itertools.izip_longest(*[output_dict[k] for k in keys], fillvalue='dummy')
pprint.pprint(csvrows)

with open('', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='\\', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(keys)
    for row in csvrows:
        csvwriter.writerow(row)'''

'''            for key in keys:
                w.writerow(chain([qchr], (output_dict[tchr].get(qchr, '') for item in lst)))
                '''




