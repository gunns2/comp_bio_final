#Michael Hoffert and Sophie Gunn
import os
from create_df import *

def read_cluster_csv(csv):
	csv = open(csv)
	rtd = {}
	for line in [i.split(',') for i in csv.readlines()][1:]:
		rtd[int(line[0])] = int(line[1].strip('\n'))

	return rtd


def write_cluster_fastas(csv, all_fasta):
	cluster_dict = read_cluster_csv(csv)
	seqs = read_fasta(all_fasta)
	fastas = []
	command = os.popen('mkdir cluster_fastas')
	for i in range(len(set(cluster_dict.values()))):
		fastas.append(open('cluster_' + str(i) + '_out.fa','w'))
		
	
	for key in cluster_dict.keys():
		fastas[cluster_dict[key]].write(seqs[key + 1][0])
		fastas[cluster_dict[key]].write(seqs[key + 1][1] + '\n')
		
	cmd = os.popen('pwd')

	for i in range(len(set(cluster_dict.values()))):
		fastas[i].close()
	cmd = os.popen("mv ./*out.fa ./cluster_fastas")
	
def run_checkm(
		
		
	
	
	
	
if __name__ == '__main__':
	write_cluster_fastas('clusters.csv','MidCaymanRise_FS856_idba_assembly_fixed.fa')
	


#def script(