import datetime
from datetime import date
import numpy as np

MISSING_DATA_FLOAT_VALUE = -3000
EPOCH = datetime.datetime.utcfromtimestamp(0).date()

def obtainAgeFromDOBFields(ageCellContents,dobCellValue,dateOfMRIcellString):
    currentAge = 0
    try:
        currentAge = float(ageCellContents)
    except:
        if (dobCellValue and dateOfMRIcellString):
            # obtains date of mri
            dateOfMRIcellValue = dateOfMRIcellString.date()

            # obtain DOB
            dobEntries = dobCellValue.split("/")
            dobDate = date(int(dobEntries[2]), int(dobEntries[0]), int(dobEntries[1]))

            # obtains the age at time of MRI
            diffBetweenBirthAndMRI = dateOfMRIcellValue - dobDate
            currentAge = diffBetweenBirthAndMRI.days / 365  # gets the floor, what we want
    return currentAge

def obtainUniqueEntries(stringArray):
    returnSet = set()
    for str1 in stringArray:
        returnSet.add(str1)
    return returnSet

def obtainNumericFieldValue(cellString):
    try:
        bmiValue=float(cellString)
    except:
        bmiValue = MISSING_DATA_FLOAT_VALUE
    return bmiValue

def obtainCategoryFieldValue(cellString2,categoryDictionary):
    return obtainCategoryFieldValueWithMissingDataIndicators(cellString2,categoryDictionary,[])

def obtainResultYesNoValue(cellStringOrig,missingDataStrs):
    if(not cellStringOrig):
        return 0
    cellString = str(cellStringOrig).lower()
    for missingIndicator in missingDataStrs:
        if missingIndicator in cellString:
            return MISSING_DATA_FLOAT_VALUE
    if "1" in cellString:
        return 1
    else:
        return 0

def obtainCategoryFieldValueWithMissingDataIndicators(cellString2,categoryDictionary,missingDataInds):
    if (not cellString2):
        return MISSING_DATA_FLOAT_VALUE
    cellString = cellString2.lower()
    for missingIndicator in missingDataInds:
        if missingIndicator in cellString:
            return MISSING_DATA_FLOAT_VALUE
    if (cellString in categoryDictionary):
        return categoryDictionary[cellString]
    else:
        return MISSING_DATA_FLOAT_VALUE

"""
The logic for these columns is as follows:
    1. If value is less than 1 then use it
    2. If the value is greater than 1, 
        then divide it by 100
"""
def obtainPercentageFieldValue(percentageString):
    numericValue = obtainNumericFieldValue(percentageString)
    if(numericValue>1):
        return numericValue/100
    else:
        return numericValue

def obtainResult_0_N_or_missing_withMissingCat(cellStringOrig,Nvalue,missingDataInteger):
    try:
        cellValue = int(cellStringOrig)
        if(cellValue>=0 and cellValue <= Nvalue):
            if(cellValue==missingDataInteger):
                return MISSING_DATA_FLOAT_VALUE
            else:
                return cellValue
        else:
            return MISSING_DATA_FLOAT_VALUE
    except:
        return MISSING_DATA_FLOAT_VALUE

def obtainResult_0_N_or_missing_whereMissingIsZero(cellStringOrig,Nvalue):
    try:
        cellValue = int(cellStringOrig)
        if(cellValue>=0 and cellValue <= Nvalue):
            return cellValue
        else:
            return 0
    except:
        return 0

def obtainResult_0_N_or_missing(cellStringOrig,Nvalue):
    return obtainResult_0_N_or_missing_withMissingCat(cellStringOrig,Nvalue,Nvalue+3)

def obtainGleasonScoreFeatures(originalString):
    scoreStrings = set()
    for token1 in str(originalString).split(';'):
        for token3 in token1.split('='):
            for token2 in token3.split():
                if "+" in token2:
                    scoreStrings.add(token2)
    currentMoreDomOutput=MISSING_DATA_FLOAT_VALUE
    currentLessDomOutput=MISSING_DATA_FLOAT_VALUE
    maxTotalScore=0
    for scoreStr in scoreStrings:
        scoreDigits = scoreStr.split("+")
        moreDominantDigit = int(scoreDigits[0])
        lessDominantDigit = int(scoreDigits[1])
        currentTotalScore = moreDominantDigit+lessDominantDigit
        if( (currentTotalScore==maxTotalScore and moreDominantDigit>currentMoreDomOutput) or
                (currentTotalScore>maxTotalScore)):
            maxTotalScore=currentTotalScore
            currentMoreDomOutput=moreDominantDigit
            currentLessDomOutput=lessDominantDigit
    return currentMoreDomOutput,currentLessDomOutput

def obtainDateFromString(originalString):
    try:
        return originalString.date()
    except:

        try:
            # If the format is <Month written out> <Year>
            strWithoutTilda = originalString.replace("~", "")

            strParts = strWithoutTilda.split(" ")
            monthPart0 = strParts[0]
            monthPart = monthPart0[0:3].lower()
            yearPart = strParts[1]

            return datetime.datetime.strptime(monthPart + " 15 " + yearPart,"%b %d %Y")

        except:
            return MISSING_DATA_FLOAT_VALUE

def obtainDateOrMissingFromValueFeature(cellValue):
    try:
        #return cellValue.time()
        timeSinceEpoch = cellValue.date()-EPOCH
        return timeSinceEpoch.days
    except:
        return MISSING_DATA_FLOAT_VALUE

def obtainTimeSinceLastProcedure(lastProcedureDateString,currentDateString):
    try:
        currentDate = obtainDateFromString(currentDateString)
        lastProcDate = obtainDateFromString(lastProcedureDateString)
        if(currentDate==MISSING_DATA_FLOAT_VALUE or lastProcDate==MISSING_DATA_FLOAT_VALUE):
            return MISSING_DATA_FLOAT_VALUE
        timeSinceLast = currentDate-lastProcDate
        return np.abs(timeSinceLast.days)
    except:
        return MISSING_DATA_FLOAT_VALUE


