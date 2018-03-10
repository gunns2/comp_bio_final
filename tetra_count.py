import multiprocessing
import time
import numpy as  np
import pandas as pd

def read_fasta(filename):
	fasta = open(filename)
	lines = fasta.readlines()
	sequences = []
	seq = ['','']
	for i in range(0,len(lines)):
		
		if lines[i][0] == '>':
			sequences.append(seq)
			seq = ['','']
			seq[0] = lines[i]
		else:
			seq[1] += lines[i][:-1]
	sequences.append(seq)	
	fasta.close()
	#print(sequences)
	return sequences

def row_dict():
	row_dict = {}
	row_dict['name'] = ''
	row_dict['GC_percent'] = 0
	nuc_list = ['A', 'T', 'C', 'G']
	for nuc1 in nuc_list:
		for nuc2 in nuc_list:
			for nuc3 in nuc_list:
				for nuc4 in nuc_list:
					row_dict[nuc1 + nuc2 + nuc3 + nuc4] = 0
	return row_dict

def fill_row(row_dict, contig):
	row_dict['name'] = contig[0][1:-1]
	
	#count tetra
	string = contig[1]
	for i in range(0,len(string) - 3):
		quad = string[i:i+4]
		row_dict[quad] += 1

	#count GC
	AT,GC = 0,0
	length = len(string)
	for ch in string:
		if ch in ['G','C']:
			GC += 1	
	row_dict['GC_percent'] = GC/length
	return row_dict



def count_tetra(tetra_dict, list1):
	string = list1[1][1]
	for i in range(0,len(string) - 3):
		quad = string[i:i+4]
		tetra_dict[quad] += 1
	print(tetra_dict)

def count_GC(list1):
	AT,GC = 0,0
	length = len(list1[1])
	for ch in list1[1]:
		if ch in ['G','C']:
			GC += 1	
			
	return(GC/length)

def test_GC(fasta,processing=False):
	start = time.time()
	seqs = read_fasta(fasta)
	if processing:
		with multiprocessing.Pool() as pool:
			new_results = pool.map(count_GC, seqs[1:])
	else:
		new_results = []
		for item in seqs[1:]:
			new_results.append(count_GC(item))
	print('finished in',time.time() - start)
	return new_results
			
def create_data_frame(gene, row_dict):
	row_list = []
	print(len(row_list))
	for contig in gene[1:]:
		contig_dict = fill_row(row_dict, contig)
		row_list.append(contig_dict.copy())
	df = pd.DataFrame(row_list)
	df.to_csv('dataframe.csv')
	return df
			
		
if __name__ == '__main__':
	#print('small test')
	#test_GC('AD-155-C09-many_assemblers_simple.CISA.ctg.fa')
	#test_GC('AD-155-C09-many_assemblers_simple.CISA.ctg.fa',True)
	#print('large test')
	#test_GC('MidCaymanRise_FS856_idba_assembly_fixed.fa')
	#test_GC('MidCaymanRise_FS856_idba_assembly_fixed.fa',True)
	gene = read_fasta('MidCaymanRise_FS877_idba_assembly_fixed.fa')
	#print(gene)
	row_dict = row_dict()
	df = create_data_frame(gene, row_dict)
	










