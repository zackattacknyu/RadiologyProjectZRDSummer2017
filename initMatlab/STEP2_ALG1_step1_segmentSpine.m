folderPath='D:\DATA\PET_CT_SCANS_MAT_FILES';
fileName='PET_CT_Spine_Cases_2015_DONE_cases_11-21_Case_11_PETCT_78815_CT.mat';

fullFilePath=strcat(folderPath,'\',fileName);
dcmArrayHUx = load(fullFilePath);
dcmArrayHU = dcmArrayHUx.dcmArrayHU;

thresholdForBone=200;
bonePixels=double(dcmArrayHU>thresholdForBone);

boneStructure=getLargestComponentImage(bonePixels);

writeMATarrayToTiff(boneStructure,'sampleTiff.tif');