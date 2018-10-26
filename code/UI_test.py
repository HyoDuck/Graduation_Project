import sys
from PyQt5.QtWidgets import *
from tkinter import *
import tkinter.filedialog
import v_test


class MyWindow(QWidget):
    start_date = ''
    end_date = ''
    xlsx_path = 'C:/data'
    max_min = 1.5

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 500, 300) #윈도우 타이틀 창의 크기를 조절합니다.

        label1 = QLabel("시장 선택")  #'시장선택'이라는 텍스트를 보여주는 QLabel위젯입니다.
        radio1 = QRadioButton("KOSPI")  #KOPI 옵션을 선택하는 QRadioButton위젯입니다.
        radio2 = QRadioButton("KOSDAQ")
        radio3 = QRadioButton("KOSPI, KOSDAQ")

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

        checkBox1 = QCheckBox("ETF, ETN 포함하여 분석")  #ETF, ETN 체크박스입니다. QCheckBox위젯을 사용했습니다.
        pushButton1 = QPushButton("설정 저장")
        pushButton1.clicked.connect(self.pushButton_setting)
        pushButton2 = QPushButton("시작")
        pushButton2.clicked.connect(self.pushButton_start)
        pushButton3 = QPushButton("불러오기")

        pushButton3.clicked.connect(self.button_test)
        pushButton4 = QPushButton("자료 업데이트")
        pushButton5 = QPushButton("기타 기능")
        pushButton6 = QPushButton("파일경로 설정")
        pushButton6.clicked.connect(self.pushButtonClicked)  #클릭시 연결할 함수명을 괄호안에 입력합니다.

        self.label10 = QLabel()

        #레이아웃을 설정합니다.
        firstLayOut = QVBoxLayout()
        firstLayOut.addWidget(label1)
        firstLayOut.addWidget(radio1)
        firstLayOut.addWidget(radio2)
        firstLayOut.addWidget(radio3)

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
        thirdLayOut.addWidget(checkBox1)
        thirdLayOut.addWidget(pushButton1)
        thirdLayOut.addWidget(pushButton2)
        thirdLayOut.addWidget(pushButton3)

        FourthLayOut = QVBoxLayout()
        FourthLayOut.addWidget(pushButton4)
        FourthLayOut.addWidget(pushButton5)
        FourthLayOut.addWidget(pushButton6)
        FourthLayOut.addWidget(self.label10)

        layout = QVBoxLayout()
        layout.addLayout(firstLayOut)
        layout.addLayout(secondLayOut)
        layout.addLayout(thirdLayOut)
        layout.addLayout(FourthLayOut)

        self.setLayout(layout)

    #파일 경로를 지정해 주는 함수입니다.
    def pushButtonClicked(self):
        root = Tk().withdraw()
        title = 'Save project as'
        ftypes = [('xlsx file', '.xlsx'), ('All files', '*')]
        filename = tkinter.filedialog.asksaveasfilename(filetypes=ftypes, title=title, initialfile='')
        self.label10.setText(filename)

    def button_test(self):
        #v_test.test()
        print("불러오기 기능")

    def pushButton_setting(self):
        # instance 초기화
        if self.spinBox2.value() < 10:          # 월 설정
            start_month_set = '0' + str(self.spinBox2.value())
        else:
            start_month_set = str(self.spinBox2.value())

        if self.spinBox5.value() < 10:
            end_month_set = '0' + str(self.spinBox5.value())
        else:
            end_month_set = str(self.spinBox5.value())

        if self.spinBox3.value() < 10:
            start_day_set = '0' + str(self.spinBox3.value())
        else:
            start_day_set = str(self.spinBox3.value())

        if self.spinBox6.value() < 10:
            end_day_set = '0' + str(self.spinBox6.value())
        else:
            end_day_set = str(self.spinBox6.value())


        self.start_date = str(self.spinBox1.value()) + '.' + start_month_set + '.' + start_day_set
        self.end_date = str(self.spinBox4.value()) + '.' + end_month_set + '.' + end_day_set

        self.xlsx_path = self.label10.text()
        
        # 인자들을 확인하는 용도의 출력문
        print(self.start_date)
        print(self.end_date)
        print(self.xlsx_path)

    def pushButton_start(self):
        v_test.graph_test(self.start_date, self.end_date, '', self.xlsx_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()

