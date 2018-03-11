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

def read_coverage_file(filename):
	d = pd.read_csv(filename, delimiter="\t", header = None, names = ['name', 'depth', 'n', 'size', 'percent'])
	return d

def get_cov_per_contig(cov_mat):
	cov_mat['count'] = cov_mat['depth']*cov_mat['n'] #depth * number of columns with said depth 
	cov_count = cov_mat.groupby(['name','size'], as_index = False).sum() #group by contig & size to preserve size
	cov_count['cov'] = cov_count['count']/cov_count['n']
	cov_small = cov_count.loc[:,['name','cov']] #we only need contig number and coverage now
	cov_small['cov'] = cov_small['cov'].astype(float)
	cov_small['log_cov'] = np.log(cov_small['cov'] + 1)

	return cov_small

			
def create_data_frame(gene, row_dict):
	row_list = []
	
	for contig in gene[1:]:
		contig_dict = fill_row(row_dict, contig)
		
		row_list.append(contig_dict.copy())
	df = pd.DataFrame(row_list)
	return df
			
		
def make_data_frame_from_csv(csv):
	return pd.read_csv('./' + csv)
		
if __name__ == '__main__':
	cov_mat = read_coverage_file('E23_FS877_coverage.txt')
	cov_vals = get_cov_per_contig(cov_mat)
	print(cov_vals.head())
	print('done with coverage, moving on to gene file')

	gene = read_fasta('MidCaymanRise_FS877_idba_assembly_fixed.fa')
	row_dict = row_dict()
	df_wo_cov = create_data_frame(gene, row_dict)	
	print(df_wo_cov.head())

	together = cov_vals.merge(df_wo_cov, left_on='name', right_on='name', how='outer')
	print(together.head())
	together.to_csv('dataframe.csv')
	










