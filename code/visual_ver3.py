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

#일정기간동안의 주식종목의 상관관계 계수 구하는 함수
def corr(excel,start,end): 
	df=pd.read_excel(excel)
	df = df[df.날짜 <=end]
	df= df [df.날짜>=start]
	df.index = pd.RangeIndex(len(df.index))
	df=df.drop("날짜",1)
	df=df.dropna(how='all')
	df=df.dropna(axis=1)
	writer = ExcelWriter('all_price.xlsx')
	df.to_excel(writer,'Sheet1')
	writer.save()

	corr = df.corr(method = 'pearson')
	corr=round(corr,4)
	corr=corr.dropna(how='all')
	corr=corr.dropna(axis=1)
	writer = ExcelWriter('corr.xlsx')
	corr.to_excel(writer,'Sheet1')
	writer.save()

	return corr

#상관계수를 바탕으로 클러스터링하는 함수
def clustering(excel,y): 
    data = 1-abs(pd.read_excel(excel))
    row_clusters = linkage(data, method='complete')
    labels = data.index
    predict = pd.DataFrame(fcluster(row_clusters,1.5,criterion='distance'),data.index)
    predict.columns=['predict']
    cluster=predict['predict'].values.tolist()
    max_num=max(cluster)
    mat = []
    for i in range(max_num):
        if len(predict.index[predict['predict']==i+1].tolist())>1 :
            mat.append(predict.index[predict['predict']==i+1].tolist())
    return mat

#시각화함수
def visualization(excel,start,end,mat): 
    df=pd.read_excel(excel)
    df = df[df.날짜 <=end]
    df= df [df.날짜>=start]
    date=df['날짜'].tolist()
    df.index = df['날짜']
    df=df.drop("날짜",1)
    df=df.sort_index()
    df = df.apply(lambda x: x / x[0])
    length=len(mat)
    view=pd.DataFrame()
    word=pd.DataFrame()

    for j in range(length):
        word_len=len(mat[j])
        empty=pd.DataFrame()
        for k in range(word_len) :
            if k==0:
                word=df[mat[j][k]]
            else:
                word=word + df[mat[j][k]]
        word= word/word_len
        empty=pd.concat((empty,word),axis=1)
        hop=','.join(mat[j])
        empty.columns=[hop]
        view=pd.concat((view,empty),axis=1)

    x=[]
    for day in date:
        times=datetime.datetime.strptime(day,"%Y.%m.%d").date()
        x.append(times)



        
    view['date']=view.index
    view['datetime'] = view['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y.%m.%d'))
    view.set_index(view['datetime'], inplace=True)
    view = view.drop('datetime', 1)
    view = view.drop('date', 1)
    plt.plot(view,label=mat)
    plt.legend(view.columns,loc='upper left')
    plt.grid(True)
    plt.axhline(y = 1, color = "black", lw = 2)
    plt.show()
    return view

if __name__ == "__main__":
	start=input('시작날짜 입력 ex)2018.09.01  :')
	end=input('끝 날짜  입력 ex)2018.09.01  :')
	corr('C:/Users/user/Desktop/all_stock.xlsx',start,end)
	mat=clustering('C:/Anaconda3/Lib/idlelib/corr.xlsx',1.5)
	view=visualization('C:/Users/user/Desktop/all_stock.xlsx',start,end,mat)
    
