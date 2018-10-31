import comp_NaverTrend
import comp_text
import download_xlsx_from_NaverTrend
import get_keyword_from_academy_re
import get_stock_title
import remove_useless_words
import datetime
import make_comp_list
import cluster1
import os

def Keywords_academy_only_ver(start_date, end_date, excel_path, max_min,
             chrome_path='c:\\data\\chromedriver.exe',
             default_path = '', academy_xlsx_path='', NaverTrend_path='', array2D_path='',
             stock_title_path=''):
    word_list = cluster1.clustering(excel=excel_path, y=max_min)

    for i in range(0, len(word_list), 1):
        if default_path == '':  # 기본경로를 설정해줍니다.
            default_path = 'C:/data/' + 'Keywords/' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + word_list[i][0] + '_포함_' + str(len(word_list)) + '_종목'

        # 경로설정하는 부분.
        academy_xlsx_path, NaverTrend_path, array2D_path, stock_title_path = path_controller(default_path,
                                                                                             academy_xlsx_path,
                                                                                             NaverTrend_path,
                                                                                             array2D_path,
                                                                                             stock_title_path)

        comp_default_path = default_path + '/' + 'Comp_data'
        comp_academy_path, comp_NaverTrend_path, comp_array2D_path, comp_stock_title_path = path_controller(comp_default_path)

        comp_word_list = make_comp_list.word_list(excel=excel_path, word=word_list[i][0])
        if len(comp_word_list) > 6:  # 대조비교군을 형성할 기업명들을 줄입니다.
            comp_input_list = comp_word_list[:6]
        # 분석하려고 하는 그룹의 데이터를 받아옴
        get_keyword_from_academy_re.download_keywords(start_date=start_date, end_date=end_date, search_key=word_list[i],
                                                    ID='academy', PWD='academy123', download_path=academy_xlsx_path, chrome_path=chrome_path)
        # 비교 대조군을 만들기 위한 데이터를 받아옴
        get_keyword_from_academy_re.download_keywords(start_date=start_date, end_date=end_date, search_key=comp_word_list,
                                                    ID='academy', PWD='academy123', download_path=comp_academy_path, chrome_path=chrome_path)

