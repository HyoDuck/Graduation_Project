# 이 파일을 테스트하려면 ID와 PWD가 필요합니다.
# 저에게 연락을 주시면 보내드리겠습니다.

# writer : 김효빈
# upload date : 2018-07-24
# 'http://academy.some.co.kr/login.html' 에서 검색어에 해당하는 키워드들을 워드파일로 저장하는 .py 파일입니다.
# def download_keywords(start_date = "2017-11-01", end_date = "2018-06-01", search_key=None,
#                      ID = None, PWD = None, page = 'http://academy.some.co.kr/login.html'):
# 이를 호출하면 selenium을 사용하여 자동으로 검색하고 워드파일 다운로드를 수행합니다.
# 전달인자는 ( 시작일, 마지막일, 검색어 리스트, 아이디, 비밀번호) 입니다.
# default 다운로드 경로 : C:/data/download
# 후에 추가가 필요할 수도 있는 부분은
# 다운로드 경로를 전달인자에 추가하여 사용자가 지정할 수 있도록 하는 것
# 한 번 함수를 호출하였을 때 다운로드 경로 아래에 새로 폴더를 만들어 어떤 리스트로 검색하였는지 알아보기 쉽도록 하는 부분.
# 다운받은 파일은 '검색어_시작일_마지막일'(ex 우원개발_20170101_20180101) 로 저장이 되는데
# 파일명에 종목명(검색어)뿐만 아니라 종목번호도 같이 넣어 저장하도록 하는 부분.


import os
import time
from selenium import webdriver   # 웹 애플리케이션의 테스트를 자동화하기 위한 프레임 워크
from datetime import datetime

def find_Sday(today, start_date, datebox):
    today_year = datetime.today().year  # int형으로 오늘 날짜를 기준으로 year와 month를 받아온다.
    today_month = datetime.today().month
    # 시작날짜 정하기   YYYY-MM 까지 시작날짜를 맞춥니다.
    while (today != start_date[:7]):
        datebox.find_element_by_tag_name("span").click()
        today_month = today_month - 1

        if today_month == 0:
            today_month = 12
            today_year = today_year - 1

        if today_month > 9:
            today = str(today_year) + "-" + str(today_month)
        else:
            today = str(today_year) + "-0" + str(today_month)

    tdset = datebox.find_elements_by_tag_name("td")  # tag name "td"는 날짜선택 달력에서 1일부터 마지막일(ex 29일 ~ 31일)까지의 선택칸입니다.

    # 시작일을 정합니다 YYYY-MM까지는 위 while문에서 찾았고, 시작일은 아래 for문에서 클릭합니다.
    for i in range(0, 31, 1):
        if tdset[i].text == ' ':    # 공백일시 i를 +1하고 넘김
            continue
        elif int(tdset[i].text) > 9:
            tdset_test = tdset[i].text  # 몇 일인지를 확인하기 위한 teset_test
        else:
            tdset_test = '0' + str(tdset[i].text)

        if tdset_test == start_date[8:10]:
            tdset[i].click()
            break

    return today

def find_Eday(today, end_date, datebox):
    today_year = datetime.today().year  # int형으로 오늘 날짜를 기준으로 year와 month를 받아온다.
    today_month = datetime.today().month
    # 시작연도 및 월 정하기   YYYY-MM 까지 시작날짜를 맞춥니다.
    while (today != end_date[:7]):
        datebox.find_element_by_tag_name("span").click()
        today_month = today_month - 1

        if today_month == 0:
            today_month = 12
            today_year = today_year - 1

        if today_month > 9:
            today = str(today_year) + "-" + str(today_month)
        else:
            today = str(today_year) + "-0" + str(today_month)

    tdset = datebox.find_elements_by_tag_name("td")  # tag name "td"는 날짜선택 달력에서 1일부터 마지막일(ex 29일 ~ 31일)까지의 선택칸입니다.

    # 마지막일을 정합니다 YYYY-MM까지는 위 while문에서 찾았고, 시작일은 아래 for문에서 클릭합니다.
    for i in range(0, 31, 1):
        if tdset[i].text == ' ':    # 공백일시 i를 +1하고 넘김
            continue
        elif int(tdset[i].text) > 9:
            tdset_test = tdset[i].text  # 몇 일인지를 확인하기 위한 teset_test
        else:
            tdset_test = '0' + str(tdset[i].text)

        if tdset_test == end_date[8:10]:
            tdset[i].click()
            break

    return today

