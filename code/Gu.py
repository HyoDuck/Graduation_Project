import sys
from PyQt5.QtWidgets import *
import download_stockinfo

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 500, 300)

        pushButton1 = QPushButton("종목보기")
        pushButton1.clicked.connect(self.pushButtonClicked)
        pushButton2 = QPushButton("갱신")
        pushButton3 = QPushButton("분석")
        pushButton4 = QPushButton("가져오기")
        pushButton4.clicked.connect(self.download_button)

        checkBox = QCheckBox("ETF, ETN")
        textEdit = QTextEdit()

        firstLayOut = QHBoxLayout()
        firstLayOut.addWidget(pushButton1)
        firstLayOut.addWidget(pushButton2)
        firstLayOut.addWidget(pushButton3)
        firstLayOut.addWidget(pushButton4)

        secondLayOut = QVBoxLayout()
        secondLayOut.addWidget(checkBox)
        secondLayOut.addWidget(textEdit)

        layout = QVBoxLayout()
        layout.addLayout(firstLayOut)
        layout.addLayout(secondLayOut)

        self.setLayout(layout)

    def pushButtonClicked(self):
        items = ("KOSPI", "KOSDAK")
        item, ok = QInputDialog.getItem(self, "시장선택", "시장을 선택하세요.", items, 0, False)
        if ok and item:
            self.label.setText(item)

    def download_button(self, download_path='C:/data'):
        download_stockinfo.Get_KospiInfo(download_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()