def Keywords(start_date, end_date, word_list, comp_word_list,
             chrome_path='c:\\data\\chromedriver.exe',
             default_path = '', academy_xlsx_path='', NaverTrend_path='', array2D_path='',
             stock_title_path='', original_stock_title_path='C:/data/Keywords/Stock_title',
             update_stock_title=False, use_navertrend=False):
    if default_path == '':      # 기본경로를 설정해줍니다.
        default_path = 'C:/data/' + 'Keywords/' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + word_list[0] + '_포함_' + str(len(word_list)) + '_종목'

    for path_checker in os.listdir('C:/data/Keywords'):
        if path_checker[19:] == word_list[0] + '_포함_' + str(len(word_list)) + '_종목':
            return False                # 이미 존재하는 자료일 때는 False를 return하여 더 이상 받지 않도록 합니다.

    # 경로설정하는 부분.
    academy_xlsx_path, NaverTrend_path, array2D_path, stock_title_path = path_controller(default_path, academy_xlsx_path, NaverTrend_path, array2D_path, stock_title_path)

    comp_default_path = default_path + '/' + 'Comp_data'
    comp_academy_path, comp_NaverTrend_path, comp_array2D_path, comp_stock_title_path = path_controller(comp_default_path)

    # 분석하려고 하는 그룹의 데이터를 받아옴
    get_keyword_from_academy_re.download_keywords(start_date=start_date, end_date=end_date, search_key=word_list,
                                                  ID='academy', PWD='academy123', download_path=academy_xlsx_path, chrome_path=chrome_path)
    # 비교 대조군을 만들기 위한 데이터를 받아옴
    get_keyword_from_academy_re.download_keywords(start_date=start_date, end_date=end_date, search_key=comp_word_list,
                                                  ID='academy', PWD='academy123', download_path=comp_academy_path, chrome_path=chrome_path)

    compressed_words = comp_text.extract_keyword(dir_path=academy_xlsx_path, return_num=5, freq_ctr=0.0)
    comp_compressed_words = comp_text.extract_keyword(dir_path=comp_academy_path, return_num=100, freq_ctr=0.4)

    compressed_only_words = pinset(compressed_words)
    comp_only_words = pinset(comp_compressed_words)

    print("compressed only words")
    print(compressed_only_words)
    print("comp only words")
    print(comp_only_words)
    print('')

    get_keyword_from_academy_re.dir_path_check(array2D_path)        #2D_array_path check and make directory
    get_keyword_from_academy_re.dir_path_check(comp_array2D_path)
    if update_stock_title:      # 기업명을 네이버에서 새로 받아오도록 하는 설정
        get_stock_title.Make_Stock_title_xlsx(dir_path=stock_title_path)        # 기업명을 네이버에서 모두 가져옴
    else:
        get_stock_title.Copy_Stock_title_xlsx(original_path=original_stock_title_path, copy_path=stock_title_path, file_name='stock_title.xlsx')

    # def Remove_words(stock_title_dir_path, stock_file_name, keywords_dir_path, comp_dir_path,  array2D_xlsx_path, array2D_xlsx_name)
    convert_to_str(compressed_only_words)
    convert_to_str(comp_only_words)

    search_words, removed_words = remove_useless_words.Remove_words(stock_title_dir_path=stock_title_path,
                                                                    stock_file_name='stock_title',
                                                                    keywords=compressed_only_words,
                                                                    comp_list=comp_only_words)
    print(" search_words : ")
    print(search_words)
    print(" removed_words : ")
    print(removed_words)
    if use_navertrend == True:
        download_xlsx_from_NaverTrend.download_xlsx(search_words=search_words, start_date=start_date, end_date=end_date,
                                                    download_path=NaverTrend_path)

        slope_list = comp_NaverTrend.comp_NaverTrend_xls(dir_path=NaverTrend_path, array2D_xlsx_path=array2D_path)
        print("slope_list : ")
        print(slope_list)
        print(slope_list[:(int)(len(slope_list)/2)])
        result = slope_list

        for i in range(0, len(result), 1):      # 뒤에 붙은 slope num을 제거
            result[i] = result[i][0]
    else:
        result = search_words

    return result       # [키워드1, 키워드2 ... ]으로 초기화 되어있는 리스트를 return합니다.

def pinset(compressed_words_list):
    r_list = []
    for i in range(0, len(compressed_words_list), 1):
        if(compressed_words_list[i][0] == ''):
            print(" remove 'NoneType' element ")
        else:
            r_list.append(compressed_words_list[i][0])

    return r_list

def convert_to_str(words_list):         # 리스트에 utf-8로 인코딩된 문자열이 들어있다면 unicode로 변환합니다.
    for i in range(0, len(words_list), 1):
        if isinstance(words_list[i], str) == False:      # 문자열이 unicode인지 판별합니다.
            words_list[i] = words_list[i].decode('utf-8')

def path_controller(default_path = 'C:/data/' + datetime.datetime.now().strftime('%Y-%m-%d'), academy_xlsx_path='', NaverTrend_path='', array2D_path='', stock_title_path=''):
    if academy_xlsx_path == '':
        academy_xlsx_path = default_path + '/' + 'Academy'
    if NaverTrend_path == '':
        NaverTrend_path = default_path + '/' + 'NaverTrend'
    if array2D_path =='':
        array2D_path = default_path + '/' + '2D_array'
    if stock_title_path == '':
        stock_title_path = default_path + '/' + 'Stock_title'

    return academy_xlsx_path, NaverTrend_path, array2D_path, stock_title_path

if __name__ == '__main__':
    #Keywords(start_date='2017-11-01', end_date='2018-06-01', word_list=['광명전기', '마이스터', '선도전기', '우원개발', '현대로템'])

    Keywords_academy_only_ver(start_date='2018-01-01', end_date='2018-09-30', excel_path='C:/data/30x30.xlsx', max_min=1.5)