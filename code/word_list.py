import openpyxl

def word_list(excel,word):
    
    wb = openpyxl.load_workbook(excel)

    ws = wb.active
    i=0
    word_list=[]
    for r in ws.rows:
        row_index=r[0].value
        if row_index == word:
            for j in ws.columns:
                if i>0:
                    if r[i].value >=-0.1 and r[i].value<=0.1:
                        word_list.append(j[0].value)
                i+=1
    return word_list


