2018 12 03
키워드추출에 관한 부분을 정리하여 둔 폴더입니다.

1. Start_with_this.py
- input : 시작일, 마감일, 상관관계 계수 excel파일, 관계수치, 네이버 트렌드 사용유무
- output : (그룹, 키워드) 형태의 list

2. Get_keywords.py
- input : 시작일, 마감일, 상관관계 계수 excel파일, 관계수치
- output : 그룹의 키워드 excel파일, NaverTrend에서 다운받은 excel파일
- http://academy.some.co.kr/login.html ==> 검색어와 함께 등장한 단어들을 모아 정리된 excel파일을 다운받음.
- https://datalab.naver.com/ ==> 검색어의 트래픽을 excel파일 형태로 제공해줌.

3. get_keywords_from_academy_re.py
- input : 시작일, 마감일, 검색어 list, ID, password, download path, chrome driver
- output : 검색어 list의 excel 파일들을 download path에 저장

4. get_stock_title.py
- 기업명을 naver.finance에서 다운받아 stock_title.xlsx로 저장합니다.

5. download_xlsx_from_NaverTrend.py
- input : 검색어 list, download path
- output : download path에 NaverTrend에서 받은 검색어 트래픽 excel파일을 저장합니다.

6. comp_NaverTrend_xls.py
- input : NaverTrend에서 받은 excel경로
- output : 해당 폴더안에 있는 data의 트래픽이 얼마나 급격하게 증가하였는지 측정한 수치
(각 점에서부터 최고점으로 향하는 기울기를 이용하여 구합니다.)

7. make_comp_list.py
- 그룹으로 묶인 기업들과 비교대조군을 만드는데 사용하는 코드를 가지고 있는 .py파일

8. comp_text.py
- 이전에 http://academy.some.co.kr 에서 수집한 키워드들을 워드파일 형태로 저장하였는데,
- 여기서 연관이 있다고 볼만한 단어들만을 뽑아내는 함수입니다. (상위 n%만을 가져옵니다.)

9. remove_useless_words
- 결과 키워드 list에서 기업명과 일치하는 단어들을 제거합니다.
