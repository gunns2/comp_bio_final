from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import AffinityPropagation
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt
from itertools import cycle
import pandas as pd

print('########################')
print('Cluster by Coverage ')
print('######################## \n')

df = pd.read_csv('df.csv')
X = df.ix[:,['log_cov']].values
af = AffinityPropagation(preference = -10, max_iter = 4000, verbose=False, damping = 0.95, affinity = 'euclidean', convergence_iter = 400).fit(X)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_
df['cov_clusters'] = labels
n_iter = af.n_iter_
no_clusters = len(cluster_centers_indices)
print('Estimated number of clusters: %d' % no_clusters)
print('Number of iterations to converge: %d' % n_iter)

df.ix[:,['log_cov']].plot.hist( bins=100)
for i in range(len(cluster_centers_indices)):
		cluster_center = X[cluster_centers_indices[i]]
		plt.axvline(cluster_center, color='b', linestyle='dashed', linewidth=2)
plt.show()

print('########################')
print('Cluster by GC and tetra_nuc freq per cluster ')
print('######################## \n')

for cluster in df.cov_clusters.unique():
	print('cluster: ', cluster)
	df_sub = df.loc[df['cov_clusters'] == cluster]
	X = df_sub.ix[:,4:-1] #looking at only tetra_nuc and GC content
	# X = df_sub.ix[:,['GC_percent']]
	X = X.values
	print('length X: ', len(X))
	af = AffinityPropagation(preference = -500, max_iter = 4000, verbose=False, damping = 0.95, affinity = 'euclidean', convergence_iter = 600).fit(X)
	cluster_centers_indices = af.cluster_centers_indices_
	labels = af.labels_
	n_iter = af.n_iter_
	no_clusters = len(cluster_centers_indices)
	print('Estimated number of clusters: %d' % no_clusters)
	print('Number of iterations to converge: %d' % n_iter, '\n')






