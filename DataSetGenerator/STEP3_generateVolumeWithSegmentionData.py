import csv
import os
import matplotlib.path as mplPath
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio


folderPath='D:\DATA\SPINE_LESIONS_GENERATED_DATA_SET'

patientFolders = os.listdir(folderPath)

displayInd=0
for ptFolder in patientFolders:
    displayInd= displayInd + 1

    print("Beginning process for pt " + str(displayInd))

    currentFullPath = os.path.join(folderPath,ptFolder)
    currentTxtFile = os.path.join(currentFullPath,'PntFileFullPath.txt')
    pntFileFullPath=open(currentTxtFile).read()

    currentSeriesNameTxtFile = os.path.join(currentFullPath,'CTSeriesNameInPntFile.txt')
    seriesName=open(currentSeriesNameTxtFile).read()

    #has data on the segmentation boundaries
    """
    The csv file contains information about which folder
        contains the data as well as the important
        segmentation information
    """

    #key is patient key. value is matrix of all seg coords
    dictOfSegCoords = {}

    print("Opening CSV file for pt " + str(displayInd))

    with open(pntFileFullPath) as csvFile:
        ourReader = csv.DictReader(csvFile)
        for row in ourReader:
            currentPtKey = row['CTSeriesName']
            if(seriesName in currentPtKey):
                currentSlice = int(row['CTSlice'])
                currentCol = int(row['CTColumn'])
                currentRow = int(row['CTRow'])
                currentXYcoords = [currentRow,currentCol]
                if(currentSlice not in dictOfSegCoords):
                    dictOfSegCoords[currentSlice]=[]
                dictOfSegCoords[currentSlice].append(currentXYcoords)

    print("Obtaining MAT data for pt " + str(displayInd))

    matlabFilePath = os.path.join(currentFullPath,'DCM_DATA.mat')
    matlabData = sio.loadmat(matlabFilePath)
    rawDataArray = matlabData['dcmArrayHU']
    volumeShape = rawDataArray.shape

    segmentedVolume = np.zeros(volumeShape)

    print("Now generating the volume for Pt " + str(displayInd))

    innerLoopIndex=1
    for sliceNum in dictOfSegCoords:

        print("Now making slice " + str(innerLoopIndex) + " of " + str(len(dictOfSegCoords)))
        innerLoopIndex = innerLoopIndex+1

        polyPts = dictOfSegCoords[sliceNum]
        polyPts.append(polyPts[0])
        polyPtsArray = np.array(polyPts)

        polygonPath = mplPath.Path(polyPtsArray)

        #fills in the path of the polygon
        matrixArray = np.zeros((volumeShape[0],volumeShape[1]))
        for ii in range(volumeShape[0]):
            for jj in range(volumeShape[1]):
                if(polygonPath.contains_point([ii,jj])):
                    matrixArray[ii,jj]=1

        #fills in the polygon
        for ii in range(volumeShape[0]):
            currentRow=matrixArray[ii]
            rowData=np.where(currentRow>0)
            rowData=rowData[0]
            if(len(rowData)>0):
                minIndex = np.min(rowData)
                maxIndex = np.max(rowData)
                matrixArray[ii,minIndex:maxIndex]=1

        segmentedVolume[:,:,sliceNum]=matrixArray

    outputFileFullPath=os.path.join(currentFullPath,'DCM_DATA_SEGMENTATION_VOLUME.mat')

    sio.savemat(outputFileFullPath,{"segVolume":segmentedVolume})

    print("Finished generating volume for Pt " + str(displayInd))