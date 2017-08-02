import numpy as np
import os
import scipy.io as sio

folderPath='D:\DATA\SPINE_LESIONS_GENERATED_DATA_SET'

rawDICOMfileName = 'DCM_DATA.mat'

nm='D:/DATA/SPINE_LESIONS_GENERATED_DATA_SET/0affd33ex0270x4491x8dcbxca07f616f217/DCM_DATA.mat'
#nm='D:/DATA/SPINE_LESIONS_GENERATED_DATA_SET/0affd33ex0270x4491x8dcbxca07f616f217/DCM_DATA_BONE_SEG_MASK.mat'

vv=sio.loadmat(nm)
print(vv)


# patientFolders = os.listdir(folderPath)
#
# displayInd=0
# for dIndex in range(len(patientFolders)):
#     currentPt = patientFolders[dIndex]
