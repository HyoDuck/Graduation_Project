import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter
import xlrd
sns.set(style="white")
plt.rcParams["font.family"] = 'HYSinMyeongJo-Medium'
plt.rcParams["font.size"] = 12

data = pd.read_excel('C:/Users/user/Desktop/15x15.xlsx')
mask = np.zeros_like(data, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True


print(data)

from scipy.cluster.hierarchy import linkage

labels = data.index
row_clusters = linkage(data, method='complete')
row_clusters=pd.DataFrame(row_clusters,columns=['클러스터ID_1','클러스터ID_2', '거리', '클러스터 멤버수'],index=['클러스터 %d' %(i+1) for i in range(row_clusters.shape[0])])
print(row_clusters)
from scipy.cluster.hierarchy import dendrogram
row_dendr = dendrogram(row_clusters, labels = labels)


plt.tight_layout()
plt.ylabel('유클리드 거리')
plt.show()
