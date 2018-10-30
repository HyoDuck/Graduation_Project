from PyQt5.QtWidgets import *
from tkinter import *
import return_without_download
import download_xlsx_from_NaverTrend
import v_test
import Get_keywords

class MyWindow(QWidget):
    start_date = ''         # 시작일
    end_date = ''           # 마감일
    navertrend_path = ''    # 네이버 트렌드를 다운받을 경로
    stock_price_xlsx_path = ''          # 네이버에서 받아온 종가엑셀
    xlsx_path = ''              # 상관관계 엑셀(corr.xlsx)
    default_path = 'C:/data/Keywords'       # 키워드 추출에 사용할 기본적인 디렉토리
    max_min = 1.5           # 클러스터링 계수
    use_navertrend = False
    search_words = ['다국적기업', '유신', '구국의결단']
    NaverTrend_path = 'C:/data'

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 500, 300) #윈도우 타이틀 창의 크기를 조절합니다.

        label2 = QLabel("시작날짜: ")
        self.spinBox1 = QSpinBox()  #시작날짜의 '년도'를 설정할 수 있습니다. QSpinBox위젯을 사용했습니다.
        self.spinBox1.setValue(0)  #시작년도의 초기값은 두자리수가 한계이므로 임의로 2018로 입력하면 됩니다.
        self.spinBox1.setMaximum(3000) #표기할 수 있는 최대값을 나타냅니다.
        label3 = QLabel("년 ")
        self.spinBox2 = QSpinBox()  #시작날짜의 '월'을 바인딩합니다.
        self.spinBox2.setValue(1)  #시작 달의 초기값 설정입니다.
        self.spinBox2.setMinimum(1)  #시작 달의 최소값입니다.
        self.spinBox2.setMaximum(12)  #시작 달의 최대값입니다.
        label4 = QLabel("월 ")
        self.spinBox3 = QSpinBox()  #시작날짜의 '일'을 바인딩합니다.
        self.spinBox3.setValue(1)  #시작일의 초기값입니다.
        self.spinBox3.setMinimum(1)  #시작일의 최소값입니다.
        self.spinBox3.setMaximum(31)  #시작일의 최대값입니다.
        label5 = QLabel("일")

        label6 = QLabel("마지막날짜: ")
        self.spinBox4 = QSpinBox()  #마지막날짜의 '넌도'를 바인딩합니다.
        self.spinBox4.setValue(0)
        self.spinBox4.setMaximum(3000)
        label7 = QLabel("년 ")
        self.spinBox5 = QSpinBox()  #마지막날짜의 '월'을 바인딩합니다.
        self.spinBox5.setValue(1)
        self.spinBox5.setMinimum(1)
        self.spinBox5.setMaximum(12)
        label8 = QLabel("월 ")
        self.spinBox6 = QSpinBox()  #마지막날짜의 '일'를 바인딩합니다.
        self.spinBox6.setValue(1)
        self.spinBox6.setMinimum(1)
        self.spinBox6.setMaximum(31)
        label9 = QLabel("일")

        self.checkBox1 = QCheckBox(" Disable NaverTrend download ")
        self.checkBox1.stateChanged.connect(self.checkBox_state_navertrend)
        self.checkBox1.click()

        pushButton1 = QPushButton("설정 저장")
        pushButton1.clicked.connect(self.pushButton_setting)

        pushButton2 = QPushButton("시작")
        pushButton2.clicked.connect(self.pushButton_start)

        pushButton3 = QPushButton("자료 받아오기")
        pushButton3.clicked.connect(self.button_download)

        pushButton4 = QPushButton("상관관계를 이용한 연관도 측정 파트")
        pushButton4.clicked.connect(self.pushButton_make_corr_xlsx)

        pushButton5 = QPushButton("클러스터링 파트")
        pushButton5.clicked.connect(self.pushButton_clustering)

        pushButton6 = QPushButton(" 시각화(종가분석)")
        pushButton6.clicked.connect(self.pushButton_draw_graph1)

        pushButton7 = QPushButton(" 키워드 다운로드(social matrix) ")
        pushButton7.clicked.connect(self.pushButon_keywords1)

        pushButton8 = QPushButton(" 키워드 추출결과 엑셀파일 만들기(NaverTrend 활용) ")
        pushButton8.clicked.connect(self.pushButton_NaverTrend)

        pushButton9 = QPushButton(" 키워드 추출결과 엑셀파일 만들기(NaverTrend 활용X) ")
        pushButton9.clicked.connect(self.pushButton_make_keywords_xlsx)

        pushButton10 = QPushButton(" 시각화(종가분석 + 키워드추출) ")
        pushButton10.clicked.connect(self.pushButton_draw_graph2)

        pushButton_upper1 = QPushButton("종가엑셀 경로")
        pushButton_upper1.clicked.connect(self.pushButton_save_stock_price_path)
        self.label_with_upper1 = QLabel()

        pushButton_upper2 = QPushButton("상관관계 엑셀 경로")
        pushButton_upper2.clicked.connect(self.pushButton_save_xlsx_path)  # 상관관계 엑셀의 경로를 설정하는 버튼
        self.label_with_upper2 = QLabel()

        pushButton_upper3 = QPushButton("키워드 분석 경로")
        pushButton_upper3.clicked.connect(self.pushButton_save_default_path)       # 키워드 분석에 사용될 기본경로를 설정하는 버튼
        self.label_with_upper3 = QLabel()


        #레이아웃을 설정합니다.
        firstLayOut = QVBoxLayout()
        firstLayOut.addWidget(pushButton_upper1)
        firstLayOut.addWidget(self.label_with_upper1)
        firstLayOut.addWidget(pushButton_upper2)
        firstLayOut.addWidget(self.label_with_upper2)
        firstLayOut.addWidget(pushButton_upper3)
        firstLayOut.addWidget(self.label_with_upper3)

        #숫자는 레이아웃의 좌표입니다.
        secondLayOut = QGridLayout()
        secondLayOut.addWidget(label2, 1, 0)
        secondLayOut.addWidget(self.spinBox1, 1, 1)
        secondLayOut.addWidget(label3, 1, 2)
        secondLayOut.addWidget(self.spinBox2, 1, 3)
        secondLayOut.addWidget(label4, 1, 4)
        secondLayOut.addWidget(self.spinBox3, 1, 5)
        secondLayOut.addWidget(label5, 1, 6)
        secondLayOut.addWidget(label6, 2, 0)
        secondLayOut.addWidget(self.spinBox4, 2, 1)
        secondLayOut.addWidget(label7, 2, 2)
        secondLayOut.addWidget(self.spinBox5, 2, 3)
        secondLayOut.addWidget(label8, 2, 4)
        secondLayOut.addWidget(self.spinBox6, 2, 5)
        secondLayOut.addWidget(label9, 2, 6)

        thirdLayOut = QHBoxLayout()
        thirdLayOut.addWidget(pushButton1)
        thirdLayOut.addWidget(pushButton2)
        thirdLayOut.addWidget(pushButton3)

        FourthLayOut = QVBoxLayout()
        FourthLayOut.addWidget(pushButton4)
        FourthLayOut.addWidget(pushButton5)
        FourthLayOut.addWidget(pushButton6)

        LayOut5 = QVBoxLayout()
        LayOut5.addWidget(pushButton7)
        LayOut5.addWidget(pushButton8)
        LayOut5.addWidget(pushButton9)
        LayOut5.addWidget(pushButton10)

        layout = QVBoxLayout()
        layout.addLayout(firstLayOut)
        layout.addLayout(secondLayOut)
        layout.addLayout(thirdLayOut)
        layout.addLayout(FourthLayOut)
        layout.addLayout(LayOut5)

        self.setLayout(layout)

    def pushButton_keywords(self):
        print("키워드 추출 파트")

    # 종가 엑셀의 경로를 지정하는 함수
    def pushButton_save_stock_price_path(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label_with_upper1.setText(fname[0])
        self.stock_price_xlsx_path = self.label_with_upper1.text()

    # 상관관계 엑셀의 경로를 지정하는 함수
    def pushButton_save_xlsx_path(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label_with_upper2.setText(fname[0])
        self.xlsx_path = self.label_with_upper2.text()

    # 키워드 추출에 사용할 경로를 지정할 함수
    def pushButton_save_default_path(self):
        fname = QFileDialog.getExistingDirectory()
        self.label_with_upper3.setText(fname)
        self.default_path = self.label_with_upper3.text()

    def checkBox_state_navertrend(self):
        if self.checkBox1.isChecked():
            self.use_navertrend = False
        else:
            self.use_navertrend = True

    def button_download(self):
        print("download")

    # 시작일과 종료일을 저장합니다.
    def pushButton_setting(self):
        # instance 초기화
        if self.spinBox2.value() < 10:          # 시작 월 설정
            start_month_set = '0' + str(self.spinBox2.value())
        else:
            start_month_set = str(self.spinBox2.value())

        if self.spinBox5.value() < 10:          # 시작 일 설정
            end_month_set = '0' + str(self.spinBox5.value())
        else:
            end_month_set = str(self.spinBox5.value())

        if self.spinBox3.value() < 10:          # 마감 월 설정
            start_day_set = '0' + str(self.spinBox3.value())
        else:
            start_day_set = str(self.spinBox3.value())

        if self.spinBox6.value() < 10:          # 마감 일 설정
            end_day_set = '0' + str(self.spinBox6.value())
        else:
            end_day_set = str(self.spinBox6.value())


        self.start_date = str(self.spinBox1.value()) + '.' + start_month_set + '.' + start_day_set
        self.end_date = str(self.spinBox4.value()) + '.' + end_month_set + '.' + end_day_set
        
        # 인자들을 확인하는 용도의 출력문
        print(self.start_date)
        print(self.end_date)
        print(self.stock_price_xlsx_path)
        print(self.xlsx_path)
        print(self.default_path)

    def pushButton_start(self):
        print("시작")

    def pushButton_draw_graph1(self):       # 키워드 없이 그리기
        print("graph1")
        v_test.visualization(start=self.start_date, end=self.end_date, mat=self.xlsx_path, all_stock_xlsx_path=self.stock_price_xlsx_path)

    def pushButton_draw_graph2(self):       # 키워드를 포함하여 그리기
        print("graph2")

    def pushButton_make_corr_xlsx(self):       # 상관관계 엑셀파일을 생성하는 함수
        print("make corr")
        v_test.corr(excel=self.stock_price_xlsx_path, start=self.start_date, end=self.end_date)

    def pushButton_clustering(self):        # 클러스터링만 진행하는 함수
        print("clustering")
        v_test.clustering(excel=self.xlsx_path)

    def pushButon_keywords1(self):      # 소셜매트릭스 다운로드
        print("social matrix")
        Get_keywords.Keywords_academy_only_ver(start_date=self.start_date, end_date=self.end_date, excel_path=self.xlsx_path, max_min=1.5)

    def pushButton_NaverTrend(self):    # 네이버 트렌드 다운로드를 이용하여 소셜매트릭스에서 가져온 키워드들을 추출합니다.
        print("NaverTrend")
        return_without_download.make_without_download(default_path=self.default_path,
                                                      start_date=self.start_date, end_date=self.end_date,
                                                      use_navertrend=True)

    # 다운로드 없이 디렉토리 안에 있는 소셜매트릭스와 네이버 트렌드 xlsx로 키워드 엑셀을 저장합니다.
    def pushButton_make_keywords_xlsx(self):
        print("keywords_xlsx")
        return_without_download.make_without_download(default_path=self.default_path,
                                                      start_date=self.start_date, end_date=self.end_date,
                                                      use_navertrend=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
