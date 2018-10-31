import comp_text
import download_xlsx_from_NaverTrend
import comp_NaverTrend
import remove_useless_words
import os
import make_keywords_xlsx
from Get_keywords import pinset
from Get_keywords import convert_to_str

def read_stockname(stock_dir_path):
    file_list = os.listdir(stock_dir_path)
    result_list = []

    for i in range(0, len(file_list), 1):
        j = 0
        while j < len(file_list[i]) :
            if(file_list[i][j] == '_'):
                result_list.append(file_list[i][:j])
                j = len(file_list[i])
            j = j + 1

    return result_list

def make_keywords_list(academy_xlsx_path, comp_academy_path, stock_title_path, NaverTrend_path, array2D_path,
                       start_date, end_date, use_navertrend, use_downloaded_navertrend):
    compressed_words = comp_text.extract_keyword(dir_path=academy_xlsx_path, return_num=5, freq_ctr=0.75)
    comp_compressed_words = comp_text.extract_keyword(dir_path=comp_academy_path, return_num=100, freq_ctr=0.0)

    stock_name_list = read_stockname(academy_xlsx_path)

    compressed_only_words = pinset(compressed_words)
    comp_only_words = pinset(comp_compressed_words)

    print("compressed only words")
    print(compressed_only_words)
    print("comp only words")
    print(comp_only_words)
    print('')

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
    result = []

    if use_navertrend == True:
        download_xlsx_from_NaverTrend.download_xlsx(search_words=search_words, start_date=start_date, end_date=end_date,
                                                    download_path=NaverTrend_path)

        slope_list = comp_NaverTrend.comp_NaverTrend_xls(dir_path=NaverTrend_path, array2D_xlsx_path=array2D_path)
        print("slope_list : ")
        print(slope_list)
        print(slope_list[:(int)(len(slope_list) / 2)])

        for i in range(0, len(slope_list), 1):
            result.append(slope_list[i][0])
    else:
        result = search_words

    if use_downloaded_navertrend == True:
        slope_list = comp_NaverTrend.comp_NaverTrend_xls(dir_path=NaverTrend_path, array2D_xlsx_path=array2D_path)
        print("slope_list : ")
        print(slope_list)
        print(slope_list[:(int)(len(slope_list) / 2)])
        for i in range(0, len(slope_list), 1):
            result.append(slope_list[i][0])

    return stock_name_list, result  # [[키워드1, 검색어 트래픽], [키워드2, 검색어 트래픽] ... ]으로 초기화 되어있는 리스트를 return합니다.

def make_without_download(default_path, start_date, end_date, use_navertrend, use_downloaded_navertrend):
    dir_list = os.listdir(default_path)
    stock_result = []
    key_result = []
    i = 0
    while i < len(dir_list):
        if dir_list[i] == 'Stock_title':
            i = i + 1
            continue
        stock_temp, key_temp = make_keywords_list(academy_xlsx_path=default_path + '/' + dir_list[i] + '/Academy',
                           comp_academy_path=default_path + '/' + dir_list[i] + '/Comp_data/Academy',
                           stock_title_path=default_path + '/stock_title',
                           NaverTrend_path=default_path + '/' + dir_list[i] + '/NaverTrend',
                           array2D_path=default_path + '/' + dir_list[i] + '/2D_array',
                           start_date=start_date, end_date=end_date, use_navertrend=use_navertrend,
                                                  use_downloaded_navertrend=use_downloaded_navertrend)

        stock_result.append(stock_temp)
        key_result.append(key_temp)

        i = i + 1

    make_keywords_xlsx.make_xlsx(stock_list=stock_result, keywords_list=key_result)


if __name__ == '__main__':
    make_without_download(default_path='C:/data/Keywords', start_date='2018-01-01', end_date='2018-10-30', use_navertrend=False, use_downloaded_navertrend=True)