from xlrd import open_workbook

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
BI, BJ, BL, BM, BP, BR, BS, BT, BU, BW, BX, BY
"""
initialColumnChars = ['C', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'Q', 'S', 'U', 'V', 'W', 'Y', 'Z']
columnCharsAfterA = ['A','B','D','I','J','K','L']
columnCharsAfterB = ['I','J','L','M','P','R','S','T','U','W','X','Y']
columnNumsToUse = []
for char1 in initialColumnChars:
    currentColumnNum =ord(char1)-ord('A')
    columnNumsToUse.append(currentColumnNum)
for char2 in columnCharsAfterA:
    currentColumnNum = ord(char2) - ord('A') + 26
    columnNumsToUse.append(currentColumnNum)
for char3 in columnCharsAfterB:
    currentColumnNum = ord(char3) - ord('A') + 52
    columnNumsToUse.append(currentColumnNum)

print(columnNumsToUse)

for rowIndex in range(4,numRows):
    for colIndex in columnNumsToUse:
        currentVal = str(prostateInfoSheet.cell(rowIndex,colIndex).value)
        print("ROW:" + str(rowIndex) + " COL:" + str(colIndex) + "::" + currentVal)