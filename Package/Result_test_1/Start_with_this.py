### 키워드 추출하는 부분 code .py
import Get_keywords
##############################################
# 클러스터링 부분 code .py
import cluster1
import make_comp_list
##############################################

def test1(start_date='2018-01-01', end_date='2018-09-30', excel_path='C:/data/1000.xlsx', max_min=1.5):
    #def Keywords(start_date, end_date, word_list, comp_word_list,
    #         chrome_path='c:\\data\\chromedriver.exe',
    #         default_path = 'C:/data/' + 'Keywords/' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
    #         academy_xlsx_path='', NaverTrend_path='', array2D_path='', stock_title_path=''):
    input_list = cluster1.clustering(excel=excel_path, y=max_min)
    print(input_list)
    print("start test1")
    #input_list = ['한국화장품', 'lg생활건강', '명인화장품']
    print("before getting keywords")

    stock_list = []         # 키워드 추출에 사용한 클러스터들
    keywords_result = []    # 키워드 결과물

    # 키워드 추출을 실행하는 for문
    # stock_list[i]번째에 포함된 종목명들로 keywords_list[i]번째의 키워드들이 추출됩니다.
    for i in range(0, len(input_list), 1):
        if (int)(len(input_list[i])) != 1:
            print(str(i) + " list")
            comp_input_list = make_comp_list.word_list(excel=excel_path, word=input_list[i][0])
            #comp_input_list = comp_input_list[:(int)(len(comp_input_list) / 2)]         # comp_input_list를 절반으로 줄임

            if len(comp_input_list) > 6:        # 대조비교군을 형성할 기업명들을 줄입니다.
                comp_input_list = comp_input_list[:6]

            print("in start_with_this - comp_input_list")
            print(comp_input_list)

            temp = Get_keywords.Keywords(start_date=start_date, end_date=end_date, word_list=input_list[i], comp_word_list=comp_input_list)

            keywords_result.append(temp)
            stock_list.append(input_list[i])

    return stock_list, keywords_result

if __name__ == '__main__':
    stock_result, keywords_result = test1(start_date='2018-01-01', end_date='2018-09-30', excel_path='C:/data/1000.xlsx', max_min=1.5)

    for i in range(0, len(keywords_result), 1):
        print(str(i) + " stock")
        print(stock_result[i])
        print(str(i) + " stock")
        print(keywords_result[i])
        print('')