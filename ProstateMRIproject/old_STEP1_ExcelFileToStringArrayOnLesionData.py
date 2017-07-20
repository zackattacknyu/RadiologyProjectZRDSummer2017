from xlrd import open_workbook
import numpy as np
import HelperFunctions

prostateFilePath='D:/DATA/rouProstateFiles/ROU_LESION_DATA_EXCELFILE.xlsx'

#opens the first worksheet, which contains the info,
#   in the excel spreadsheet
prostateInfoSheet = open_workbook(prostateFilePath).sheets()[0]

numRows = prostateInfoSheet.nrows
numCol = prostateInfoSheet.ncols

"""
IMPORTANT NOTE:
A1 in the Excel Spreadsheet corresponds
to (0,0) in (Row,Col) format

Rows are the numeric part of cell coords
Cols are the alphabetic part of cell coords
"""


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
columnChars = []
columnChars.append(['C', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'Q', 'S', 'U', 'V', 'W', 'Y', 'Z'])
columnChars.append(['A','B','D','I','J','K','L']) #all these have "A" as prefix
columnChars.append(['I','J','L','M','P','R','S','T','U','W','X','Y']) #all these have "B" as prefix
columnChars.append(['C','I','N','O','U','V','W','X','Y','Z']) #have "C" has prefix
columnChars.append(['A','C','D','E','F','G','H','I','K','L','N','T','U','V','W','X','Y','Z']) #have "D" as prefix
columnChars.append(['A','B','C','D','E','F','G','H','R','S','T','V','W','Y']) #have "E" prefix
columnChars.append(['C','D','E','F','G','H','I','K','L','M','N','O','P','Q','R','S','T','U','V']) #have "F" prefix

initialIndex=0
columnNumsToUse = []
for charList in columnChars:
    for currentChar in charList:
        colOffsetNum = ord(currentChar)-ord('A')
        columnNumUse = initialIndex+colOffsetNum
        columnNumsToUse.append(columnNumUse)
    initialIndex = initialIndex+26

stringArrayData = []
for rowIndex in range(4,numRows):
    curRow = ['' for x in range(numCol)]
    for colIndex in columnNumsToUse:
        currentVal = str(prostateInfoSheet.cell_value(rowIndex,colIndex))
        curRow[colIndex]=currentVal
    stringArrayData.append(curRow)

outputDataPath='D:/DATA/rouProstateFiles/ROU_LESION_DATA_AS_STIRNG_ARRAY.npy'

np.save(outputDataPath,stringArrayData)