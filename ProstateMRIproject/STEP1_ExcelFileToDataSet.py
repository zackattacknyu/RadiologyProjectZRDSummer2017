"""
Columns we care about are the following:
C, G, H, I, J, L, M, N, Q, S, U, V, W, Y, Z
AA, AB, AD, AI, AJ, AK, AL
BI, BJ, BL, BM, BP, BR, BS, BT, BU, BW, BX, BY, BZ
CC, CI, CN, CO, CU, CV, CW, CX, CY, CZ
DA, DC, DD, DE, DF, DG, DH, DI, DK, DL, DN, DT, DU, DV, DW, DX, DY, DZ
EA, EB, EC, ED, EE, EF, EG, EH, ER, ES, ET, EV, EW, EY
FC, FD, FE, FF, FG, FH, FI, FK, FL, FM, FN, FO, FP, FQ, FR, FS, FT, FU, FV

NOTE:
    MISSING DATA WILL BE GIVEN VALUE -1 IN THE DATA SET

This site has documentation on using XGBoost
http://xgboost.readthedocs.io/en/latest/python/python_api.html#module-xgboost.core

Under "XGBRegressor" and "XGBClassifier" there is a parameter
    entitled "missing" where you denote the float value that represents
    missing data.
IMPORTANT: Set that paramater to -1 before doing any training with this data

IMPORTANT CODING NOTE:
    THIS CODE USING FUNCTIONAL PROGRAMMING FEATURES
    MEANING THAT FUNCTIONS ARE PASSED AS ARGUMENTS
    THERE IS A GOOD EXAMPLE IN THIS WEBPAGE SHOWING ITS USE IN PYTHON:
        https://stackoverflow.com/questions/706721/how-do-i-pass-a-method-as-a-parameter-in-python
"""

import numpy as np
import openpyxl
import HelperFunctions
from datetime import datetime
from datetime import date
from matplotlib import pyplot as plt
import DataSetLogic
import CategoryFeatureLogic

INITIAL_ROW_NUMBER=5
DATA_WORKSHEET_NAME='Sheet1'
PROSTATE_FILE_PATH= 'D:/DATA/rouProstateFiles/ROU_LESION_DATA_modified.xlsx'

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

def TESTFUNC_printUniqueEntries(stringArray):
    returnSet = set()
    for str1 in stringArray:
        returnSet.add(str1)
    for entry in returnSet:
        print(entry)

def OBTAIN_FEATURE_COLUMN(columnCodeStr,functionForFeatureLogic,*functionArgs):
    dataInCol = getAllStringsForCol(columnCodeStr)
    colDataRes = []
    for listInd in range(len(dataInCol)):
        colDataRes.append(functionForFeatureLogic(dataInCol[listInd], *functionArgs))
    featureData = np.array(colDataRes)
    return featureData

def get0_to_N_or_missingFeature(columnCodeStr, Nval):
    return OBTAIN_FEATURE_COLUMN(columnCodeStr,DataSetLogic.obtainResult_0_N_or_missing,Nval)

def get0_to_N_or_missingFeature_withMissingCat(columnCodeStr, Nval,missingDataInt):
    return OBTAIN_FEATURE_COLUMN(
        columnCodeStr,
        DataSetLogic.obtainResult_0_N_or_missing_withMissingCat,
        Nval,missingDataInt)

def get0_to_N_or_missingFeature_withMissingCat_Matrix(columnCodeStr,Nval,missingDataInt):
    colFeature = get0_to_N_or_missingFeature_withMissingCat(columnCodeStr,Nval,missingDataInt)
    return CategoryFeatureLogic.categoryToOneHotFeatureZeroStart(colFeature,Nval+1,-1,-1)

def getNumericValueFeature(columnCodeStr):
    return OBTAIN_FEATURE_COLUMN(columnCodeStr, DataSetLogic.obtainNumericFieldValue)


def getPercentageValueFeature(columnCodeStr):
    return OBTAIN_FEATURE_COLUMN(columnCodeStr, DataSetLogic.obtainPercentageFieldValue)

def getTimeSinceFeature(lastProcDateColumnCode,currentDateColumnCode):
    colAIvalues = getAllStringsForCol(lastProcDateColumnCode)
    colCvalues = getAllStringsForCol(currentDateColumnCode)
    featureVals = []
    for index in range(len(colAIvalues)):
        currentDate = colCvalues[index]
        lastProcDate = colAIvalues[index]
        timeSinceLast = DataSetLogic.obtainTimeSinceLastProcedure(lastProcDate,currentDate)
        featureVals.append(timeSinceLast)
    return np.array(featureVals)

def getBackfillPercentageFeature(percentageFeature,numeratorFeature,denominatorFeature):
    outputFeature = []
    for index1 in range(len(percentageFeature)):
        percentage = percentageFeature[index1]
        if(percentage<0):
            numer = float(numeratorFeature[index1])
            denom = float(denominatorFeature[index1])
            if(numer>0 and denom>0):
                outputFeature.append(numer/denom)
            else:
                outputFeature.append(-1)
        else:
            outputFeature.append(percentage)
    return np.array(outputFeature)

