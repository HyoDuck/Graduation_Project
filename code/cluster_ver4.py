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


def clustering(excel,y):
    data = 1-abs(round(pd.read_excel(excel),4))
    row_clusters = linkage(data, method='complete')
    labels = data.index
    predict = pd.DataFrame(fcluster(row_clusters,y,criterion='distance'),data.index)
    predict.columns=['predict']
    cluster=predict['predict'].values.tolist()
    max_num=max(cluster)
    mat = []
    for i in range(max_num):
        mat.append(predict.index[predict['predict']==i+1].tolist())
    return mat




