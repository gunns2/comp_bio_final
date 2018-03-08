from itertools import cycle
import numpy as  np
import pandas as pd
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
from itertools import cycle

def read_coverage_file(filename):
	d = pd.read_csv(filename, delimiter="\t", header = None, names = ['name', 'depth', 'n', 'size', 'percent'])
	return d

def get_cov_per_contig(cov_mat):
	cov_mat['count'] = cov_mat['depth']*cov_mat['n'] #depth * number of columns with said depth 
	cov_count = cov_mat.groupby(['name','size'], as_index = False).sum() #group by contig & size to preserve size
	cov_count['cov'] = cov_count['count']/cov_count['n']
	#print(cov_mat.head())
	#print(cov_count.head())
	#print(cov_count.columns.values.tolist())
	cov_small = cov_count.loc[:,['name','cov']] #we only need contig number and coverage now
	#print(cov_small.head())
	#print(cov_small.dtypes)
	#cov_small['cov'].plot.hist( bins=100)
	cov_small['cov'] = cov_small['cov'].astype(float)
	#print(cov_small.dtypes)
	cov_small['log_cov'] = np.log(cov_small['cov'])
	#print(cov_small.head())
	#cov_small['log_cov'].plot.hist( bins=100) #looks way better
	#plt.show()
	return cov_small


if __name__ == '__main__':
	cov_mat = read_coverage_file('FS849_coverage.txt')
	cov_vals = get_cov_per_contig(cov_mat)
	#print(cov_vals)
	
	X = cov_vals.iloc[:, 2].values
	X = X.reshape(-1,1)


	af = AffinityPropagation(preference = -17, verbose=False).fit(X.reshape(-1, 1) )
	cluster_centers_indices = af.cluster_centers_indices_
	labels = af.labels_

	cov_vals['log_cov'].plot.hist( bins=100) #looks way better
	

	for i in range(len(cluster_centers_indices)):
		cluster_center = X[cluster_centers_indices[i]]
		plt.axvline(cluster_center, color='b', linestyle='dashed', linewidth=2)
		#print('cluster center', cluster_center)

	no_clusters = len(cluster_centers_indices)
	print('Estimated number of clusters: %d' % no_clusters)

	#plt.show()
	plt.savefig('preference-17.png', bbox_inches='tight')





