from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import  FirefoxBinary
from selenium.webdriver.common.desired_capabilities import  DesiredCapabilities
import time
from selenium.webdriver.common.keys import Keys
import datetime as dt
import pandas as pd

binary=FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe')
browser=webdriver.Firefox(executable_path='C:/Program Files/Mozilla Firefox/geckodriver.exe',firefox_binary=binary)

df = pd.DataFrame(columns=['id','message','created-at','symbol']) # 빈 데이터 프레임 생성

stock = ["현대로템", "현대상사", "대아티아이", "제룡전기", "신원", "신대양제지", "써니전자", "보광산업", "한국선재", "매커스", "두올산업", "풀무원"]  # 주가 종목 입력하면됨
# stock=["현대로템","현대상사"]
totaltweets = []
date = []
name = []
for i in range(len(stock)):
    startdate = dt.date(year=2018, month=6, day=1)  # 시작날짜
    untildate = dt.date(year=2018, month=6, day=2)  # 시작날짜 +1 날짜 입력
    enddate = dt.date(year=2018, month=6, day=30)  # 끝날짜
    while not enddate == startdate:
        url = 'https://twitter.com/search?q=' + stock[i] + '%20since%3A' + str(startdate) + '%20until%3A' + str(
            untildate) + '&amp;amp;amp;amp;amp;amp;lang=eg'

        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        lastHeight = browser.execute_script("return document.body.scrollHeight")
        while True:

            dailyfreq = {'Date': startdate}

            wordfreq = 0
            tweets = soup.find_all("p", {"class": "TweetTextSize"})
            # print(tweets)
            totaltweets.append(tweets)
            for j in range(len(tweets)):
                date.append(startdate)
                name.append(stock[i])
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            newHeight = browser.execute_script("return document.body.scrollHeight")
            # print(newHeight)
            if newHeight != lastHeight:
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                tweets = soup.find_all("p", {"class": "TweetTextSize"})
                wordfreq = len(tweets)
            else:
                dailyfreq['Frequency'] = wordfreq
                wordfreq = 0
                # totalfreq.append(dailyfreq)
                startdate = untildate
                untildate += dt.timedelta(days=1)
                dailyfreq = {}
                break

            lastHeight = newHeight

len(totaltweets)

# 데이터프레임에 내용 적재
number=1
Index=0
for i in range(len(totaltweets)):
    for j in range(len(totaltweets[i])):
        df = df.append({'id': number,'message':(totaltweets[i][j]).text,'created-at':date[Index],'symbol':name[Index]}, ignore_index=True)
        number = number+1
        Index = Index+1

df

df.head() # 5개행만 보기

df.to_excel("E:\\개인분석\\twitter.xlsx",sheet_name='sheet1') # 저장하기


