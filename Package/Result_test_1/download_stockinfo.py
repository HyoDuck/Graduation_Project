###############################################################################
# Update : 2018.06.15
# Writer : 김효빈
# 소스코드에 오류가 있었고 네이버 소스페이지에 전일비 부분에 변화가 있어서 다시 업데이트합니다.
# http://finance.naver.com/ 에서 주식종목 데이터를 받아 Excel 파일로 생성합니다.
# Excel file은 C:\data\StockInfo 에 kosdaq, kospi folder로 저장됩니다.
###############################################################################
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import os
#from openpyxl import Workbook
from pyexcelerate import Workbook
import time
import sys
#
# html 주소를 받아 페이지를 여는 함수
# 인터넷 연결이 불안정하여 중간에 끊길수도 있으니 except로 재호출하고 Error_Count를 +1한다.
# Error_Count가 100보다 커지면 프로그램을 강제로 종료한다.
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

#일일 주식정보를 가져온다.
def Get_Daily_Info(codenum = None, stock_name = None, save_address = "C:\\data\\StockInfo"):
    if(os.path.isfile(save_address + "\\" + str(codenum) + "_" + str(stock_name) + ".xlsx") == True):
        print(str(codenum) + "_" + str(stock_name) + " is already exist \n")
        return -1

    stock_info = [[codenum, stock_name], ["날짜", "종가", "전일비", "시가", "고가", "저가", "거래량"]]
    print("connect to " + str(codenum) + "_" + str(stock_name) + "\n")
    Url = 'http://finance.naver.com/item/sise_day.nhn?code=' + codenum
    # 일별 주식 페이지는
    # http://finance.naver.com/item/sise_day.nhn?code= + 종목번호로 이루어져 있다.
    Source = Get_html(Url)

    Page_select = Source.find("table", align = "center")
    #1/2/3/4/5/6/7/8/9/10 맨뒤 ... nnavi table
    try:
        MaxPage_section = Page_select.find("td", class_= "pgRR")
        #1/2/3/4/5 ... 맨뒤 ... 맨뒤로가기를 선택한다.
        MaxPage_section = MaxPage_section.find("a")
        MaxPage_section = MaxPage_section.get('href')
    except:     #등록된지 얼마되지 않아 1페이지만 있는 종목일 때 예외처리
        MaxPage_section = "/item/sise_day.nhn?code=500013&page=1"
    print(MaxPage_section)
    MaxPage_section = "http://finance.naver.com" + MaxPage_section
    MaxPage_section = Get_html(MaxPage_section)

    MaxPage_num = MaxPage_section.find("table", summary = "페이지 네비게이션 리스트")
    MaxPage_num = MaxPage_num.find("td", class_ = "on")
    MaxPage_num = int(MaxPage_num.find("a").text)
    #맨뒤로 가기 선택 또는 사용자가 원하는 날짜가 있는 페이지까지 이동 후 그 부분부터 자료를 가져오는 코드를 만들 것.

    #1페이지 ~ 마지막 페이지까지 반복문
    for page in range(1, MaxPage_num + 1):
        get_url = 'http://finance.naver.com/item/sise_day.nhn?code=' + codenum + '&page=' + str(page)
        get_source = Get_html(get_url)
        srlists = get_source.find_all("tr")
        variation = ''
        #홈페이지 주소에 있는 필요한 html코드의 frame들을 가져온다.

        #하루씩 데이터를 가져오는 반복문
        for i in range(1, len(srlists) - 1):
            if(srlists[i].span != None):
                day = srlists[i].find_all("td", align = "center")[0].text
                price_closing = srlists[i].find_all("td", class_="num")[0].text

                compare_yesterday = srlists[i].find("img")

                #전일비 + / - 를 표시하는 이미지 파일이 있을시에 정보를 가져온다.
                if(compare_yesterday != None):
                    inc_price = compare_yesterday.get("src")        #상승 혹은 하락을 저장할 변수 inc_price
                    non_marking = srlists[i].find_all("td", class_="num")[1].text
                    #전일비교 가격변동 but 앞에 상승,하락 / +,- 가 이미지 파일로 되어있어 숫자만 따로 가져온다.
                    non_marking = re.sub("\n", "", non_marking)
                    non_marking = re.sub("\r", "", non_marking)
                    non_marking = re.sub("\t", "", non_marking)
                    #네이버 주식페이지에 전일비값 앞뒤로 개행문자와 tab문자가 있어 이를 제거한다.

                    #네이버 주식페이지에 전일비값 +와 -값이 이미지 파일로 저장되어있어 이를 이용해 상승,하락 문자를 붙여준다.
                    if(inc_price == "https://ssl.pstatic.net/imgstock/images/images4/ico_down.gif"):
                        variation = '-' + non_marking
                    elif(inc_price == "https://ssl.pstatic.net/imgstock/images/images4/ico_up.gif"):
                        variation = '+' + non_marking
                else:
                    variation = '0'     #변동폭이 없을 때는 0

                price_opening = srlists[i].find_all("td", class_="num")[2].text
                price_high = srlists[i].find_all("td", class_="num")[3].text
                price_low = srlists[i].find_all("td", class_="num")[4].text
                total_volume = srlists[i].find_all("td", class_="num")[5].text

                #stock_info를 주식정보들의 변수들로 초기화함.
                stock_info.append([day, price_closing, variation, price_opening, price_high, price_low, total_volume])

    # 워드파일 생성
    # 종목코드, 회사명을 포함한 문자열을 워드파일에 씀
    wb = Workbook()
    wb.new_sheet("first sheet", data=stock_info)
    #파일명에서 /*?: 등 사용할 수 없는 문자가 왔을 때 except 문을 실행한다.
    try:
        wb.save(save_address + "\\{}.xlsx".format(codenum+"_"+stock_name))
    except:
        stock_name = re.sub('[<|>|\|*|:|/|?"]', "_", stock_name)
        wb.save(save_address + "\\{}.xlsx".format(codenum + "_" + stock_name))

