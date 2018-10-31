import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter
import xlrd
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
import datetime

sns.set(style="white")
plt.rcParams["font.family"] = 'HYSinMyeongJo-Medium'
plt.rcParams["font.size"] = 12


# 일정기간동안의 주식종목의 상관관계 계수 구하는 함수
def corr(excel, start, end):
    df = pd.read_excel(excel)
    df = df[df.날짜 <= end]
    df = df[df.날짜 >= start]
    df.index = pd.RangeIndex(len(df.index))
    df = df.drop("날짜", 1)

    writer = ExcelWriter('all_price.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()

    corr = df.corr(method='pearson')
    writer = ExcelWriter('corr.xlsx')
    corr.to_excel(writer, 'Sheet1')
    writer.save()
    return corr


# 상관계수를 바탕으로 클러스터링하는 함수
def clustering(excel):
    data = 1 - abs(round(pd.read_excel(excel), 4))
    row_clusters = linkage(data, method='complete')
    labels = data.index
    predict = pd.DataFrame(fcluster(row_clusters, 1.5, criterion='distance'), data.index)
    predict.columns = ['predict']
    cluster = predict['predict'].values.tolist()
    max_num = max(cluster)
    mat = []
    for i in range(max_num):
        if len(predict.index[predict['predict'] == i + 1].tolist()) > 1:
            mat.append(predict.index[predict['predict'] == i + 1].tolist())
    return mat


# 시각화함수
def visualization(excel, start, end, mat):
    li = pd.read_excel('C:/data/리스트.xlsx')
    wd = pd.read_excel('C:/data/키워드.xlsx')
    li = li.fillna(0)
    wd = wd.fillna(0)
    list_length = len(li.index)
    mat = []
    me = []
    word_list = []
    for i in range(list_length):
        me = li.ix[i].tolist()
        while me.count(0) > 0:
            me.remove(0)
        mat.append(me)

    for l in range(list_length):
        list_stock = li.ix[l].tolist()
        list_stock.append("[")
        while list_stock.count(0) > 0:
            list_stock.remove(0)
        if l == 0:
            word_stock = wd.ix[0].tolist()
        else:
            word_stock = wd.ix[l * 2].tolist()

        while word_stock.count(0) > 0:
            word_stock.remove(0)
        word_stock.append("]")
        total = list_stock + word_stock
        word_list.append(total)

    df = pd.read_excel('C:/data/거래량.xlsx')
    df = df[df.날짜 <= '2018.09.01']
    df = df[df.날짜 >= '2018.01.01']
    date = df['날짜'].tolist()
    df.index = df['날짜']
    df = df.drop("날짜", 1)
    df = df.sort_index()
    df = df.apply(lambda x: x / x[0])
    length = len(mat)

    view = pd.DataFrame()
    word = pd.DataFrame()

    for j in range(length):
        empty = pd.DataFrame()
        word_len = len(mat[j])

        for k in range(word_len):
            if k == 0:
                word = df[mat[j][k]]
            else:
                word = word + df[mat[j][k]]
        word = word / word_len
        empty = pd.concat((empty, word), axis=1)
        hop = ",".join(word_list[j])
        empty.columns = [hop]
        view = pd.concat((view, empty), axis=1)
        empty['date'] = view.index
        empty['datetime'] = empty['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y.%m.%d'))
        empty.set_index(empty['datetime'], inplace=True)
        empty = empty.drop('datetime', 1)
        empty = empty.drop('date', 1)
        plt.plot(empty, label=mat)
        plt.legend(empty.columns, loc='upper left')
        plt.grid(True)
        plt.axhline(y=1, color="black", lw=2)
        plt.show()

    view['date'] = view.index
    view['datetime'] = view['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y.%m.%d'))
    view.set_index(view['datetime'], inplace=True)
    view = view.drop('datetime', 1)
    view = view.drop('date', 1)
    plt.plot(view, label=mat)
    plt.legend(view.columns, loc='upper left')
    plt.grid(True)
    plt.axhline(y=1, color="black", lw=2)
    plt.show()


def graph_test(start = '', end = '', all_stock_xlsx_path = '', cluster_xlsx_path = ''):
    #corr(all_stock_xlsx_path, start, end)
    mat = clustering(cluster_xlsx_path)
    visualization(start, end, mat, 'C:/data/all_stock.xlsx')

    for i in range(0, len(mat), 1):
        for j in range(0, len(mat[i]), 1):
            print(mat[i][j])
        print('')

if __name__ == '__main__':
    visualization(start='2018.01.01', end='2018.09.30', mat=clustering('C:/data/30x30.xlsx'), excel='C:/data/2000x2000.xlsx')