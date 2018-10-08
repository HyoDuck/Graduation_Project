import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter
import xlrd
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
        
sns.set(style="white")
plt.rcParams["font.family"] = 'HYSinMyeongJo-Medium'
plt.rcParams["font.size"] = 12

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

def clustering():
    predict = pd.DataFrame(fcluster(row_clusters,1.5,criterion='distance'),data.index)
    predict.columns=['predict']
    cluster=predict['predict'].values.tolist()
    n_cluster=max(cluster)
    
    for i in range(n_cluster):
        print('Cluster %i: %s' % ((i+1), ','.join(predict.index[predict['predict']==i+1].tolist())))
	
    return predict




if __name__ == '__main__':
    data = 1-abs(round(pd.read_excel('C:/Users/user/Desktop/150x150.xlsx'),4))
    labels = data.index
    row_clusters = linkage(data, method='complete')
    row_clusters = pd.DataFrame(row_clusters,columns=['클러스터ID_1','클러스터ID_2', '거리', '클러스터 멤버수'],index=['클러스터 %d' %(i+1) for i in range(row_clusters.shape[0])])
    fancy_dendrogram(row_clusters, labels = labels, max_d=1.5)
    clustering()
    plt.tight_layout()
    plt.ylabel('height')
    plt.show()
