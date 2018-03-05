import seaborn
import matplotlib.pyplot as plt
import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set()
uniform_data = np.random.rand(10, 10)
ax = sns.heatmap(uniform_data)

plt.show()