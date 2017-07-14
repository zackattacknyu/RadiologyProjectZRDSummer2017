import csv
import os


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
        currentSRCcoords = [currentSlice,currentRow,currentCol]
        if(currentPtKey not in dictOfSegCoords):
            dictOfSegCoords[currentPtKey]=[]
        dictOfSegCoords[currentPtKey].append(currentSRCcoords)

print(dictOfSegCoords.keys())

