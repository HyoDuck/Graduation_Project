# writer : 김효빈
# upload date : 2018-08-18
# 이전에 http://academy.some.co.kr 에서 수집한 키워드들을 워드파일 형태로 저장하였는데,
# 여기서 연관이 있다고 볼만한 단어들만을 뽑아내는 함수입니다.
# extract_keyword(dir_path, return_num = 3) 을 호출하여 사용하면 됩니다.
# dir_path는 워드파일들이 위치한 디렉토리이고, return_num은 각각의 항목당 상위 몇 개까지의 단어들만을 뽑아낼 것인지 지정하는 인자입니다.

import xlrd
import pathlib
import os
from operator import eq


# 검색어 리스트와 count수 리스트를 전달하면 ...
# [키워드, 검색에서 노출된 횟수, 총 count수] n개를 2차원 리스트형태로 반환한다.
def cprs_list(keywords_list, frq_list):
    app_check = 1  # 검색에서 노출된 횟수

    result = []  # return하는데 쓰일 result 리스트

    i = 0
    while (1):
        if len(keywords_list) - 1 == i:
            break
        j = i + 1
        try:
            keyword_check = keywords_list[i]  # 검색어
        except IndexError:
            break
        frq_check = frq_list[i]
        while (1):
            if (len(keywords_list) - 1 == j) or (len(keywords_list) == j):
                result.append([keyword_check, app_check, frq_check])
                app_check = 1
                break
            if eq(keyword_check, keywords_list[j]):
                app_check = app_check + 1
                frq_check = frq_check + frq_list[j]
                del keywords_list[j]
                del frq_list[j]
            j = j + 1
        i = i + 1

    return result


# 등장한 빈도수가 높은 키워드만 가져오게한다.
# list의 형태는 2차원 배열로, [ 단어, 등장횟수, count 합계 ]
def compress_keywords_list(keylist, freq_ctr = 0.75):
    file_num = 0
    for i in range(0, len(keylist) - 1, 1):  # file_num ==>> 가장 많이 등장한 단어의 횟수를 찾는다
        if keylist[i][1] > file_num:
            file_num = keylist[i][1]

    result_list = []

    for i in range(0, len(keylist) - 1, 1):  # 검색시75% 이상 노출된 단어만을 뽑아낸다
        if keylist[i][1] / file_num >= freq_ctr:  # 이 부분을 수정하면 됩니다.
            result_list.append(keylist[i])

    for i in range(0, len(result_list) - 1, 1):  # count가 큰 순으로 sorting
        for j in range(i + 1, len(result_list) - 1, 1):
            try:
                if result_list[i][2] < result_list[j][2]:
                    temp = result_list[i]
                    result_list[i] = result_list[j]
                    result_list[j] = temp
            except ValueError as ve:
                print(" empty Value ")
            except TypeError as te:
                print(str(i) + " : " + str(result_list[i][2]))
                print(str(j) + " : " + str(result_list[j][2]))
                print(" Type Error ")

    return result_list


