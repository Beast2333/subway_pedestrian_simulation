import dxfgrabber
import xlwt


def dxf_dumper(dxf1):
    row = []
    count = 0
    for e in dxf1.entities:
        count += 1
        if e.dxftype == 'POINT':
            position = e.point
            a, b, c = position[0], position[1], position[2]
            row_list = [e.layer, a, b, c]
            row.append(row_list)
    return row


def write_excel(row1):
    f = xlwt.Workbook()
    # 创建sheet1
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
    for i in range(len(row1)):
        for j in range(len(row1[i])):
            sheet1.write(i, j, row1[i][j], set_stlye("Time New Roman", 220, True))
    f.save('data.xls')
    return 0


if __name__ == '__main__':
    dxf = dxfgrabber.readfile("cad\subway0.dxf")
    row = dxf_dumper(dxf)
    write_excel(row)

