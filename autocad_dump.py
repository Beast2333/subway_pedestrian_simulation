import dxfgrabber
import xlwt


def dxf_dumper(dxf1):
    row = []
    count = 0
    for e in dxf1.entities:

        if e.dxftype == 'POINT':
            count += 1
            position = e.point
            a, b, c = position[0], position[1], position[2]
            if e.layer == '入口':
                d = 0
            elif e.layer == '闸机入':
                d = 1
            elif e.layer == '楼扶梯下':
                d = 2
            elif e.layer == '楼扶梯上':
                d = 3
            elif e.layer == '闸机出':
                d = 4
            elif e.layer == '出口':
                d = 5
            elif e.layer == '换乘入口':
                d = 6
            elif e.layer == '换乘出口':
                d = 7
            else:
                d = 9
            row_list = [count, e.layer, d, a, b, c]

            row.append(row_list)
    return row


def write_excel(row1):
    f = xlwt.Workbook()
    # 创建sheet1
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
    for i in range(len(row1)):
        for j in range(len(row1[i])):
            sheet1.write(i, j, row1[i][j])
    f.save('data.xls')
    return 0


if __name__ == '__main__':
    dxf = dxfgrabber.readfile("./cad/subway0.dxf")
    row = dxf_dumper(dxf)
    write_excel(row)