# 파일에 있는 키워드들과 빈도수를 배열로 반환합니다.
# ex) [['문재인', 3, 18.0], ['노무현', 1, 3.0], ['트럼프', 3, 16.0], ['방탄소년단', 2, 17.0], ['유진', 1, 2.0], ['김현구', 1, 2.0], ...]
def read_exl(dir_path):
    filenames = os.listdir(dir_path)
    data_row = 1  # 위에서 아래로 진행

    person_keywords = []
    person_frq = []
    person_result = []

    org_keywords = []
    org_frq = []
    org_result = []

    place_keywords = []
    place_frq = []
    place_result = []

    product_keywords = []
    product_frq = []
    product_result = []

    chr_keywords = []
    chr_frq = []
    chr_result = []

    brand_keywords = []
    brand_frq = []
    brand_result = []

    hobby_keywords = []
    hobby_frq = []
    hobby_result = []

    psycology_keywords = []
    psycology_frq = []
    psycology_result = []

    for filename in filenames:
        while_check = 1  # while 반복문 체크
        data_column = 3  # 단어가 위치한 column
        frq_column = 4  # 단어 빈도수가 위치한 column
        filename = dir_path + '\\' + filename
        wb = xlrd.open_workbook(filename)
        ws1 = wb.sheet_by_index(0)

        # 어떠한 단어가 노출되었는지 가져온다
        while (data_column < 19):  # column은 17까지 있으므로 넘어가면 반복문 중단
            while (while_check):
                if data_column == 3:
                    person_keywords.append(ws1.cell(rowx=data_row, colx=data_column).value)
                    person_frq.append(ws1.cell(rowx=data_row, colx=frq_column).value)
                    data_row = data_row + 1

                elif data_column == 5:
                    org_keywords.append(ws1.cell(rowx=data_row, colx=data_column).value)
                    org_frq.append(ws1.cell(rowx=data_row, colx=frq_column).value)
                    data_row = data_row + 1

                elif data_column == 7:
                    place_keywords.append(ws1.cell(rowx=data_row, colx=data_column).value)
                    place_frq.append(ws1.cell(rowx=data_row, colx=frq_column).value)
                    data_row = data_row + 1

                elif data_column == 9:
                    product_keywords.append(ws1.cell(rowx=data_row, colx=data_column).value)
                    product_frq.append(ws1.cell(rowx=data_row, colx=frq_column).value)
                    data_row = data_row + 1

                elif data_column == 11:
                    chr_keywords.append(ws1.cell(rowx=data_row, colx=data_column).value)
                    chr_frq.append(ws1.cell(rowx=data_row, colx=frq_column).value)
                    data_row = data_row + 1

                elif data_column == 13:
                    brand_keywords.append(ws1.cell(rowx=data_row, colx=data_column).value)
                    brand_frq.append(ws1.cell(rowx=data_row, colx=frq_column).value)
                    data_row = data_row + 1

                elif data_column == 15:
                    hobby_keywords.append(ws1.cell(rowx=data_row, colx=data_column).value)
                    hobby_frq.append(ws1.cell(rowx=data_row, colx=frq_column).value)
                    data_row = data_row + 1

                elif data_column == 17:
                    psycology_keywords.append(ws1.cell(rowx=data_row, colx=data_column).value)
                    psycology_frq.append(ws1.cell(rowx=data_row, colx=frq_column).value)
                    data_row = data_row + 1

                try:
                    if (eq(ws1.cell(rowx=data_row, colx=data_column).value, '')):
                        while_check = 0
                        data_row = 1
                except:
                    while_check = 0
                    data_row = 1

            data_column = data_column + 2
            frq_column = frq_column + 2
            while_check = 1

    # 키워드 리스트를 압축시키는 함수
    person_result = cprs_list(person_keywords, person_frq)
    org_result = cprs_list(org_keywords, org_frq)
    place_result = cprs_list(place_keywords, place_frq)
    product_result = cprs_list(product_keywords, product_frq)
    chr_result = cprs_list(chr_keywords, chr_frq)
    brand_result = cprs_list(brand_keywords, brand_frq)
    hobby_result = cprs_list(hobby_keywords, hobby_frq)
    #psycology_result = cprs_list(psycology_keywords, psycology_frq)

    return person_result, org_result, place_result, product_result, chr_result, brand_result, hobby_result
        #, psycology_result 심리 부분은 큰 의미가 없어 제외하기로 함.

# 2018-10-02 freq_ctr 전달인자 추가 ( 몇 건의 문서에 단어가 등장하는지 체크하는 변수 )
def extract_keyword(dir_path, return_num=5, freq_ctr=0.75):

    person_result, org_result, place_result, product_result, chr_result, brand_result, hobby_result= read_exl(
        dir_path=dir_path)
    # psycology_result는 제외

    person_result = compress_keywords_list(person_result, freq_ctr)
    org_result = compress_keywords_list(org_result, freq_ctr)
    place_result = compress_keywords_list(place_result, freq_ctr)
    chr_result = compress_keywords_list(chr_result, freq_ctr)
    product_result = compress_keywords_list(product_result, freq_ctr)
    brand_result = compress_keywords_list(brand_result, freq_ctr)
    hobby_result = compress_keywords_list(hobby_result, freq_ctr)
    #psycology_result = compress_keywords_list(psycology_result)    #제외함 2018-10-02

    print(person_result[:return_num])
    print(org_result[:return_num])
    print(place_result[:return_num])
    print(chr_result[:return_num])
    print(product_result[:return_num])
    print(brand_result[:return_num])
    print(hobby_result[:return_num])
    #print(psycology_result[:return_num])

    result_test = person_result[:return_num] + org_result[:return_num] + place_result[:return_num] + \
                  product_result[:return_num] + chr_result[:return_num] + brand_result[:return_num] + \
                  hobby_result[:return_num]
                  #+ psycology_result[:return_num]  심리부분 삭제 2018-10-02

    return result_test


if __name__ == '__main__':
    extract_keyword("C:\\data\\download")