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
import HelperFunctions
from datetime import datetime
from datetime import date
from matplotlib import pyplot as plt
import DataSetLogic

INITIAL_ROW_NUMBER=5
DATA_WORKSHEET_NAME='Sheet1'
PROSTATE_FILE_PATH= 'D:/DATA/rouProstateFiles/ROU_LESION_DATA_EXCELFILE.xlsx'

excelData = openpyxl.load_workbook(PROSTATE_FILE_PATH)
dataOnSheet = excelData[DATA_WORKSHEET_NAME]

def getCellKey(columnCodeStr,rowInteger):
    return columnCodeStr+str(rowInteger)

def getAllStringsForCol(columnCodeStr):
    allStrs = []
    for rowI in range(INITIAL_ROW_NUMBER, dataOnSheet.max_row):
        cellKey = getCellKey(columnCodeStr, rowI)
        ageCellContents = dataOnSheet[cellKey].value
        allStrs.append(ageCellContents)
    return allStrs


"""
This will give us Age at Time of MRI
Column H contains that data
If column H missing, do the following:
    Column C is date of MRI, Column G is date of birth
"""
ageOfPatients = []
ageCellContentsList = getAllStringsForCol('H')
dobCellValueList = getAllStringsForCol('G')
dateOfMRIcellStrList = getAllStringsForCol('C')
for listInd in range(len(ageCellContentsList)):
    currentAge = DataSetLogic.obtainAgeFromDOBFields(
        ageCellContentsList[listInd],
        dobCellValueList[listInd],
        dateOfMRIcellStrList[listInd])
    ageOfPatients.append(currentAge)
ageAtMriFeature = np.array(ageOfPatients)
print(ageAtMriFeature.shape)


"""
This will give us the BMI of patients
"""
bmiOfPatients = []
allBMIstrings = getAllStringsForCol('J')
for listInd in range(len(allBMIstrings)):
    bmiValue = DataSetLogic.obtainNumericFieldValue(allBMIstrings[listInd])
    bmiOfPatients.append(bmiValue)
bmiFeature = np.array(bmiOfPatients)
print(bmiFeature.shape)

"""
This tells the race of patients

Entries will be the following:
    -1: unknown/other/etc
    1: White
    2: Black
    3: Asian
    4: Asian/Pacific
    5: Amer Indian/Eskio
"""
raceOfPtsCatNums = []
raceCategories = {"white":1,"black":2,"asian":3,"asian/pacific":4,"amer indian/eskimo":5}
raceOfPtsAllEntries = getAllStringsForCol('I')
for listInd in range(len(raceOfPtsAllEntries)):
    raceNum = DataSetLogic.obtainCategoryFieldValue(raceOfPtsAllEntries[listInd], raceCategories)
    raceOfPtsCatNums.append(raceNum)
raceFeature = np.array(raceOfPtsCatNums)
print(raceFeature.shape)
# for num in range(-1,6):
#     print(len(np.where(raceFeature==num)[0]))




