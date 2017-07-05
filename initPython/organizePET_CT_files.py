import os

rootPath='D:\DATA\PET_Spine_Lesions'

allDCMpaths = []

def processDirectory(currentRoot):
    files = os.listdir(currentRoot)
    for ff in files:
        currentPath = os.path.join(currentRoot,ff)
        if(os.path.isdir(currentPath)):
            processDirectory(currentPath)
        if(currentPath.endswith(".dcm")):
            allDCMpaths.append(currentRoot)
            break

processDirectory(rootPath)



with open('dcmDirectories.txt','w') as filePathTextFile:
    for mypath in allDCMpaths:
        filePathTextFile.write(mypath + "\n")
