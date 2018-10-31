### 키워드 추출하는 부분 code .py
import Get_keywords
import make_keywords_xlsx
##############################################
# 클러스터링 부분 code .py
import cluster1
import make_comp_list
##############################################
import os
from operator import eq

def all_in_one(start_date='2018-01-01', end_date='2018-09-30', excel_path='C:/data/1000.xlsx', max_min=1.5, use_navertrend = False):
    #def Keywords(start_date, end_date, word_list, comp_word_list,
    #         chrome_path='c:\\data\\chromedriver.exe',
    #         default_path = 'C:/data/' + 'Keywords/' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
    #         academy_xlsx_path='', NaverTrend_path='', array2D_path='', stock_title_path=''):
    #input_list = cluster1.clustering(excel=excel_path, y=max_min)
    input_list = [['오이솔루션', '유엔젤'], ['웰크론', '체시스','한솔홈데코'], ['동양물산기업', '일성건설'],
                  ['웨이브일렉트로', '광명전기', '영흥철강', '우원개발'], ['제주항공', '한창'],
                  ['엑사이엔씨', '성신양회', '현대로템'], ['행남사', '한일현대시멘트'],
                  ['에이티넘인베스트', '광전자', '한솔피엔에스']]

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

            for path_checker in os.listdir('C:/data/Keywords'):
                if eq(path_checker[19:], input_list[i][0] + '_포함_' + str(len(input_list[i])) + '_종목'):
                    continue  # 이미 존재하는 자료일 때는 continue하여 다음으로 넘어갑니다.

            comp_input_list = make_comp_list.word_list(excel=excel_path, word=input_list[i][0])

            if len(comp_input_list) > 6:        # 대조비교군을 형성할 기업명들을 줄입니다.
                comp_input_list = comp_input_list[:6]

            print("in start_with_this - comp_input_list")
            print(comp_input_list)

            temp = Get_keywords.Keywords(start_date=start_date, end_date=end_date, word_list=input_list[i], comp_word_list=comp_input_list, use_navertrend=use_navertrend)

            if temp == False:
                continue

            keywords_result.append(temp)
            stock_list.append(input_list[i])

    return stock_list, keywords_result

if __name__ == '__main__':
    #stock_result, keywords_result = all_in_one(start_date='2018-01-01', end_date='2018-10-25', excel_path='C:/data/corr.xlsx', max_min=1.5, use_navertrend=True)
    #make_keywords_xlsx.make_xlsx(stock_list=stock_result, keywords_list=keywords_result)

    #for i in range(0, len(keywords_result), 1):
    #    print(str(i) + " stock")
    #    print(stock_result[i])
    #    print(str(i) + " stock")
    #    print(keywords_result[i])
    #    print('')
    print("test")
    all_in_one(start_date='2018-01-01', end_date='2018-10-30', excel_path='C:/data/corr.xlsx', max_min=1.5,
               use_navertrend=True)