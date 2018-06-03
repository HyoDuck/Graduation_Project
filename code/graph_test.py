# writer : 김효빈
# last update : 2018.06.04
# Csimilarity.comp_kos 로 얻어낸 리스트를 matplotlib를 이용하여 출력합니다.

import Csimilarity
import matplotlib as mlt

# ! 주의 ! 반드시 지켜야함.
# list[n][0]은 기준이 되는 종목번호
# list[n][1]은 비교할 종목번호
# list[n][2]은 차이값 평균치
# list[n][3]은 기준종목의 종가 리스트
# list[n][4]은 비교종목의 종가 리스트

# 그래프 2개씩 묶음으로 그려냅니다.
def graph_testing(source_list):
    mdf_list = []       #mdf_list[n][0]은 종목번호, mdf_list[n][1]은 변경된 종가 리스트입니다.
    stock_num_list = []

    for i in range(0, len(source_list), 1):
        temp_list = source_list[i]
        stock_num_list.append(temp_list[1])
        mdf_list.append(temp_list[4])

    stock_num_list.append(temp_list[0])
    mdf_list.append(temp_list[3])

    for i in range(0, len(mdf_list), 1):
        mlt.pyplot.plot(mdf_list[i], label=stock_num_list[i])

    mlt.pyplot.legend(loc='upper left')
    mlt.pyplot.show()

if __name__ == '__main__':
    test_list = Csimilarity.comp_kos(start_date="2017.06.01", end_date="2018.01.01", stock_num="005930", dirname = "C:\\data\\StockInfo\\Kospi", limit=2.5)
    graph_testing(test_list)