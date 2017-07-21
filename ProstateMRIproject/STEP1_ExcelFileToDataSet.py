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

prostateFilePath='D:/DATA/rouProstateFiles/ROU_LESION_DATA_EXCELFILE.xlsx'

excelData = openpyxl.load_workbook(prostateFilePath)
dataOnSheet = excelData['Sheet1']

# for rowI in range(5,10):
#     cellKey = 'H'+str(rowI)
#     print(dataOnSheet[cellKey].value)

"""
This will give us Age at Time of MRI
Column H contains that data
If column H missing, do the following:
    Column C is date of MRI, Column G is date of birth
"""

ageOfPatients = []
for rowI in range(5,dataOnSheet.max_row):
    cellKey= 'H'+str(rowI)
    cellContents = dataOnSheet[cellKey].value
    currentAge=0
    try:
        currentAge=float(cellContents)
    except:

        #obtains date of birth string
        dobCellKey='G'+str(rowI)
        dobCellValue = dataOnSheet[dobCellKey].value

        # obtains date of mri string
        dateOfMRIcellKey = 'C' + str(rowI)
        dateOfMRIcellString = dataOnSheet[dateOfMRIcellKey].value

        if(dobCellValue and dateOfMRIcellString):

            #obtains date of mri
            dateOfMRIcellValue = dateOfMRIcellString.date()

            #obtain DOB
            dobEntries = dobCellValue.split("/")
            dobDate = date(int(dobEntries[2]),int(dobEntries[0]),int(dobEntries[1]))

            #obtains the age at time of MRI
            diffBetweenBirthAndMRI = dateOfMRIcellValue-dobDate
            currentAge = diffBetweenBirthAndMRI.days/365 #gets the floor, what we want

    ageOfPatients.append(currentAge)

ageAtMriFeature = np.array(ageOfPatients)
print(ageAtMriFeature.shape)

"""
This will give us the BMI of patients
"""
bmiOfPatients = []
for rowI in range(5,dataOnSheet.max_row):
    cellKey = 'J'+str(rowI)
    bmiCellStr = dataOnSheet[cellKey].value
    try:
        bmiValue=float(bmiCellStr)
    except:
        bmiValue = 0
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
TODO: Setup this logic
"""
raceOfPts = []
raceOfPtsSet = set()
for rowI in range(5,dataOnSheet.max_row):
    cellKey='I'+str(rowI)
    raceStr=dataOnSheet[cellKey].value
    raceOfPts.append(raceStr)
    raceOfPtsSet.add(raceStr)

print(raceOfPtsSet)
#plt.plot(ageAtMriFeature,bmiFeature,'r.')
#plt.show()

# dobColumn = HelperFunctions.getColumnNumber('H')
# for row in dataOnSheet.iter_rows(min_row=5,max_row=dataOnSheet.get_highest_row(),min_col=dobColumn,max_col=dobColumn):
#     for cell in row:
#         print(cell.value)
