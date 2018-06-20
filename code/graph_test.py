# writer : 김효빈
# last update : 2018.06.20
# Csimilarity.comp_kos 로 얻어낸 리스트를 matplotlib를 이용하여 출력합니다.
# 출력에 문제가 있어 수정 후 재업로드합니다. ######## 그래도 한 번 더 수정이 필요합니다. ##########

import Csimilarity
import matplotlib as mlt
import matplotlib.pyplot as plt

# ! 주의 ! 반드시 지켜야함.
# list[n][0]은 기준이 되는 종목번호
# list[n][1]은 비교할 종목번호
# list[n][2]은 차이값 평균치
# list[n][3]은 기준종목의 종가 리스트
# list[n][4]은 비교종목의 종가 리스트

# 그래프 2개씩 묶음으로 그려냅니다.
def graph_testing(source_list):
    figure_num = 1
    try:
        if len(source_list) == 0:
            print("len of source_list == 0")
            return 0
    except:
        print("Error occured in graph_testing")
        return -1
    mdf_list = []       #mdf_list[n][0]은 종목번호, mdf_list[n][1]은 변경된 종가 리스트입니다.
    stock_num_list = []

    for i in range(0, len(source_list), 1):
        temp_list = source_list[i]
        stock_num_list.append(temp_list[1])
        mdf_list.append(temp_list[4])

    stock_num_list.append(source_list[0][0])
    mdf_list.append(source_list[0][3])

    print(mdf_list)
    print(stock_num_list)

    for i in range(0, len(mdf_list), 1):
        showing(source_list[0][3], mdf_list[i], source_list[0][0], stock_num_list[i], figure_num)
        figure_num = figure_num + 1


def showing(data1, data2, label1, label2, figure_num):
    plt.figure(figure_num)
    plt.plot(data1, label=label1)
    plt.plot(data2, label=label2)

    plt.legend()
    plt.show()

if __name__ == '__main__':
    test_list1 = Csimilarity.comp_kos(start_date="2017.11.01", end_date="2018.06.01", stock_num="014990", dirname="C:\\data\\StockInfo\\test_list", limit=20)
    print(test_list1)
    graph_testing(test_list1)