def getCategoryFeature(columnCodeStr,categoryDictionary):
    allCategoryNums = []
    allCatEntries = getAllStringsForCol(columnCodeStr)
    for listInd in range(len(allCatEntries)):
        catNum = DataSetLogic.obtainCategoryFieldValue(allCatEntries[listInd],
                                                        categoryDictionary)
        allCategoryNums.append(catNum)
    return np.array(allCategoryNums)

def getGleasonScoreMatrix(columnCodeStr):
    gleasonScores = getAllStringsForCol(columnCodeStr)
    gleasonScoreMoreDom = []
    gleasonScoreLessDom = []
    for listInd in range(len(gleasonScores)):
        moredom, lessdom = DataSetLogic.obtainGleasonScoreFeatures(gleasonScores[listInd])
        gleasonScoreMoreDom.append(moredom)
        gleasonScoreLessDom.append(lessdom)
    gleasonScoreMoreDomFeature = np.array(gleasonScoreMoreDom)
    gleasonScoreLessDomFeature = np.array(gleasonScoreLessDom)
    gleasonScoreMatrix = np.zeros((len(gleasonScoreLessDom),2))
    gleasonScoreMatrix[:,0]=gleasonScoreMoreDomFeature
    gleasonScoreMatrix[:,1]=gleasonScoreLessDomFeature
    return gleasonScoreMatrix

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


"""
This will give us the BMI of patients
"""
bmiFeature = getNumericValueFeature('J')


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
raceCategories = {"white":1,"black":2,"asian":3,"asian/pacific":4,"amer indian/eskimo":5}
raceFeature = getCategoryFeature('I',raceCategories)
raceFeatureMatrix=CategoryFeatureLogic.categoryToOneHotNoBothNeither(raceFeature,5)
print(raceFeatureMatrix.shape)


"""
Column L: Prior Outside Biopsy
If string contains "no notes", "unknown" or "n/a" then missing data, make it -1
else if string contains "1" then make value 1, meaning yes
else make it "0" for no prior biopsy
"""
allPriorOutside = getAllStringsForCol('L')
#TESTFUNC_printUniqueEntries(allPriorOutside)
priorOutsideValues =[]
for listInd in range(len(allPriorOutside)):
    priorOutsideValues.append(DataSetLogic.obtainResultYesNoValue(
        allPriorOutside[listInd],['no notes','unknown','n/a']))
priorOutsideFeature = np.array(priorOutsideValues)

"""
Column M: Prior Result
Same logic as L
"""
allPriorResult = getAllStringsForCol('M')
#TESTFUNC_printUniqueEntries(allPriorResult)
priorResult =[]
for listInd in range(len(allPriorOutside)):
    priorResult.append(DataSetLogic.obtainResultYesNoValue(
        allPriorOutside[listInd],['no notes','unknown','n/a']))
priorResultFeature = np.array(priorResult)


"""
Column N: Gleason Score
Logic will be as follows:
    -Split string by space and semi-colon
    -Use the strings in the form A+B
    -Use whichever one has highest C = A+B
        - If there is a tie, use one with higher A
If either feature is -1, then there is missing data
"""
colNmatrix=getGleasonScoreMatrix('N')


"""
Column Q: Digital Rectal Exam score
Column S: Pre-biopsy clinical information assay
Column U: Pre-biopsy clinical information assay qualitative, positive or negative
***GO BACK TO COLUMN V***
Column W: Assay
Column Y: Assay Result
Column Z: Risk of High Grade Caner
    - 0,1,or missing
"""
dreResultFeature = get0_to_N_or_missingFeature('Q',1)
preBiopsyFeature = get0_to_N_or_missingFeature('S',1)
colUfeature = get0_to_N_or_missingFeature('U',1)
colWfeature = get0_to_N_or_missingFeature('W',1)
colYfeature = get0_to_N_or_missingFeature('Y',1)
riskOfHighGradeCancerFeature = get0_to_N_or_missingFeature('Z',1)


"""
Column AA
"""
colAAfeature = get0_to_N_or_missingFeature('AA',3)
colAAfeatureMatrix = CategoryFeatureLogic.categoryToOneHotFeatureZeroStart(colAAfeature,4,-1,-1)
print(colAAfeatureMatrix.shape)

"""
Column AB
"""
colABfeature = get0_to_N_or_missingFeature('AB',1)


"""
Column AD, percentage risk of high grade tumors
"""
colADfeature = getPercentageValueFeature('AD')


"""
Column AI
Most recent PSA. 
Will store time in days since most recent one
"""
timeSincePSA=getTimeSinceFeature('AI','C')


"""
Column AJ, AK are both numeric values
"""
colAJfeature = getNumericValueFeature('AJ')
colAKfeature = getNumericValueFeature('AK')


"""
Column AL
If missing then do AK/AJ
"""
colALfeature = getPercentageValueFeature('AL')
freePSApercentFeature = getBackfillPercentageFeature(colALfeature,colAKfeature,colAJfeature)


"""
Column BI, BJ are numeric values
"""
colBIfeature = getNumericValueFeature('BI')
colBJfeature = getNumericValueFeature('BJ')

