import xlrd
import random
import os
import re
import pandas as pd

def read(file):
    pattern = re.compile(r"\s+")
    workbook = xlrd.open_workbook(file)
    print(workbook.nsheets)
    df = pd.DataFrame(columns = ['Sheet Name', 'Country', 'Author', 'Application', 'Field', 'Year'], index=range(workbook.nsheets-1))
    for i, sheet in enumerate(workbook.sheets()):
        if i == 0:
            continue
        cur_sheet = ' '.join(sheet.name.split())
        country = ' '.join(sheet.cell(3, 1).value.split())
        author = ' '.join(sheet.cell(6, 1).value.split())
        application = ' '.join(str(sheet.cell(10, 1).value).split())
        field = ' '.join(sheet.cell(11, 1).value.split())
        year = pattern.sub(" ", str(sheet.cell(12, 1).value))
        df.iloc[i-1] = [cur_sheet, country, author, application, field, year]
    df.to_csv('../data/res.csv', index=False)
        # if country == '':
            # country = sheet.
        # print(sheet.cell(3, 1).value)


    # print(workbook)
    # print(workbook.keys())
    # sheet = workbook.sheet_by_index(0)
    # res = []
    # missing = 0
    # existing = 0
    # print('Total: {}'.format(sheet.nrows))
    # for rowx in range(sheet.nrows):
    #     cols = sheet.row_values(rowx)

if __name__ == '__main__':
    file = '../data/review_85188_extracted_data_xlsx_20200609043441.xls'
    read(file)
