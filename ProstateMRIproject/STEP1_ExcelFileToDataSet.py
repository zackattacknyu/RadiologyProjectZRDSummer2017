"""
Columns we care about are the following:
C, G, H, I, J, L, M, N, Q, S, U, V, W, Y, Z
AA, AB, AD, AI, AJ, AK, AL
BI, BJ, BL, BM, BP, BR, BS, BT, BU, BW, BX, BY, BZ
CC, CI, CN, CO, CU, CV, CW, CX, CY, CZ
DA, DC, DD, DE, DF, DG, DH, DI, DK, DL, DN, DT, DU, DV, DW, DX, DY, DZ
EA, EB, EC, ED, EE, EF, EG, EH, ER, ES, ET, EV, EW, EY
FC, FD, FE, FF, FG, FH, FI, FK, FL, FM, FN, FO, FP, FQ, FR, FS, FT, FU, FV
"""

import numpy as np
import openpyxl


prostateFilePath='D:/DATA/rouProstateFiles/ROU_LESION_DATA_EXCELFILE.xlsx'

excelData = openpyxl.load_workbook(prostateFilePath)
dataOnSheet = excelData['Sheet1']

for rowI in range(5,10):
    cellKey = 'G'+str(rowI)
    print(dataOnSheet[cellKey].value)