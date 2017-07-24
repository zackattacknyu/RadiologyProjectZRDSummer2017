import datetime
from datetime import date

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