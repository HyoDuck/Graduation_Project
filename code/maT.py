import sys
from PyQt5.QtWidgets import *
import download_stockinfo

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 500, 300)

        label1 = QLabel("시장 선택")
        radio1 = QRadioButton("KOSPI")
        radio2 = QRadioButton("KOSDAK")

        label2 = QLabel("기준 종목명 및 종목코드")
        lineEdit1 = QLineEdit("")
        label3 = QLabel("비교 종목명 및 종목코드")
        lineEdit2 = QLineEdit("")

        label4 = QLabel("시작날짜: ")
        spinBox1 = QSpinBox()
        spinBox1.setValue(2018)
        spinBox1.setMaximum(3000)
        spinBox2 = QSpinBox()
        spinBox2.setValue(1)
        spinBox2.setMinimum(1)
        spinBox2.setMaximum(12)
        spinBox3 = QSpinBox()
        spinBox3.setValue(1)
        spinBox3.setMinimum(1)
        spinBox3.setMaximum(31)

        label5 = QLabel("마지막날짜: ")
        spinBox4 = QSpinBox()
        spinBox4.setValue(2018)
        spinBox4.setMaximum(3000)
        spinBox5 = QSpinBox()
        spinBox5.setValue(1)
        spinBox5.setMinimum(1)
        spinBox5.setMaximum(12)
        spinBox6 = QSpinBox()
        spinBox6.setValue(1)
        spinBox6.setMinimum(1)
        spinBox6.setMaximum(31)

        pushButton1 = QPushButton("종가")
        pushButton2 = QPushButton("코사인 유사도 분석")
        pushButton3 = QPushButton("군집 분석")

        checkBox = QCheckBox("크롬 드라이브에서 adobe flash 사용")
        pushButton4 = QPushButton("일일 주식 정보")
        pushButton5 = QPushButton("주식 분봉 데이터")
        pushButton6 = QPushButton("파일경로 설정")
        pushButton6.clicked.connect(self.pushButtonClicked)
        label6 = QLabel()

        firstLayOut = QVBoxLayout()
        firstLayOut.addWidget(label1)
        firstLayOut.addWidget(radio1)
        firstLayOut.addWidget(radio2)

        secondLayOut = QHBoxLayout()
        secondLayOut.addWidget(label2)
        secondLayOut.addWidget(lineEdit1)

        thirdLayOut = QHBoxLayout()
        thirdLayOut.addWidget(label3)
        thirdLayOut.addWidget(lineEdit2)

        FourthLayOut = QGridLayout()
        FourthLayOut.addWidget(label4, 1, 0)
        FourthLayOut.addWidget(spinBox1, 1, 1)
        FourthLayOut.addWidget(spinBox2, 1, 2)
        FourthLayOut.addWidget(spinBox3, 1, 3)
        FourthLayOut.addWidget(label5, 2, 0)
        FourthLayOut.addWidget(spinBox4, 2, 1)
        FourthLayOut.addWidget(spinBox5, 2, 2)
        FourthLayOut.addWidget(spinBox6, 2, 3)

        FifthLayOut = QHBoxLayout()
        FifthLayOut.addWidget(pushButton1)
        FifthLayOut.addWidget(pushButton2)
        FifthLayOut.addWidget(pushButton3)

        SixthLayOut = QVBoxLayout()
        SixthLayOut.addWidget(checkBox)
        SixthLayOut.addWidget(pushButton4)
        SixthLayOut.addWidget(pushButton5)
        SixthLayOut.addWidget(pushButton6)
        SixthLayOut.addWidget(label6)

        layout = QVBoxLayout()
        layout.addLayout(firstLayOut)
        layout.addLayout(secondLayOut)
        layout.addLayout(thirdLayOut)
        layout.addLayout(FourthLayOut)
        layout.addLayout(FifthLayOut)
        layout.addLayout(SixthLayOut)

        self.setLayout(layout)

    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label.setText(fname[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()


