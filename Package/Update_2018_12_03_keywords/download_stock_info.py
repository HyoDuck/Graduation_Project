import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter

sns.set(style="white")
plt.rcParams["font.family"] = 'HYSinMyeongJo-Medium'
plt.rcParams["font.size"] = 12

code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

n = 0

code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
code_df = code_df[['회사명', '종목코드']]
code_df = code_df[['회사명', '종목코드']]
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})


def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    print("요청 URL = {}".format(url))
    return url

def downloading():
    priceDic = {}

    namelist = code_df['name']

    for name in namelist:
        item_name = name
        url = get_url(item_name, code_df)
        df = pd.DataFrame()
        for page in range(1, 22):
            pg_url = '{url}&page={page}'.format(url=url, page=page)
            df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
        df = df.dropna(how='all')
        pricelist = df['종가']
        priceDic[item_name] = pricelist
        n += 1

    All_Price = pd.DataFrame(priceDic)
    All_Price.index = df['날짜']
    All_Price = All_Price.dropna(how='all')

    writer = ExcelWriter('price_list.xlsx')
    All_Price.to_excel(writer, 'Sheet1')
    writer.save()