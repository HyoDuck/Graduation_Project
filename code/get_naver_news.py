# writer : 김효빈
# date : 2018.05.14
# http://finance.naver.com/item/news.nhn?code= 에서 뉴스, 공시 정보를 가져옵니다
# 가져온 기사들을 txt 파일로 저장하는 path는 "C:\\data\\StockInfo\\news\\naver" 입니다.
#
# 자연어 처리코드, 빈도수 체크하는 코드 추가예정

from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import time
import sys
import urllib.parse   # http encoding에 사용합니다.

def Get_html(address = None, Error_Count = 1):
    try:
        Url = address
        Html = urlopen(Url)
        Source = BeautifulSoup(Html.read(), "html.parser")
        return Source
    except:
        print("Error_Count : " + str(Error_Count) + "\n")
        if Error_Count < 100 :
            time.sleep(3)
            return Get_html(address, Error_Count + 1)
        else:
            sys.exit(1)

# 시작날짜부터 종료날짜까지 종목번호로 검색된 기사들의 http 주소를 가져오는데 쓰이는 함수입니다.
# http://finance.naver.com/item/news.nhn?code= 에서 뉴스, 공시 부분을 이용합니다.
# 기사들의 http 주소는 리스트 형태로 묶여서 return 됩니다.
# keyword = 종목번호, start_date = 시간(언제부터), end_date = 시간(언제까지) 입니다.
def Get_newsPage_naver(keyword = None, start_date = "2018.01.01 12:00", end_date = "2018.05.15 12:00"):
    temp_list = []
    article_list = []
    page_num = 1
    article_time = ''

    keyword = urllib.parse.quote(keyword)  # 검색어를 http에 알맞게 변환합니다. ex) 한글 ==> %EC%D%.... 와 같은 형태로

    finance_address = "http://finance.naver.com/item/news_news.nhn?code=" + keyword + "&page=" + str(page_num) + "&sm=title_entity_id.basic&clusterId="  # 검색어의 첫번째 페이지 주소로 초기화합니다.
    finance_page = Get_html(finance_address)  # source를 가져옵니다.

    print(finance_page)

    while(1):
        finance_page = finance_page.find("tbody")
        temp_list = finance_page.find_all("tr")

        for i in range(0, len(temp_list), 1):
            article_time = temp_list[i].find("td", class_="date").text
            article_time = article_time[1:]
            print(article_time)

            if (str(article_time) > str(end_date)):        #전달인자로 준 시간정보와 비교하여 맞지 않는 날짜이면 기사를 체크하지 않습니다.
                continue
            elif (str(article_time) < str(start_date)):    #전달인자로 준 시간정보와 비교하여 지난 날짜의 기사이면 더 이상 받지않습니다.
                return article_list

            temp_list[i] = temp_list[i].find('a')
            temp_list[i] = temp_list[i].get('href')
            temp_list[i] = "http://finance.naver.com" + temp_list[i]

            article_list.append(temp_list[i])

            print(temp_list[i])

        page_num = page_num + 1

        #검색어의 n번째 주소로 초기화합니다.
        finance_address = "http://finance.naver.com/item/news_news.nhn?code=" + keyword + "&page=" + str(page_num) + "&sm=title_entity_id.basic&clusterId="
        finance_page = Get_html(finance_address)

# http 주소들을 리스트 형태로 전달받으면 "C:\\data\\StockInfo\\news\\naver" 위치에 .txt 파일을 만들어 text 정보들을 저장합니다.
# source_list = 주소 리스트, txt_file = "C:\\data\\StockInfo\\news\\naver" 위치에 생성되는 .txt 파일 정보
# 이전에 생성되었던 파일과 같은 txt파일이름을 전달할시에는 이전에 있던 txt파일의 text들이 모두 삭제됩니다.
def Get_text_naver(source_list = None, txt_file = "txt_file.txt"):
    txt_path = "C:\\data\\StockInfo\\news\\naver\\" + txt_file
    file_cont = open(txt_path, mode='w', encoding='utf-8')

    for i in range(0, len(source_list), 1):
        source_page = Get_html(source_list[i])
        source_page = source_page.find("table", class_="view")
        source_page = source_page.find("div", id="news_read").text

        try:
            file_cont.write(source_page)
        except:
            print(source_list[i])
            print(source_page)

            #file_cont.write(source_page.decode('UTF-8').encode('EUC-KR', 'replace'))

    file_cont.close()

# "C:\\data\\StockInfo\\news\\naver" 디렉토리가 모두 있는지 체크하고 없다면 생성합니다.
def Check_dir():
    if not os.path.isdir("C:\\data"):
        os.mkdir("C:\\data")
    if not os.path.isdir("C:\\data\\StockInfo"):
        os.mkdir("C:\\data\\StockInfo")
    if not os.path.isdir("C:\\data\\StockInfo\\news"):
        os.mkdir("C:\\data\\StockInfo\\news")
    if not os.path.isdir("C:\\data\\StockInfo\\news\\naver"):
        os.mkdir("C:\\data\\StockInfo\\news\\naver")

if __name__ == '__main__':
    Check_dir()
    test = Get_newsPage_naver('005930', "2018.05.01 12:00", "2018.05.14 12:00")
    Get_text_naver(test)