#'http://academy.some.co.kr/login.html'에서 해당 검색어의 키워드들을 워드파일로 저장합니다.
def download_keywords(start_date = "2017-11-01", end_date = "2018-06-01", search_key=None,
                      ID = None, PWD = None):
    ### 옵션설정 ###
    # 크롬 드라이버에서 adobe flash를 사용하는 것과 다운로드 경로를 설정합니다.
    prefs = {
        "profile.default_content_setting_values.plugins": 1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        "PluginsAllowedForUrls": "http://academy.some.co.kr",
        "download.default_directory": "C:/data/download"        #이 부분에서 다운로드 경로를 설정합니다.
    }
    ### 옵션설정 ###
    page = 'http://academy.some.co.kr/login.html'       # page 변수 절대 수정하지 마세요.
    today_year = datetime.today().year          #int형으로 오늘 날짜를 기준으로 year와 month를 받아온다.
    today_month = datetime.today().month
    if today_month > 9:
        today = str(today_year) + "-" + str(today_month)
        ch_file = str(today_year) + str(today_month)
    else:
        today = str(today_year) + "-0" + str(today_month)
        ch_file = str(today_year) + '0' + str(today_month)

    comp_today1 = today
    comp_today2 = today
    num_check = 0

    chrome = 'c:\\data\\chromedriver.exe'       #크롬드라이버 경로
    chrome_options = webdriver.ChromeOptions()      #adobe flash player를 사용하기 위한 옵션설정을 하는데 사용합니다.
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome, chrome_options=chrome_options)

    browser.implicitly_wait(3)  # 브라우저 로드를 기다립니다.-----

    browser.get(page)

    ### 로그인 ###
    browser.find_element_by_name("userId").send_keys(ID)
    browser.find_element_by_name("userPswd").send_keys(PWD)
    browser.find_element_by_class_name("f_btn").click()
    ### 로그인 ###

    # 검색어와 달력을 활용한 조건설정, 다운로드를 수행하는 for문
    for i in range(0, len(search_key), 1):
        browser.find_element_by_id("topMenuImage").click()
        browser.find_element_by_name("directKey").clear()
        browser.find_element_by_name("directKey").send_keys(search_key[i])
        cal_img = browser.find_elements_by_class_name("ui-datepicker-trigger")
        datebox = browser.find_element_by_id("ui-datepicker-div")

        #시작일과 마지막일을 클릭합니다.
        cal_img[0].click()  #달력 펼치기
        comp_today1 = find_Sday(today= comp_today1, start_date=start_date, datebox=datebox)
        cal_img[1].click()
        comp_today2 = find_Eday(today=comp_today2, end_date=end_date, datebox=datebox)

        search_btn = browser.find_element_by_class_name("btn")
        search_btn.click()

        section_pdt = browser.find_element_by_class_name("tab_container")
        section_pdt.find_element_by_tag_name("img").click()

        num_check = path_check(ch_file, num_check)      # 다운로드가 수행되었는지 확인하는 부분.

    files_rename("C:/data/download", 'AssKeywdList',search_key, start_date, end_date)       #파일의 이름을 바꾸는 부분.

    time.sleep(5)   # 5초뒤 종료


# 파일경로에 파일이 존재하는지 확인하고 num_check(몇 개나 받았는지 확인) 변수를 return합니다.
def path_check(ch_file, num_check):
    if num_check != 0:
        while not os.path.exists("C:/data/download/AssKeywdList_" + ch_file + str(datetime.today().day) + ' (' + str(num_check) + ').xls'):
            time.sleep(1)
        num_check = num_check + 1
    else:
        while not os.path.exists("C:/data/download/AssKeywdList_" + ch_file + str(datetime.today().day) + '.xls'):
            time.sleep(1)
        num_check = num_check + 1

    return num_check

# 파일의 이름을 기업명(검색어)로 변경합니다.
def files_rename(path, b_name, a_name_str, start_date, end_date):
    files = os.listdir(path)

    name = files[-1]
    newname = a_name_str[0] + "_" + start_date + '_' + end_date + '.xls'
    os.rename(path + '/' + name, path + '/' + newname)

    for i in range(1, len(files), 1):
        name = files[i - 1]
        newname = a_name_str[i] + "_" + start_date + '_' + end_date + '.xls'
        os.rename(path + '/' + name, path + '/' + newname)