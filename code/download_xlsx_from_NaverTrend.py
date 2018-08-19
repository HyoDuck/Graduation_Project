# writer : 김효빈
# upload date : 2018-08-19
# https://datalab.naver.com/ 에서 검색어 트래픽을 확인하고 xlsx 파일을 다운받습니다.
#
# download_xlsx(search_words, start_date = "2016-01-01",
#                  end_date = str(datetime.today().year) + '-' + str(datetime.today().month) + '-' + str(datetime.today().day),
#                  download_path = 'C:\data\download_from_NaverTrend', chrome_path = 'c:\\data\\chromedriver.exe')
# 전달인자
# search_words 검색하고자 하는 리스트
# start_date, end_date 시작일과 마감일 // 디폴트값은 2016-01-01 부터 ~ 현재까지 입니다.
# download_path 다운로드 경로 // 기본경로는 C:\data\download_from_NaverTrend 입니다.
# download_path 에 전달한 경로가 존재하지 않는다면 하위 디렉토리부터 하나씩 생성합니다.
# chrome_path 크롬드라이버가 위치한 경로입니다. // 기본경로는 c:\\data\\chromedriver.exe입니다.


import os
import time
from selenium import webdriver   # 웹 애플리케이션의 테스트를 자동화하기 위한 프레임 워크
from datetime import datetime

# 사용자가 경로를 입력하면 하위경로부터 시작해 폴더가 존재하는지 확인하고
# 폴더가 존재하지 않는다면 생성합니다.
def dir_path_check(dir_path):
    for i in range(0, len(dir_path) -1, 1):
        if dir_path[i] == '/' and dir_path[i-1] != ':':
            dir_name = dir_path[:i]
            if not os.path.isdir(dir_name):
                os.mkdir(dir_name)

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

# 파일경로에 파일이 존재하는지 확인하고 num_check(몇 개나 받았는지 확인) 변수를 return합니다.
# 파일명을 '검색어_시작일_마감일.xlsx로 변경합니다.
def path_check(ch_file, num_check, download_path, added_name, start_date, end_date):
    while not os.path.exists(download_path + '/' + added_name):
        time.sleep(1)
    num_check = num_check + 1

    if not os.path.exists(download_path + '/' + ch_file + '.xlsx'):
        os.rename(download_path + '/' + added_name, download_path + '/' + ch_file + '_' + start_date + '_' + end_date + '.xlsx')

    return num_check

# 시작일과 마지막일을 지정하는 함수
def set_date(browser, start_date, end_date):
    # 시작일을 지정하는 부분
    # 2016년 ~~ 선택
    browser.find_element_by_id('startYear').click()
    year_selector = browser.find_element_by_id('startYearDiv')
    year_selector = year_selector.find_elements_by_class_name('option')

    for num in range(0, len(year_selector), 1):
        if year_selector[num].text == start_date[:4]:
            year_selector[num].click()

    # 1월 ~ 12월 선택
    browser.find_element_by_xpath("//a[@id='startMonth']").click()
    month_selector = browser.find_element_by_id('startMonthDiv')
    month_selector = month_selector.find_elements_by_class_name('option')

    for num in range(0, len(month_selector), 1):
        if month_selector[num].text == start_date[5:7]:
            month_selector[num].click()

    # 일 선택
    browser.find_element_by_xpath("//a[@id='startDay']").click()
    day_selector = browser.find_element_by_id('startDayDiv')
    day_selector = day_selector.find_elements_by_class_name('option')

    for num in range(0, len(day_selector), 1):
        if day_selector[num].text == start_date[8:]:
            day_selector[num].click()

    # 마감일을 지정한다.
    # 2016년 ~~ 선택
    browser.find_element_by_xpath("//a[@id='endYear']").click()
    year_selector = browser.find_element_by_id('endYearDiv')
    year_selector = year_selector.find_elements_by_class_name('option')

    for num in range(0, len(year_selector), 1):
        if year_selector[num].text == end_date[:4]:
            year_selector[num].click()

    # 1월 ~ 12월 선택
    browser.find_element_by_xpath("//a[@id='endMonth']").click()
    month_selector = browser.find_element_by_id('endMonthDiv')
    month_selector = month_selector.find_elements_by_class_name('option')

    for num in range(0, len(month_selector), 1):
        if month_selector[num].text == end_date[5:7]:
            month_selector[num].click()

    # 일 선택
    browser.find_element_by_xpath("//a[@id='endDay']").click()
    day_selector = browser.find_element_by_id('endDayDiv')
    day_selector = day_selector.find_elements_by_class_name('option')

    for num in range(0, len(day_selector), 1):
        if day_selector[num].text == end_date[8:]:
            day_selector[num].click()

def download_xlsx(search_words, start_date = "2016-01-01",
                  end_date = str(datetime.today().year) + '-' + str(datetime.today().month) + '-' + str(datetime.today().day),
                  download_path = 'C:\data\download_from_NaverTrend', chrome_path = 'c:\\data\\chromedriver.exe'):
    dir_path_check(download_path)
    num_check = 0
    ### 옵션설정 ###
    # 크롬 드라이버에서 adobe flash를 사용하는 것과 다운로드 경로를 설정합니다.
    prefs = {
        "profile.default_content_setting_values.plugins": 1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        "PluginsAllowedForUrls": "https://datalab.naver.com/",
        "download.default_directory": download_path  # 이 부분에서 다운로드 경로를 설정합니다.
    }
    ### 옵션설정 ###
    page = 'https://datalab.naver.com/'  # page 변수 절대 수정하지 마세요.

    chrome_options = webdriver.ChromeOptions()  # adobe flash player를 사용하기 위한 옵션설정을 하는데 사용합니다.
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

    browser.implicitly_wait(3)  # 브라우저 로드를 기다립니다.-----

    browser.get(page)

    # 검색어와 지정한 날짜를 브라우저에 전달하고 결과를 다운받는 반복문
    for i in range(0, len(search_words), 1):
        browser.find_element_by_id('item_keyword1').clear()
        browser.find_element_by_id('item_sub_keyword1_1').clear()
        browser.find_element_by_id('item_keyword1').send_keys(search_words[i])

        # 첫 검색에서 기간을 지정하면 이후로는 같은 기간이 적용되어 지정하지 않아도 괜찮다.
        if i == 0:
            set_date(browser=browser, start_date=start_date, end_date=end_date)

        browser.find_element_by_xpath("//span[@class='text']").click()

        browser.implicitly_wait(3)

        while(1):
            try:
                browser.find_element_by_xpath("//a[@class='sp_btn_file_down']").click()
                break
            except:
                time.sleep(1)
                continue

        time.sleep(1)

        num_check = path_check(ch_file=search_words[i], num_check=num_check, download_path=download_path, added_name='datalab.xlsx',
                               start_date=start_date, end_date=end_date)



