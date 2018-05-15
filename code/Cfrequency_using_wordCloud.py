import matplotlib.pyplot as plt
from os import path
from wordcloud import WordCloud, STOPWORDS
from konlpy.tag import Kkma

kkma = Kkma()

# txt_path는 txt파일이 있는 폴더명
# file_name은 txt파일명입니다.
def word_cld(txt_path, file_name) :
    d = path.dirname(txt_path)  # 텍스트 파일이 있는 상위 디렉토리를 path로 지정
    text = open(path.join(d, txt_path + "\\" + file_name), mode="r",encoding="euc-kr")  # 읽기모드로 test.txt 파일을 불러옴

    text = text.read()
    text = kkma.nouns(str(text))
    temp = ''
    for i in range(0, len(text), 1):
        temp = temp + " " + str(text[i])
    text = temp

    wordcloud = WordCloud(font_path='C://Windows//Fonts//YTTE08.TTF',  # 폰트를 YTTE08.TTF 로 지정
                        stopwords=STOPWORDS, background_color='white',  # STOPWORDS ==> 공백 or 개행으로 문자를 구분
                        width=1000,  # background_color ==> 배경색을 흰색으로 지정
                        height=800,  # width, height 높이와 너비를 지정
                        colormap='PuRd').generate(text)
                        # colormap ==> 글자색을 지정
                        # generate() ==> 워드 클라우드 실행

    plt.figure(figsize=(13, 13))  # matplotlib의 pyplot을 figsize로 생성
    plt.imshow(wordcloud)  #이미지를 pyplot에 띄움
    plt.axis("off")  # pyplot에 x, y축을 표시하지 않도록 한다.
    plt.show()  # 워드 클라우드를 출력한다.

if __name__ == '__main__':
    word_cld("C:\\data\\StockInfo\\news\\konlpy_test", "txt_file.txt")