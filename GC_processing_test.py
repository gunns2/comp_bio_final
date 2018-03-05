import multiprocessing
import time

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
			
			
			
		
if __name__ == '__main__':
	print('small test')
	test_GC('AD-155-C09-many_assemblers_simple.CISA.ctg.fa')
	test_GC('AD-155-C09-many_assemblers_simple.CISA.ctg.fa',True)
	print('large test')
	test_GC('MidCaymanRise_FS856_idba_assembly_fixed.fa')
	test_GC('MidCaymanRise_FS856_idba_assembly_fixed.fa',True)
	