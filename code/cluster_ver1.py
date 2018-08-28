import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter
import xlrd


def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata

sns.set(style="white")
plt.rcParams["font.family"] = 'HYSinMyeongJo-Medium'
plt.rcParams["font.size"] = 12

data = pd.read_excel('C:/Users/kwctl/Desktop/100.xlsx')
mask = np.zeros_like(data, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True


print(data)

from scipy.cluster.hierarchy import linkage

labels = data.index
row_clusters = linkage(data, method='complete')
print(row_clusters)
row_clusters=pd.DataFrame(row_clusters,columns=['클러스터ID_1','클러스터ID_2', '거리', '클러스터 멤버수'],index=['클러스터 %d' %(i+1) for i in range(row_clusters.shape[0])])
print(row_clusters)
from scipy.cluster.hierarchy import dendrogram
fancy_dendrogram(row_cluster, max_d=3)


plt.tight_layout()
plt.ylabel('유클리드 거리')
plt.show()


from sklearn.cluster import AgglomerativeClustering

ac = AgglomerativeClustering(n_clusters=2
                             , affinity='euclidean', linkage='complete')
labels = ac.fit_predict(data)
print('클러스터 분류 결과:', labels)
print(data.index)







