import seaborn
import random
import matplotlib.pyplot as plt
import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set()
# uniform_data = np.random.rand(10, 10)
# 
# print(uniform_data)
# ax = sns.heatmap(uniform_data)
# 
# plt.show()

file = open('FS877_bin_collection.txt')
matrix_dict = {}
for item in [line.split() for line in file.readlines()]:
	matrix_dict[item[0]] = item[1]
print(matrix_dict)
output_list = []
lock = list(matrix_dict.keys())
length = len(matrix_dict.keys())
for i in range(length):
	output_list.append([])
	
	for j in range(length):
		output_list[i].append(0)

for item in range(length):
	for item2 in range(length):
		if matrix_dict[lock[item]] == matrix_dict[lock[item2]]:
			print(item, item2,matrix_dict[lock[item]],matrix_dict[lock[item2]])
			
			output_list[item][item2] = 1
			output_list[item2][item] = 1
			

# for item in output_list:
# 	print(item)
ax = sns.heatmap(output_list)

plt.show()
			
		

	
