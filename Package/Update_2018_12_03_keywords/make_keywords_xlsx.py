from pyexcelerate import Workbook
import datetime

def make_xlsx(stock_list, keywords_list, xlsx_path = 'C:/data', xlsx_name=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_'+'분석키워드'):
    mk = keywords_xlsx()
    mk.stock_list = stock_list
    mk.keywords_list = keywords_list
    mk.path = xlsx_path + '/' + xlsx_name + '.xlsx'

    mk.make_xlsx()

class keywords_xlsx:
    stock_list = []
    keywords_list = []
    path = ''

    def make_xlsx(self):
        wb = Workbook()
        ws = wb.new_sheet("sheet1")

        row = 1
        column = 1

        for i in range(0, len(self.stock_list), 1):
            for j in range(0, len(self.stock_list[i]), 1):
                ws.set_cell_value(row, column, self.stock_list[i][j])
                column = column + 1
            row = row + 2
            column = 1

        row = 2
        column = 1

        for i in range(0, len(self.keywords_list), 1):
            for j in range(0, len(self.keywords_list[i]), 1):
                ws.set_cell_value(row, column, self.keywords_list[i][j])
                column = column + 1
            row = row + 2
            column = 1

        wb.save(self.path)

if __name__ == '__main__':
    make_xlsx([['s1', 's2'], ['s3', 's4']], [['t1', 't2'], ['t3', 't4']])