#코스피 정보를 가져오는 함수
def Get_KospiInfo(save_folder = "C:\\data\\StockInfo"):
    Source1 = Get_html("http://finance.naver.com/sise/sise_market_sum.nhn?&page=1")

    Page_select = Source1.find("table", class_="Nnavi")
    # 1/2/3/4/5/6/7/8/9/10 맨뒤 ... 부분의 코드를 가지게 한다.

    MaxPage_section = Page_select.find("td", class_="pgRR")
    MaxPage_section = MaxPage_section.find("a")
    MaxPage_section = MaxPage_section.get('href')
    MaxPage_section = "http://finance.naver.com" + MaxPage_section
    # 마지막 페이지의 html 주소로 MaxPage_section을 초기화한다.

    Source2 = Get_html(MaxPage_section)
    # 1/2/3/4/5 ... 맨뒤 ... 맨뒤로 가기를 선택

    MaxPage_num = Source2.find("td", class_="on")
    MaxPage_num = int(MaxPage_num.find("a").text)
    #마지막 페이지 번호를 가져온다.

    #코스피 첫 페이지부터 마지막 페이지까지 기업명과 번호를 가져온다.
    for i in range(1, MaxPage_num + 1):
        Source3 = Get_html("http://finance.naver.com/sise/sise_market_sum.nhn?&page=" + str(i))
        #기업리스트가 있는 페이지를 마지막 페이지까지 차례대로 연다.

        inc_list = Source3.find_all("tr", onmouseover="mouseOver(this)")
        #하나의 페이지마다 있는 기업들의 정보를 inc_list에 초기화시킨다.

        for j in range(0, len(inc_list)):
            inc_select = inc_list[j].find("a", class_="tltle")
            inc_select = inc_select.get('href')
            #기업정보를 보는 페이지 주소를 만듦
            Source4 = Get_html("http://finance.naver.com" + str(inc_select))

            #inc_code를 종목번호로 초기화
            inc_code = Source4.find("span", class_="code")
            inc_code = inc_code.text

            #inc_name를 기업명으로 초기화
            inc_name = Source4.find("a", onclick="clickcr(this, 'sop.title', '', '', event);window.location.reload();")
            inc_name = inc_name.text

            Get_Daily_Info(inc_code, inc_name, save_folder)

def Get_KosdaqInfo(save_folder = "C:\\data\\StockInfo"):
    Source1 = Get_html("http://finance.naver.com/sise/sise_market_sum.nhn?sosok=1")

    Page_select = Source1.find("table", class_="Nnavi")
    # 1/2/3/4/5/6/7/8/9/10 맨뒤 ... 부분의 코드를 가지게 한다.

    MaxPage_section = Page_select.find("td", class_="pgRR")
    MaxPage_section = MaxPage_section.find("a")
    MaxPage_section = MaxPage_section.get('href')
    MaxPage_section = "http://finance.naver.com" + MaxPage_section
    # 마지막 페이지의 html 주소로 MaxPage_section을 초기화한다.

    Source2 = Get_html(MaxPage_section)
    # 1/2/3/4/5 ... 맨뒤 ... 맨뒤로 가기를 선택

    MaxPage_num = Source2.find("td", class_="on")
    MaxPage_num = int(MaxPage_num.find("a").text)
    # 마지막 페이지 번호를 가져온다.

    # 코스피 첫 페이지부터 마지막 페이지까지 기업명과 번호를 가져온다.
    for i in range(1, MaxPage_num + 1):
        Source3 = Get_html("http://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page=" + str(i))
        # 기업리스트가 있는 페이지를 마지막 페이지까지 차례대로 연다.

        inc_list = Source3.find_all("tr", onmouseover="mouseOver(this)")
        # 하나의 페이지마다 있는 기업들의 정보를 inc_list에 초기화시킨다.

        for j in range(0, len(inc_list)):
            inc_select = inc_list[j].find("a", class_="tltle")
            inc_select = inc_select.get('href')
            # 기업정보를 보는 페이지 주소를 만듦
            Source4 = Get_html("http://finance.naver.com" + str(inc_select))

            # inc_code를 종목번호로 초기화
            inc_code = Source4.find("span", class_="code")
            inc_code = inc_code.text

            # inc_name를 기업명으로 초기화
            inc_name = Source4.find("a", onclick="clickcr(this, 'sop.title', '', '', event);window.location.reload();")
            inc_name = inc_name.text

            Get_Daily_Info(inc_code, inc_name, save_folder)

if __name__ == '__main__':
    #폴더가 없을 시 생성
    if not os.path.isdir("C:\\data"):
        os.mkdir("C:\\data")
    if not os.path.isdir("C:\\data\\StockInfo"):
        os.mkdir("C:\\data\\StockInfo")
    if not os.path.isdir("C:\\data\\StockInfo\\Kosdaq"):
        os.mkdir("C:\\data\\StockInfo\\Kosdaq")
    if not os.path.isdir("C:\\data\\StockInfo\\Kospi"):
        os.mkdir("C:\\data\\StockInfo\\Kospi")

    Get_KosdaqInfo("C:\\data\\StockInfo\\Kosdaq")
    Get_KospiInfo("C:\\data\\StockInfo\\Kospi")