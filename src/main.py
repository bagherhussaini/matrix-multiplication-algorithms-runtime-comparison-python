import time
import numpy as np
import pandas as pd
import xlsxwriter


def main():
    n = [2 ** i for i in range(2, 10)]
    log = pd.DataFrame(index=[],
                       columns=['N', 'Normal_Multiplication_Time', 'Divide_and_Conquer_Time',
                                'Strassen_Time'])

    normal_multiplication_duration_db = []
    divide_and_conquer_duration_db = []
    strassen_duration_db = []

    for size in n:
        a = np.random.uniform(low=-500000, high=500000, size=(size, size))
        b = np.random.uniform(low=-500000, high=500000, size=(size, size))

        start_time = 0
        start_time = time.time()
        result = normal_multiplication(a, b)
        normal_multiplication_duration = time.time() - start_time
        normal_multiplication_duration_db.append(
            normal_multiplication_duration)

        start_time = 0
        start_time = time.time()
        result = divide_and_conquer(a, b)
        divide_and_conquer_duration = time.time() - start_time
        divide_and_conquer_duration_db.append(divide_and_conquer_duration)

        start_time = 0
        start_time = time.time()
        result = strassen(a, b)
        strassen_duration = time.time() - start_time
        strassen_duration_db.append(strassen_duration)

        tmp = pd.Series([
            size,
            normal_multiplication_duration,
            divide_and_conquer_duration,
            strassen_duration
        ], index=['N', 'Normal_Multiplication_Time', 'Divide_and_Conquer_Time', 'Strassen_Time'])
        log = log.append(tmp, ignore_index=True)
        log.to_csv('time-complexity.csv', index=False)

    workbook = xlsxwriter.Workbook('chart.xlsx')
    worksheet = workbook.add_worksheet()

    chart = workbook.add_chart({'type': 'line'})
    bold = workbook.add_format({'bold': True})
    headings = ['N', 'Normal_Multiplication', 'Divide_and_Conquer', 'Strassen']

    worksheet.write_row('A1', headings, bold)
    worksheet.write_column('A2', n)
    worksheet.write_column('B2', normal_multiplication_duration_db)
    worksheet.write_column('C2', divide_and_conquer_duration_db)
    worksheet.write_column('D2', strassen_duration_db)

    chart.add_series({
        'name': '=Sheet1!$B$1',
        'categories': '=Sheet1!$A$2:$A$9',
        'values': '=Sheet1!$B$2:$B$9',
    })
    chart.add_series({
        'name': '=Sheet1!$C$1',
        'categories': '=Sheet1!$A$2:$A$9',
        'values': '=Sheet1!$C$2:$C$9',
    })
    chart.add_series({
        'name': '=Sheet1!$D$1',
        'categories': '=Sheet1!$A$2:$A$9',
        'values': '=Sheet1!$D$2:$D$9',
    })

    worksheet.insert_chart('G10', chart)
    workbook.close()
    return log


def normal_multiplication(a, b):
    n = len(a)
    result = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i, j] += a[i, k] * b[k, j]
    return result


def divide_and_conquer(a, b):
    n = len(a)
    if n == 1:
        return a * b
    else:
        a11 = a[:int(len(a) / 2), :int(len(a) / 2)]
        a12 = a[:int(len(a) / 2), int(len(a) / 2):]
        a21 = a[int(len(a) / 2):, :int(len(a) / 2)]
        a22 = a[int(len(a) / 2):, int(len(a) / 2):]

        b11 = b[:int(len(b) / 2), :int(len(b) / 2)]
        b12 = b[:int(len(b) / 2), int(len(b) / 2):]
        b21 = b[int(len(b) / 2):, :int(len(b) / 2)]
        b22 = b[int(len(b) / 2):, int(len(b) / 2):]

        c11 = divide_and_conquer(a11, b11) + divide_and_conquer(a12, b21)
        c12 = divide_and_conquer(a11, b12) + divide_and_conquer(a12, b22)
        c21 = divide_and_conquer(a21, b11) + divide_and_conquer(a22, b21)
        c22 = divide_and_conquer(a21, b12) + divide_and_conquer(a22, b22)

        result = np.zeros((n, n))
        result[:int(len(result) / 2), :int(len(result) / 2)] = c11
        result[:int(len(result) / 2), int(len(result) / 2):] = c12
        result[int(len(result) / 2):, :int(len(result) / 2)] = c21
        result[int(len(result) / 2):, int(len(result) / 2):] = c22
    return result


def strassen(a, b):
    n = len(a)
    if n <= 4:
        return normal_multiplication(a, b)
    else:
        a11 = a[:int(len(a) / 2), :int(len(a) / 2)]
        a12 = a[:int(len(a) / 2), int(len(a) / 2):]
        a21 = a[int(len(a) / 2):, :int(len(a) / 2)]
        a22 = a[int(len(a) / 2):, int(len(a) / 2):]

        b11 = b[:int(len(b) / 2), :int(len(b) / 2)]
        b12 = b[:int(len(b) / 2), int(len(b) / 2):]
        b21 = b[int(len(b) / 2):, :int(len(b) / 2)]
        b22 = b[int(len(b) / 2):, int(len(b) / 2):]

        p1 = strassen(a11, b12 - b22)
        p2 = strassen(a11 + a12, b22)
        p3 = strassen(a21 + a22, b11)
        p4 = strassen(a22, b21 - b11)
        p5 = strassen(a11 + a22, b11 + b22)
        p6 = strassen(a12 - a22, b21 + b22)
        p7 = strassen(a11 - a21, b11 + b12)

        result = np.zeros((n, n))
        result[:int(len(result) / 2), :int(len(result) / 2)
               ] = p5 + p4 - p2 + p6
        result[:int(len(result) / 2), int(len(result) / 2):] = p1 + p2
        result[int(len(result) / 2):, :int(len(result) / 2)] = p3 + p4
        result[int(len(result) / 2):, int(len(result) / 2)               :] = p5 + p1 - p3 - p7
        return result


if __name__ == "__main__":
    log = main()
