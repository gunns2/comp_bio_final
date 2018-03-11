from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
from itertools import cycle
import pandas as pd



dataframe = pd.read_csv('dataframe.csv')
X = dataframe.iloc[:,3:]
# Setup Affinity Propagation

print(dataframe.head())
print(X.head())
X = dataframe.iloc[:,3:].values

af = AffinityPropagation(preference = -10, verbose=False).fit(X)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

no_clusters = len(cluster_centers_indices)

print('Estimated number of clusters: %d' % no_clusters)



# colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
# for k, col in zip(range(no_clusters), colors):
#     class_members = labels == k
#     cluster_center = X[cluster_centers_indices[k]]
#     plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
#     plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)
#     for x in X[class_members]:
#         plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

# plt.show()x