"""
column BL,BM is a percentage
"""
colBLfeature = getPercentageValueFeature('BL')
colBMfeature = getPercentageValueFeature('BM')

"""
column BP is category
-1: unknown, other
1: Siemens 3T
2: Phillips
"""
deviceCategories = {"siemens 3t":1,"phillips":2}
deviceFeature = getCategoryFeature('BP',deviceCategories)
deviceFeatureMatrix=CategoryFeatureLogic.categoryToOneHotNoBothNeither(deviceFeature,2)
print(deviceFeatureMatrix.shape)

"""
column BR is positive or negative
"""
colBRfeature = get0_to_N_or_missingFeature('BR',1)
colBSfeature = get0_to_N_or_missingFeature('BS',1)

"""
lesion Info: BT, BU, BW, BX, BY, BZ
"""

"""
For column BT, "3" indicates missing data
"""
colBTfeature = get0_to_N_or_missingFeature_withMissingCat('BT',4,3)
colBTfeatureMatrix = CategoryFeatureLogic.categoryToOneHotNoBothNeither(colBTfeature,4)

"""
Column BU, where lesion is located
L: left
R: right
B: both
N: no laterality
"""
colBUcategories = {"l":1,"r":2,"b":3,"n":4}
colBUfeaturePre = getCategoryFeature('BU',colBUcategories)
colBUfeatureMatrix = CategoryFeatureLogic.categoryToOneHotFeature(colBUfeaturePre,2,3,4)
print(colBUfeatureMatrix.shape)

"""
Column BW, BX, BY: Lesion Location Information
All Zero, One, Missing type fields
"""
columnBWfeature = get0_to_N_or_missingFeature('BW',1)
columnBXfeature = get0_to_N_or_missingFeature('BX',1)
columnBYfeature = get0_to_N_or_missingFeature('BY',1)


"""
Column BZ: Lesion Size, numeric value
"""
colBZfeature = getNumericValueFeature('BZ')


"""
Column CC
Numeric value 0-5 with 0 meaning missing
"""
colCCfeature = get0_to_N_or_missingFeature_withMissingCat('CC',5,0)

"""
Column CI
same logic as CC
"""
colCIfeature = get0_to_N_or_missingFeature_withMissingCat('CI',5,0)

"""
Column CN
3 values: 0,1,2
0 negative, 1 positive, 2 no score given, so missing
"""
colCNfeature = get0_to_N_or_missingFeature_withMissingCat('CN',2,2)

"""
Column CO
Numeric value 0-5 with 0 being missing data
"""
colCOfeature = get0_to_N_or_missingFeature_withMissingCat('CO',5,0)

"""
Column CU
**COLUMN TO PREDICT**
0,1,2
0 negative, 1 positive, 2 missing
"""
colCUfeature = get0_to_N_or_missingFeature_withMissingCat('CU',2,2)

"""
Column CV
**COLUMN TO PREDICT**
same logic as CU
"""
colCVfeature = get0_to_N_or_missingFeature_withMissingCat('CV',2,2)

"""
Column CW
Summary of Gleason score
numeric value 0-10
"""
colCWfeature = get0_to_N_or_missingFeature('CW',10)

"""
Column CX
same logic as CU
"""
colCXfeature = get0_to_N_or_missingFeature_withMissingCat('CX',2,2)


"""
Column CY
other 12core biospy
"""
colCYfeatureMatrix=get0_to_N_or_missingFeature_withMissingCat_Matrix('CY',3,2)
print(colCYfeatureMatrix.shape)

"""
Column CZ
gleason score for 12core. same logic as N
"""
colCZfeatureMatrix = getGleasonScoreMatrix('CZ')

"""
Column DA
summary of gleason score. same logic as CW
"""
colDAfeature = get0_to_N_or_missingFeature('CW',10)

"""
Column DC
"""
colDCfeature = getPercentageValueFeature('DC')

"""
Column DD
same logic as CY
"""
colDDfeatureMatrix = get0_to_N_or_missingFeature_withMissingCat_Matrix('DD',3,2)
print(colDDfeatureMatrix.shape)

"""
column DE
**IMPORTANT COLUMN**
0 - negative
1 - positive
2 - missing data
"""
colDEfeature = get0_to_N_or_missingFeature_withMissingCat('DE',2,2)

""""
column DF
"""
colDFfeature = get0_to_N_or_missingFeature_withMissingCat('DF',2,2)

"""
column DG
same logic as CY
"""
colDGfeatureMatrix = get0_to_N_or_missingFeature_withMissingCat_Matrix('DG',3,2)

"""
column DH
gleason score column. same as N
"""
columnDHfeature = getGleasonScoreMatrix('DH')
print(columnDHfeature.shape)

"""
Column DI
sum of gleason score. 0-10
"""
columnDIfeature = get0_to_N_or_missingFeature('DI',10)

"""
Column DK
percentage value
"""
columnDKfeature = getPercentageValueFeature('DK')

"""
Column DL. same logic as DD
"""
colDLfeatureMatrix = get0_to_N_or_missingFeature_withMissingCat_Matrix('DL',3,2)


