import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

#데이터 포인트를 만듭니다.
df = pd.DataFrame(columns=['x', 'y']) #columns name x, y로 지정
#x, y 데이터 포인트 지정
df.loc[0] = [3,1]
df.loc[1] = [4,1]
df.loc[2] = [3,2]
df.loc[3] = [4,2]
df.loc[4] = [10,5]
df.loc[5] = [10,6]
df.loc[6] = [11,5]
df.loc[7] = [11,6]
df.loc[8] = [15,1]
df.loc[9] = [15,2]
df.loc[10] = [16,1]
df.loc[11] = [16,2]

print(df.head(20)) #만든 데이터 프레임 출력

#데이터 포인트를 보여줍니다.
sns.lmplot('x', 'y', data=df, fit_reg=False, scatter_kws={"s": 200})

#타이틀
plt.title('kmean plot')

#x-axis lable
plt.xlabel('x')

#y-axis lable
print(plt.ylabel('y'))

#데이터 프레임을 numpy 배열 형식으로 변경해 줍니다.
data_points = df.values

#클러스터의 갯수를 지정합니다.
kmeans = KMeans(n_clusters=3).fit(data_points)

#각각의 데이터에 대한 클러스터 넘버를 보여줍니다.
print(kmeans.labels_)

#각각의 클러스터의 중심 지점(x, y축)을 출력합니다.
print(kmeans.cluster_centers_)

#데이터 프레임의 클러스터 id랑 kmean의 클러스터 id들을 붙여줍니다.
df['cluster_id'] = kmeans.labels_

#x, y 축 데이터에 따른 클러스터 id를 출력합니다.
print(df.head(12))

#각 클러스터의 색깔을 구분합니다.
sns.lmplot('x', 'y', data=df, fit_reg=False,
scatter_kws={"s": 150},
hue="cluster_id")
print(plt.title('after kmean clustering'))










