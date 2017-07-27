import datetime
from datetime import date
import numpy as np

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

def obtainNumericFieldValue(cellString):
    try:
        bmiValue=float(cellString)
    except:
        bmiValue = -1
    return bmiValue

def obtainCategoryFieldValue(cellString2,categoryDictionary):
    if(not cellString2):
        return -1
    cellString = cellString2.lower()
    if (cellString in categoryDictionary):
        return categoryDictionary[cellString]
    else:
        return -1

def obtainResultYesNoValue(cellStringOrig,missingDataStrs):
    if(not cellStringOrig):
        return 0
    cellString = str(cellStringOrig).lower()
    for missingIndicator in missingDataStrs:
        if missingIndicator in cellString:
            return -1
    if "1" in cellString:
        return 1
    else:
        return 0

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


def obtainResult_0_N_or_missing(cellStringOrig,Nvalue):
    try:
        cellValue = int(cellStringOrig)
        if(cellValue>=0 and cellValue <= Nvalue):
            return cellValue
        else:
            return -1
    except:
        return -1

def obtainGleasonScoreFeatures(originalString):
    scoreStrings = set()
    for token1 in str(originalString).split(';'):
        for token2 in token1.split():
            if "+" in token2:
                scoreStrings.add(token2)
    currentMoreDomOutput=-1
    currentLessDomOutput=-1
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
            return -1

def obtainTimeSinceLastProcedure(lastProcedureDateString,currentDateString):
    try:
        currentDate = obtainDateFromString(currentDateString)
        lastProcDate = obtainDateFromString(lastProcedureDateString)
        if(currentDate==-1 or lastProcDate==-1):
            return -1
        timeSinceLast = currentDate-lastProcDate
        return np.abs(timeSinceLast.days)
    except:
        return -1


