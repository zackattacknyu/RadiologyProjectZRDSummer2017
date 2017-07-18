import csv
import os
import matplotlib.path as mplPath
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio


folderPath='D:/DATA/PET_Spine_Lesions/PET CT Spine Cases 2015'

#has data on the centroids of lesions
fileName = 'PET_CT_Cases_UC_MixedLesionsCT_v17.csv'

#has data on the segmentation boundaries
"""
The csv file contains information about which folder
    contains the data as well as the important
    segmentation information
TODO: assemble the segmentation data set
    using this CSV file. Once I have a proper data
    set, begin using CNN to see if segmentation
    can be done using it. 
"""
fileName2 = 'Case5_PETR_pnt.csv'

csvFileFullPath = os.path.join(folderPath,fileName2)
rows = []

#key is patient key. value is matrix of all seg coords
dictOfSegCoords = {}

with open(csvFileFullPath) as csvFile:
    ourReader = csv.DictReader(csvFile)
    for row in ourReader:
        currentPtKey = row['CTSeriesName']
        currentSlice = int(row['CTSlice'])
        currentCol = int(row['CTColumn'])
        currentRow = int(row['CTRow'])
        currentXYcoords = [currentRow,currentCol]
        if(currentPtKey not in dictOfSegCoords):
            dictOfSegCoords[currentPtKey]={}
        if(currentSlice not in dictOfSegCoords[currentPtKey]):
            dictOfSegCoords[currentPtKey][currentSlice]=[]
        dictOfSegCoords[currentPtKey][currentSlice].append(currentXYcoords)


sliceSizeRow = 512
sliceSizeCol = 512

for currentPtKey in dictOfSegCoords:

    maxSliceNumber = np.max(np.array(dictOfSegCoords[currentPtKey].keys()))+1

    segmentedVolume = np.zeros((sliceSizeRow,sliceSizeCol,maxSliceNumber))

    for sliceNum in dictOfSegCoords[currentPtKey]:
        print(sliceNum)
        polyPts = dictOfSegCoords[currentPtKey][sliceNum]
        polyPts.append(polyPts[0])
        polyPtsArray = np.array(polyPts)

        polygonPath = mplPath.Path(polyPtsArray)

        #fills in the path of the polygon
        matrixArray = np.zeros((sliceSizeRow,sliceSizeCol))
        for ii in range(sliceSizeRow):
            for jj in range(sliceSizeCol):
                if(polygonPath.contains_point([ii,jj])):
                    matrixArray[ii,jj]=1

        #fills in the polygon
        for ii in range(sliceSizeRow):
            currentRow=matrixArray[ii]
            rowData=np.where(currentRow>0)
            rowData=rowData[0]
            if(len(rowData)>0):
                minIndex = np.min(rowData)
                maxIndex = np.max(rowData)
                matrixArray[ii,minIndex:maxIndex]=1

        segmentedVolume[:,:,sliceNum]=matrixArray

    fileName=currentPtKey.replace("\\","__")

    sio.savemat(fileName+'_segVolume.mat',{"segVolume":segmentedVolume})