import pandas as pd
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import linkage
import os

def clustering(excel, y):
    data = 1 - abs(round(pd.read_excel(excel), 4))
    row_clusters = linkage(data, method='complete')

    predict = pd.DataFrame(fcluster(row_clusters, y, criterion='distance'), data.index)
    predict.columns = ['predict']
    cluster = predict['predict'].values.tolist()
    max_num = max(cluster)
    mat = []
    for i in range(max_num):
        mat.append(predict.index[predict['predict'] == i + 1].tolist())
    return mat

if __name__ == '__main__':
    input_list = clustering(excel='C:/data/30x30.xlsx', y=1.5)
