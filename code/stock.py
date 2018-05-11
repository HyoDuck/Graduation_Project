# 마지막 수정일 : 2018/05/11
# 키움증권 api를 이용해 사용자가 원하는 종목코드의 분봉데이터를 가져옵니다.

import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd
import sqlite3

stock = input("원하는 종목코드: ")
class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10080_req":
            self._opt10080(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10080(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            print("분봉 데이터 저장중")
            date = self._comm_get_data(trcode, "", rqname, i, "체결시간")
            high = self._comm_get_data(trcode, "", rqname, i, "현재가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            if(high[0] == '-'):
                high = high[1:]
            if(low[0] == '-'):
                low = low[1:]

            self.ohlcv['date'].append(date)
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))

            if date[8:] == "090000":
                open = self._comm_get_data(trcode, "",rqname, i, "시가")
                if(open[0] == '-'):
                    open = open[1:]
                self.ohlcv['open'].append(int(open))
            else:
                open="00000";
                self.ohlcv['open'].append(int(open))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    kiwoom.ohlcv = {'date': [], 'high': [], 'low': [], 'open': []}
    
    # opt10081 TR 요청
    kiwoom.set_input_value("종목코드", stock)
    kiwoom.set_input_value("틱범위", 1)
    kiwoom.set_input_value("수정주가구분", 1)
    kiwoom.comm_rq_data("opt10080_req", "opt10080", 0, "0101")

    for i in range(1):
        time.sleep(0.2)
        kiwoom.set_input_value("종목코드", stock)
        kiwoom.set_input_value("수정주가구분", 1)
        kiwoom.comm_rq_data("opt10080_req", "opt10080", 2, "0101")

    df = pd.DataFrame(kiwoom.ohlcv, columns=['high', 'low','open'], index=kiwoom.ohlcv['date'])

    con = sqlite3.connect("c:/Anaconda3/Lib/idlelib/stock.db")
    df.to_sql('005930', con, if_exists='replace')
