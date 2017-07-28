"""
This will do the one-hot encoding
    for the different types of category values
"""


import numpy as np

def categoryToOneHot_WithStartCatNum(columnVector,numCategories,valueIfBoth,valueIfNeither,
                                     initCategoryNumber):
    outputArray = np.zeros((len(columnVector), numCategories))
    for rowInd in range(len(columnVector)):
        currentCatValue = columnVector[rowInd]
        if (currentCatValue < 0):
            outputArray[rowInd, :] = np.ones((1, numCategories)) * -1
        elif (valueIfBoth > 0 and currentCatValue == valueIfBoth):
            outputArray[rowInd, :] = np.ones((1, numCategories))
        elif (valueIfNeither > 0 and currentCatValue == valueIfNeither):
            outputArray[rowInd, :] = np.zeros((1, numCategories))
        else:
            outputArray[rowInd, currentCatValue - initCategoryNumber] = 1
    return outputArray

def categoryToOneHotNoBothNeither(columnVector,numCategories):
    return categoryToOneHotFeature(columnVector,numCategories,-1,-1)

def categoryToOneHotFeature(columnVector,numCategories,valueIfBoth,valueIfNeither):
    return categoryToOneHot_WithStartCatNum(columnVector,numCategories,
                                            valueIfBoth,valueIfNeither,1)

def categoryToOneHotFeatureZeroStart(columnVector,numCategories,valueIfBoth,valueIfNeither):
    return categoryToOneHot_WithStartCatNum(columnVector,numCategories,
                                            valueIfBoth,valueIfNeither,0)