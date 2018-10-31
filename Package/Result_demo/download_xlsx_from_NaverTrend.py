import os
import time
from sys import exit
from selenium import webdriver   # 웹 애플리케이션의 테스트를 자동화하기 위한 프레임 워크
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    if not os.path.exists(download_path + '/' + ch_file + '_' + start_date + '_' + end_date + '.xlsx'):
        os.rename(download_path + '/' + added_name, download_path + '/' + ch_file + '_' + start_date + '_' + end_date + '.xlsx')

    return num_check

def wait_until_download(download_path, file_name):
    if os.path.exists(download_path + '/' + file_name + '.xlsx') == False:
        time.sleep(3)
        wait_until_download(download_path, file_name)

def new_path_check(download_path, file_front_str, file_last_str, search_key, start_date, end_date):
    if os.path.exists(download_path + '/' + file_front_str + file_last_str + '.xlsx'):
        print("download check")
        new_rename(download_path, file_front_str, file_last_str, search_key, start_date, end_date)
    else:
        time.sleep(2)
        new_path_check(download_path, file_front_str, file_last_str, search_key, start_date, end_date)

def new_rename(download_path, file_front_str, file_last_str, search_key, start_date, end_date):
    new_name = search_key + '_' + start_date + '_' + end_date + '.xlsx'
    if (os.path.exists(download_path + '/' + new_name) == False) and (os.path.exists(download_path + '/' + file_front_str + file_last_str + '.xlsx') == True):
        os.rename(download_path + '/' + file_front_str + file_last_str + '.xlsx', download_path + '/' + new_name)
    else:       # 파일이 이미 존재한다면, 원본파일을 삭제
        os.remove(download_path + '/' + file_front_str + file_last_str + '.xlsx')

def new_refresh(browser, search):
    try:
        print("try refresh")
        time.sleep(5)
        print("navertrend_refresh")
        browser.refresh()
        browser.find_element_by_id('item_keyword1').clear()
        browser.find_element_by_id('item_sub_keyword1_1').clear()
        browser.find_element_by_id('item_keyword1').send_keys(search)
    except:
        if browser.current_url == 'https://stopit':
            time.sleep(18000)           # ip차단시에는 3시간 뒤 다시 시도
        print("except")
        new_refresh(browser=browser, search=search)

def new_downloading(browser, download_path, file_front_str, file_last_str):
    try:
        time.sleep(2)
        print("try downloading")
        browser.find_element_by_xpath("//a[@class='sp_btn_file_down']").click()
        time.sleep(3)
        for i in range(0, 10, 1):           # 10초까지 다운로드를 기다립니다.
            if os.path.exists(download_path + '/' + file_front_str + file_last_str + '.xlsx'):
                return True
            time.sleep(1)
        new_downloading(browser, download_path, file_front_str, file_last_str)
    except:
        browser.refresh()
        time.sleep(3)
        WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located)  # 브라우저가 로딩하기를 기다림.
        print("except in NaverTrend download")

        if browser.current_url == 'https://stopit':
            time.sleep(18000)           # ip차단시에는 3시간 뒤 다시 시도

        new_downloading(browser, download_path, file_front_str, file_last_str)


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

def connect_to_page(browser, page):
    try:
        browser.get(page)
    except:
        time.sleep(15000)
        connect_to_page(browser, page)

def download_xlsx(search_words, start_date = "2016-01-01",
                  end_date = 0,
                  download_path = 'C:\data\download_from_NaverTrend', chrome_path = 'c:\\data\\chromedriver.exe'):
    dir_path_check(download_path)

    if end_date == 0 :
        if datetime.today().month >= 10 :
            end_date = str(datetime.today().year) + '-' + str(datetime.today().month)
        elif datetime.today().month < 10 :
            end_date = str(datetime.today().year) + '-' + '0' + str(datetime.today().month)

        if datetime.today().day >=10 :
            end_date = end_date + '-' + str(datetime.today().day)
        elif datetime.today().day < 10 :
            end_date = end_date + '-' + '0' + str(datetime.today().day)

    ### 옵션설정 ###
    # 크롬 드라이버에서 adobe flash를 사용하는 것과 다운로드 경로를 설정합니다.
    prefs = {
        "profile.default_content_setting_values.plugins": 1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        "PluginsAllowedForUrls": "https://datalab.naver.com/",
        # user-agent를 추가하여 네이버에서 사용자가 아님을 알아채 막지않도록 합니다.
        "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "lang":"ko_KR",
        "download.default_directory": download_path  # 이 부분에서 다운로드 경로를 설정합니다.
    }
    ### 옵션설정 ###
    page = 'https://datalab.naver.com/'  # page 변수 절대 수정하지 마세요.

    chrome_options = webdriver.ChromeOptions()  # adobe flash player를 사용하기 위한 옵션설정을 하는데 사용합니다.

    chrome_options.add_argument("disable-gpu")
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

    browser.get('about:blank')
    browser.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
    browser.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    browser.execute_script(
        "const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
    WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located)  # 브라우저가 로딩하기를 기다림.  # 브라우저 로드를 기다립니다.-----

    connect_to_page(browser, page)          # 페이지로 연결을 시도하고 만약 차단 당했을 시에는 2시간 30분 뒤 다시 시도하도록 하였습니다.

    # 검색어와 지정한 날짜를 브라우저에 전달하고 결과를 다운받는 반복문
    for i in range(0, len(search_words), 1):
        try:            # 키워드를 브라우저에 전달합니다.
            browser.find_element_by_id('item_keyword1').clear()
            browser.find_element_by_id('item_sub_keyword1_1').clear()
            browser.find_element_by_id('item_keyword1').send_keys(search_words[i])
            time.sleep(3)
        except:         # 만약 에러가 발생할 시에는 브라우저를 새로고침하고 다시 키워드를 전달합니다.
            time.sleep(3)
            new_refresh(browser=browser, search=search_words[i])

        # 첫 검색에서 기간을 지정하면 이후로는 같은 기간이 적용되어 지정하지 않아도 괜찮다.
        if i == 0:
            set_date(browser=browser, start_date=start_date, end_date=end_date)

        browser.find_element_by_xpath("//span[@class='text']").click()
        WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located)  # 브라우저가 로딩하기를 기다림.

        # 2018 10 25 네이버 트렌드에서 이 부분이 계속 오류남. 위 코드로 수정하였음.

        new_downloading(browser=browser, download_path=download_path, file_front_str='data', file_last_str='lab')

        WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located)  # 브라우저가 로딩하기를 기다림.
        #new_path_check(download_path, file_front_str, file_last_str, search_key, start_date, end_date)
        new_path_check(download_path=download_path, file_front_str='data', file_last_str='lab',
                       search_key=search_words[i], start_date=start_date, end_date=end_date)        # 2018 10 22 수정 새로운 체크함수
        #num_check = path_check(ch_file=search_words[i], num_check=num_check, download_path=download_path, added_name='datalab.xlsx',
        #                       start_date=start_date, end_date=end_date)       # 2018 10 22 수정. 새로운 파일체크 함수를 사용
        time.sleep(3)
    browser.close()

if __name__ == '__main__':
    download_xlsx(search_words=['철도', '푸른기술', '한라'], download_path='C:\data\download_from_NaverTrend_reTest')