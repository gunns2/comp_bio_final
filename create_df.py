import multiprocessing
import time
import numpy as  np
import pandas as pd
import math


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
	return sequences

def row_dict():
	row_dict = {}
	row_dict['name'] = 0
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
	length = len(string)
	row_dict['length'] = len(string)

	#print(length)
	for i in range(0,len(string) - 3):
		quad = string[i:i+4]
		row_dict[quad] += 1

	for quad in row_dict:
		if quad != 'name' and quad != 'GC_percent' and quad != 'length':
			row_dict[quad] = np.log(row_dict[quad]/length * 100 + 1e-7)

	#count GC
	AT,GC = 0,0
	for ch in string:
		if ch in ['G','C']:
			GC += 1	
	row_dict['GC_percent'] = GC/length
	return row_dict

def read_coverage_file(filename):
	d = pd.read_csv(filename, delimiter="\t", header = None, names = ['name', 'depth', 'n', 'size', 'percent'])
	return d

def get_cov_per_contig(cov_mat):
	cov_mat['count'] = cov_mat['depth']*cov_mat['n'] #depth * number of columns with said depth 
	cov_count = cov_mat.groupby(['name','size'], as_index = False).sum() #group by contig & size to preserve size
	cov_count['cov'] = cov_count['count']/cov_count['n']
	cov_small = cov_count.loc[:,['name','cov', 'n']] #we only need contig number and coverage now
	cov_small['cov'] = cov_small['cov'].astype(float)
	cov_small['log_cov'] = np.log(cov_small['cov'] + 1e-7)
	return cov_small
			
def create_data_frame(gene, row_dict):
	row_list = []
	for contig in gene[1:]:
		contig_dict = fill_row(row_dict.copy(), contig)
		row_list.append(contig_dict.copy())
	df = pd.DataFrame(row_list)
	return df			
		
def make_data_frame_from_csv(csv):
	return pd.read_csv('./' + csv)

if __name__ == '__main__':
	cov_mat = read_coverage_file('FS851_coverage.txt')
	cov_vals = get_cov_per_contig(cov_mat)
	print(cov_vals.head())
	print('done with coverage, moving on to gene file')

	gene = read_fasta('MidCaymanRise_FS851_idba_assembly_fixed.fa')
	row_dict = row_dict()
	df_wo_cov = create_data_frame(gene, row_dict)	
	print(df_wo_cov.head())

	together = cov_vals.merge(df_wo_cov, left_on='name', right_on='name', how='inner')
	print(together.head())
	together.to_csv('df_851.csv')

