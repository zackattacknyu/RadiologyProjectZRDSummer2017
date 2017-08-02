"""
This will do the one-hot encoding
    for the different types of category values
"""

import DataSetLogic
import numpy as np

def categoryToOneHot_WithStartCatNum(columnVector,numCategories,valueIfBoth,valueIfNeither,
                                     initCategoryNumber):
    outputArray = np.zeros((len(columnVector), numCategories))
    for rowInd in range(len(columnVector)):
        currentCatValue = columnVector[rowInd]
        if (currentCatValue < 0):
            outputArray[rowInd, :] = np.ones((1, numCategories)) * DataSetLogic.MISSING_DATA_FLOAT_VALUE
        elif (valueIfBoth > 0 and currentCatValue == valueIfBoth):
            outputArray[rowInd, :] = np.ones((1, numCategories))
        elif (valueIfNeither > 0 and currentCatValue == valueIfNeither):
            outputArray[rowInd, :] = np.zeros((1, numCategories))
        else:
            outputArray[rowInd, currentCatValue - initCategoryNumber] = 1
    return outputArray

def categoryToOneHotNoBothNeither(columnVector,numCategories):
    return categoryToOneHotFeature(columnVector,numCategories,DataSetLogic.MISSING_DATA_FLOAT_VALUE,DataSetLogic.MISSING_DATA_FLOAT_VALUE)

def categoryToOneHotFeature(columnVector,numCategories,valueIfBoth,valueIfNeither):
    return categoryToOneHot_WithStartCatNum(columnVector,numCategories,
                                            valueIfBoth,valueIfNeither,1)

def categoryToOneHotFeatureZeroStart(columnVector,numCategories,valueIfBoth,valueIfNeither):
    return categoryToOneHot_WithStartCatNum(columnVector,numCategories,
                                            valueIfBoth,valueIfNeither,0)

def autoGeneratedCategoryToOneHot(columnVector,missingDataStrs):
    columnValues =[]
    for val in columnVector:
        if(val):
            try:
                columnValues.append(str(val).lower())
            except:
                columnValues.append('none')
        else:
            columnValues.append('none')
    uniqueValues = DataSetLogic.obtainUniqueEntries(columnValues)
    generatedCategoryDict = {}
    currentIndex=0
    for value in uniqueValues:
        notMissing = True
        for missingStr in missingDataStrs:
            if(value in missingStr):
                notMissing = False
        if(notMissing):
            generatedCategoryDict[value]=currentIndex
            currentIndex = currentIndex+1
    outputColumnNumbers = []
    for entry in columnVector:
        outputColumnNumbers.append(
            DataSetLogic.obtainCategoryFieldValueWithMissingDataIndicators(
                entry,generatedCategoryDict,missingDataStrs))
    outputColVector = np.array(outputColumnNumbers)
    categoryMatrix = categoryToOneHotFeatureZeroStart(
        outputColVector,np.max(outputColVector)+1,
        DataSetLogic.MISSING_DATA_FLOAT_VALUE,DataSetLogic.MISSING_DATA_FLOAT_VALUE)
    return categoryMatrix,outputColVector,generatedCategoryDict


"""
If "prostatectomy" or "surgery" is in the string then category 1: 
    prostatectonmy/surgery
If "cryo" then label is 2
Otherwise label is 0
"""
def columnFMlogic(columnVector):
    columnFeatureValues = []
    for value in columnVector:
        value0=str(value)
        if('prostatectomy' in value0 or 'surgery' in value0):
            columnFeatureValues.append(1)
        elif('cryo' in value0):
            columnFeatureValues.append(2)
        else:
            columnFeatureValues.append(0)
    return np.array(columnFeatureValues)

"""
For FN, if word "brachytherapy" or "radiotherapy" or "seed"
    or "radiation" label them as 1
    If string is just "1" label it as 1
all others label 0
"""
def columnFNlogic(columnVector):
    colFeatureVals = []
    for val0 in columnVector:
        val = str(val0)
        if('brachytherapy' in val or 'radiotherapy' in val
           or 'seed' in val or 'radiation' in val or val in '1'):
            colFeatureVals.append(1)
        else:
            colFeatureVals.append(0)
    colVector = np.array(colFeatureVals)
    return colVector

"""
If FK is 1, then others are 0
Otherwise if any other is 1, FK is zero
This enforces that rule
"""
def applyFKtoFNrule(colFK,colFL,colFM,colFN):
    for index0 in range(len(colFK)):
        if(colFK[index0]==1):
            colFL[index0]=0
            colFM[index0]=0
            colFN[index0]=0
        elif(colFL[index0]==1 or colFM[index0]==1 or colFN[index0]==1):
            colFK[index0]=0
    return colFK,colFL,colFM,colFN

"""
If contains "negative" then 0
If contains "positive" then 1
Otherwise missing
"""
def columnFTlogic(columnVector):
    columnFeatureValues = []
    for value in columnVector:
        value0=str(value)
        if('negative' in value0):
            columnFeatureValues.append(0)
        elif('positive' in value0):
            columnFeatureValues.append(1)
        else:
            columnFeatureValues.append(DataSetLogic.MISSING_DATA_FLOAT_VALUE)
    return np.array(columnFeatureValues)