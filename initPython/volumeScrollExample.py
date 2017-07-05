import dicom
import numpy as np
import os
import matplotlib.pyplot as plt
from scrollTracker import IndexTracker



#dicomPath='sampleDICOMs'
#patFolders = os.listdir(dicomPath)
#pat0FolderPath = os.path.join(dicomPath,patFolders[0])

#pat0FolderPath='D:/dev/PET_Spine_Lesions/PET CT Spine Cases 2015/Case_10_PETCT/PET/Case10_PET'
#pat0FolderPath='D:/dev/Test Subjects-20170629T062439Z-001/Test Subjects/18/run'
#pat0FolderPath = 'D:/dev/Test Subjects-20170629T062439Z-001/Test Subjects/35/35 cut'
pat0FolderPath='D:/dev/SpineCTScans_childrenUnder5/TestSubjects/34/34 cut'

pat0FolderDCMFilesX = os.listdir(pat0FolderPath)
pat0FolderDCMFiles = [file1 for file1 in pat0FolderDCMFilesX if file1.endswith(".dcm")]

totalNumFiles = len(pat0FolderDCMFiles)
patDCMimage = os.path.join(pat0FolderPath, pat0FolderDCMFiles[0])
image0File = dicom.read_file(patDCMimage)._pixel_data_numpy()
image0FileShape = image0File.shape



ctScanVolume = np.zeros((image0FileShape[0],image0FileShape[1],totalNumFiles))

sliceLocations = []
dictOfSliceLocations = {}
for dcmFileIndex in range(totalNumFiles):
    currentDCMimageFile = os.path.join(pat0FolderPath, pat0FolderDCMFiles[dcmFileIndex])
    currentDCMimage = dicom.read_file(currentDCMimageFile)
    currentSliceLocation = float(currentDCMimage.SliceLocation)
    sliceLocations.append(currentSliceLocation)
    dictOfSliceLocations[currentSliceLocation] = dcmFileIndex

sliceLocationsSorted = np.sort(np.array(sliceLocations))

for sliceIndex in range(len(sliceLocationsSorted)):
    currentSliceLoc = sliceLocationsSorted[sliceIndex]
    fileIndexOfSlice = dictOfSliceLocations[currentSliceLoc]
    currentDCMimageFile = os.path.join(pat0FolderPath, pat0FolderDCMFiles[fileIndexOfSlice])
    currentDCMimage = dicom.read_file(currentDCMimageFile)
    ctScanVolume[:,:,sliceIndex] = currentDCMimage._pixel_data_numpy()

minValue = np.min(ctScanVolume)
maxValue = np.max(ctScanVolume)

fig, ax = plt.subplots(1, 1)
tracker = IndexTracker(ax, ctScanVolume)
fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
fig.colorbar(tracker.im,ticks=np.linspace(minValue,maxValue,num=10))
plt.show()