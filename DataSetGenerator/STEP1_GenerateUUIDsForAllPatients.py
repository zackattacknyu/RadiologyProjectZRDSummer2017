import os
import csv
import uuid
"""

The pnt files with .csv endings have the segmentation data

The script does the following:
1. Generate a UUID for each folder mentioned in a pnt CSV file
2. For each UUID, generate folder and put following text files in it:
    - Location mentioned in pnt file
    - File path to pnt file
    - Full file path to data

"""

def generateUUID():
    #generates a UUID and replaces the dashes with x
    # that way it is completely alphanumeric
    return str(uuid.uuid4()).replace('-','x')

inputDatSetRootPath= 'D:\DATA\PET_Spine_Lesions\PET CT Spine Cases 2015'
outputDataSetRootPath = 'D:\DATA\SPINE_LESIONS_GENERATED_DATA_SET'

outputTablePath = 'D:\DATA\SPINE_LESIONS_GENERATED_DATA_SET_table.csv'
outputTableCSV = open(outputTablePath,'w')
outputTableCSV.write('FolderName,DataPathListedInPntFile,FullPathToRawData,FullPathToPntFile\n')


def processPntFile(pntFilePath):
    print("Now processing " + pntFilePath)
    filePathsInPntFile = set()
    with open(pntFilePath) as csvPntFile:
        csvReader = csv.DictReader(csvPntFile)
        for row in csvReader:
            currentPath = row['CTSeriesName']
            filePathsInPntFile.add(currentPath)

    for dataPath in filePathsInPntFile:
        #check to make sure not empty and not None
        if(dataPath):
            fullPathToData = os.path.join(inputDatSetRootPath, dataPath)
            if(os.path.isdir(fullPathToData)):

                folderName = generateUUID()
                fullFolderPath = os.path.join(outputDataSetRootPath, folderName)
                if not os.path.exists(fullFolderPath):
                    os.makedirs(fullFolderPath)


                fullPathToDataTextFile = os.path.join(fullFolderPath, 'FullPathToDataLocation.txt')
                with open(fullPathToDataTextFile, 'w') as txtFile3:
                    txtFile3.write(fullPathToData)

                locationFromPntTextFile = os.path.join(fullFolderPath,'CTSeriesNameInPntFile.txt')
                with open(locationFromPntTextFile,'w') as txtFile1:
                    txtFile1.write(dataPath)

                pntFileFullPathTextFile = os.path.join(fullFolderPath,'PntFileFullPath.txt')
                with open(pntFileFullPathTextFile,'w') as txtFile2:
                    txtFile2.write(pntFilePath)

                outputTableCSV.write(folderName+","+dataPath+","+fullPathToData+","+pntFilePath+"\n")


def processDirectory(currentRoot):
    files = os.listdir(currentRoot)
    for ff in files:
        currentPath = os.path.join(currentRoot,ff)
        if(os.path.isdir(currentPath)):
            processDirectory(currentPath)

        #Criteria for paint file: has 'pnt' in name and is '.csv' file
        if(currentPath.endswith(".csv") and 'pnt' in ff):
            processPntFile(currentPath)

processDirectory(inputDatSetRootPath)
outputTableCSV.close()
