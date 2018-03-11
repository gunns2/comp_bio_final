#Michael Hoffert and Sophie Gunn


from itertools import cycle
import numpy as  np
import pandas as pd
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
from create_df import *
import time

def cluster(dataframe):
	start = time.time()
	
	
	
	preferences = [0] * 6260
	#X = dataframe.iloc[:,4:262].values
	#X = X.reshape(-1,1)
	#print('THIS IS X',X)
	
	
	for i in range(100):
		X = dataframe.iloc[:,(i+6):(i+8)].values
		
		af = AffinityPropagation(preference = preferences, verbose=True).fit(X)
		cluster_centers_indices = af.cluster_centers_indices_
		labels = af.labels_

		for i in cluster_centers_indices:
			preferences[i] += 1
	
		no_clusters = len(cluster_centers_indices)

		print('Estimated number of clusters: %d' % no_clusters)
		print('Finished in: ',time.time() -start)
		print(preferences)
	# Plot exemplars
	plt.close('all')
	plt.figure(1)
	plt.clf()

	colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
	for k, col in zip(range(no_clusters), colors):
		class_members = labels == k
		cluster_center = X[cluster_centers_indices[k]]
		plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
		plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)
		for x in X[class_members]:
			plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

	plt.show()
	#dataframe['log_cov'].plot.hist( bins=100) #looks way better than non logged
	

	# for i in range(len(cluster_centers_indices)):
# 		cluster_center = X[cluster_centers_indices[i]]
# 		plt.axvline(cluster_center, color='b', linestyle='dashed', linewidth=2)
# 		#print('cluster center', cluster_center)
# 
# 	no_clusters = len(cluster_centers_indices)
# 	print('Estimated number of clusters: %d' % no_clusters)
# 
# 	#plt.show()
# 	plt.savefig('preferenceNoneFS877_covlog.png', bbox_inches='tight')
	
	
	
if __name__ == '__main__':
	# cov_mat = read_coverage_file('E23_FS877_coverage.txt')
# 	cov_vals = get_cov_per_contig(cov_mat)
# 	print(cov_vals.head())
# 	print('done with coverage, moving on to gene file')
# 
# 	gene = read_fasta('MidCaymanRise_FS877_idba_assembly_fixed.fa')
# 	row_dict = row_dict()
# 	df_wo_cov = create_data_frame(gene, row_dict)	
# 	print(df_wo_cov.head())
# 
# 	together = cov_vals.merge(df_wo_cov, left_on='name', right_on='name', how='outer')
# 	print(together.head())
# 	together.to_csv('dataframe.csv')
	
	print('RUNNING CLUSTER')
	cluster(make_data_frame_from_csv('dataframe.csv'))
	
	
	
	
	
	
	
	