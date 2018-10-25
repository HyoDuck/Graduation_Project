import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter
import xlrd
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram

df=pd.read_excel('C:/Users/user/Desktop/price all 2000x2000.xlsx')
df = df[df.날짜 <='2018.09.01']
df= df [df.날짜>='2018.08.01']
df.index = pd.RangeIndex(len(df.index))
df=df.drop("날짜",1)

writer = ExcelWriter('all_price.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()

corr = df.corr(method = 'pearson')
writer = ExcelWriter('corr.xlsx')
corr.to_excel(writer,'Sheet1')
writer.save()

