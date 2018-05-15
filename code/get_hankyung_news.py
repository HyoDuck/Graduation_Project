#writer : 김효빈
#date : 2018.05.14
#how to use : 전달인자로 1. 검색어, 2. 시간(언제부터), 3. 시간(언제까지) 넣어주면
#한국경제 홈페이지에서 검색어로 나오는 기사들을 크롤링합니다.
#2가지 function이 있는데 첫 번째는 일반 검색으로 뉴스의 text들을 가져오는 것,
#두 번째로는 태그를 활용한 검색입니다. 예를 들어 삼성전자에 관한 태그검색을 실행하면 #삼성전자로 태그붙인 기사들을 모두 가져옵니다.
#
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import time
import sys
import urllib.parse   # http encoding에 사용합니다.
from selenium import webdriver   # 웹 애플리케이션의 테스트를 자동화하기 위한 프레임 워크
#from selenium.webdriver.common.keys import Keys

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

# 한경신문에서 태그를 활용하여 기사를 가져옵니다.
#
def Get_tag_pages(keyword = None, start_time = "2018-01-01 12:00", end_time = "2018-06-01 12:00"):
    temp_list = []
    article_list = []
    page_num = 1
    article_time = ''

    keyword = urllib.parse.quote(keyword)       # 검색어를 http에 알맞게 변환합니다. ex) 한글 ==> %EC%D%.... 와 같은 형태로

    tag_address = "http://news.hankyung.com/tag/" + keyword + "?page=1"     # 검색어의 첫번째 페이지 주소로 초기화합니다.
    tag_page = Get_html(tag_address)        # source를 가져옵니다.


    while(1):
        temp_list = tag_page.find("ul", class_="list_basic")
        temp_list = temp_list.find_all("li")

        for i in range(0, len(temp_list), 1):
            article_time = temp_list[i].find("span", class_="time").text     #기사의 작성시간을 가져옵니다.

            if (str(article_time) > str(end_time)):        #전달인자로 준 시간정보와 비교하여 맞지 않는 날짜이면 기사를 체크하지 않습니다.
                continue
            elif (str(article_time) < str(start_time)):    #전달인자로 준 시간정보와 비교하여 지난 날짜의 기사이면 더 이상 받지않습니다.
                return article_list

            temp_list[i] = temp_list[i].find('a')           #기사의 주소만을 가져옵니다.
            temp_list[i] = temp_list[i].get('href')

            print(temp_list[i])

            article_list.append(temp_list[i])               #리스트에 http 주소를 넣습니다.

        for i in range(len(tag_address) - 1, 0, -1):
            if (tag_address[i] == '='):
                page_num = page_num + 1
                tag_address = tag_address[:i + 1] + str(page_num)
                tag_page = Get_html(tag_address)







# 한경신문에서 start_time부터 end_time까지 keyword로 검색된 기사를 가져옵니다.
# ex) 대한항공 관련 기사를 2017년 01월 01일부터 2018년 05월 11일까지
def Get_news_pages(keyword = None, start_time = "2018.01.01 12:00", end_time = "2018.06.01 12:00"):
    news_page_list = []     # 페이지에 있는 기사를 리스트에 저장합니다.
    news_time=''            # 기사 작성시간으로 초기화하는데 필요한 변수
    news_temp=""            # 기사 http 주소를 임시로 저장할 변수

    chrome = 'c:\\data\\chromedriver.exe'
    browser = webdriver.Chrome(chrome)

    browser.implicitly_wait(3)      # 브라우저 로드를 기다립니다.

    browser.get("http://search.hankyung.com/apps.frm/search.news?query=")

    page_num = 1
    browser.find_element_by_id("query").send_keys(keyword)  #검색어 보내기
    browser.find_element_by_class_name('btn_search').click()        #검색 클릭
    browser.find_element_by_xpath("//body")     #바디 클릭

    html = browser.page_source
    html = BeautifulSoup(html, "html.parser")
    current_page = html

    # 다음 페이지로 넘어갈 때 사용할 next_page
    next_page = current_page.find("div", class_="paging")
    next_page = next_page.find("div", class_="paging_wrap")
    next_page = next_page.find("a", class_="next")
    next_page = next_page.get('href')

    for j in range(len(next_page) - 1, 0, -1):
        if next_page[j] == '=':
            next_page = next_page[:j + 1] + str(page_num)
            next_page = "http://search.hankyung.com" + next_page
            break
    # 다음 페이지로 넘어갈 때 사용할 next_page

    while(1):       #코드 중간에 있는 elif문을 통해 반복문을 탈출합니다.
        news_pages = current_page.find("ul", class_="article")
        news_pages = news_pages.find_all("li")

        for i in range(0, 10 ,1):           #한 페이지당 10개씩 기사가 있는데, 이를 반복문 10번을 돌아서 가져옵니다.
            news_temp = news_pages[i].find("div", class_="txt_wrap")
            news_time = news_temp
            news_time = news_time.find('p', class_="info")       # 기사 작성시간 가져오기
            news_time = news_time.find("span", class_="date_time").text

            if (str(news_time) > str(end_time)):        #전달인자로 준 시간정보와 비교하여 맞지 않는 날짜이면 기사를 체크하지 않습니다.
                continue
            elif (str(news_time) < str(start_time)):    #전달인자로 준 시간정보와 비교하여 지난 날짜의 기사이면 더 이상 받지않습니다.
                return news_page_list

            news_temp = news_temp.find('a')             #http 주소만을 가져옵니다.
            news_temp = news_temp.get('href')

            news_page_list.append(news_temp)

        page_num = page_num + 1

        current_page = Get_html(next_page + str(page_num))      # 다음 페이지로 이동

    return news_page_list

def Get_article(news_list = [], file_name = "txt_file.txt"):            #전달받은 http list에서 text 정보만을 가져옵니다.
    article_list = []
    txt_file = open("C:\\data\\StockInfo\\news\\hankyung\\" + file_name, mode="w")  #파일오픈

    for i in range(0, len(news_list), 1):       #전달받은 http의 개수만큼 반복문을 돌립니다.
        article_page = Get_html(news_list[i])
        try:        #try except 문을 이용해 외부 http와 연결된 기사는 받아오지 않습니다.
            article_page = article_page.find("div", class_="articlebody ga-view").text
            article_page = article_page[:-65]       # 기사 끝에있는 반복되는 텍스트들은 문자열에서 제외합니다.
        except:
            continue

        article_list.append(article_page)

    for i in range(0, len(article_list), 1):        #txt 파일에 write
        txt_file.write(article_list[i])
    txt_file.close()


def Check_dir():                #디렉토리가 있는지 체크하고 없다면 생성합니다.
    if not os.path.isdir("C:\\data"):
        os.mkdir("C:\\data")
    if not os.path.isdir("C:\\data\\StockInfo"):
        os.mkdir("C:\\data\\StockInfo")
    if not os.path.isdir("C:\\data\\StockInfo\\news"):
        os.mkdir("C:\\data\\StockInfo\\news")
    if not os.path.isdir("C:\\data\\StockInfo\\news\\hankyung"):
        os.mkdir("C:\\data\\StockInfo\\news\\hankyung")

if __name__ == '__main__':
    Check_dir()
    #news_pages = Get_news_pages("대한항공", "2018.05.10 12:00", "2018.06.01 12:00")
    #Get_article(news_pages)
    tag_pages = Get_tag_pages("삼성전자", "2018-05-01 12:00", "2018-06-01 12:00")
    Get_article(tag_pages)
