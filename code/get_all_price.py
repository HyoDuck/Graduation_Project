import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter

sns.set(style="white")
plt.rcParams["font.family"] = 'HYSinMyeongJo-Medium'
plt.rcParams["font.size"] = 12

code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

n=0

code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
code_df = code_df[['회사명', '종목코드']]
code_df = code_df[['회사명','종목코드']]
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})


def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    print("요청 URL = {}".format(url))
    return url



def get_All_Price(start,end):
    n=0
    priceDic={}
    namelist=code_df['name']
    for name in namelist:
        if(n<5):
            item_name=name
            url=get_url(item_name,code_df)
            df=pd.DataFrame()
            for page in range(1, 12):
                pg_url = '{url}&page={page}'.format(url=url, page=page)
                df = df.append(pd.read_html(pg_url, header=0)[0],     ignore_index=True)
            df = df.dropna()
            length=len(df.index)
            df.index = pd.RangeIndex(len(df.index))
            df = df[df.날짜 <end]
            df = df[df.날짜 >start]
            df.index = pd.RangeIndex(len(df.index))
            pricelist=df['종가']
            priceDic[item_name]=pricelist
            n+=1
    All_Price=pd.DataFrame(priceDic)
    writer = ExcelWriter('price.xlsx')
    All_Price.to_excel(writer,'Sheet1')
    writer.save()
    corr = All_Price.corr(method = 'pearson')
    writer = ExcelWriter('corr.xlsx')
    corr.to_excel(writer,'Sheet1')
    writer.save()
    All_Price.index=df['날짜']
    return All_Price
    
if __name__ == "__main__":
    start, end=input('시작날짜와 끝 날짜  입력 ex)2018.09.01 2018.10.01 :').split()
    price=get_All_Price(start,end)
    print(price)
