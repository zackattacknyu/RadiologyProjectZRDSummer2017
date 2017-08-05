predictionFolder='D:\DATA\SPINAL_LESIONS_RESULTS\';
originalDataFolder = 'D:/DATA/SPINE_LESIONS_GENERATED_DATA_SET_old/';

pt9file = 'Patient_9_Prediction.mat';
pt12file = 'Patient_12_Prediction.mat';

pt58file = 'Patient_58_Prediction.mat';




%For this patient, slice 94 and 105 have lesions that show up well in
%prediction. Patient Info:
%   Index 22 in Prediction folder
%   Folder 0affd33ex0270x4491x8dcbxca07f616f217
%   in the parent folder SPINE_LESIONS_GENERATED_DATA_SET_old
currentPtPredFile='Patient_22_Prediction.mat';
currentPtOrigDataFolder='0affd33ex0270x4491x8dcbxca07f616f217/';

%sliceNum=94;
%rowRange = 250:350;
%colRange = 200:350;

sliceNum=105;
rowRange = 250:350;
colRange = 200:350;

%{
In slice 180 of the CT scan in this folder there is a large lesion
%}
%currentFolder='D:/DATA/SPINE_LESIONS_GENERATED_DATA_SET_old/1ca9e9efxab7ax4b2fxa0fbx1565ecb72c5d/';

%{
another example: 2dbbde86x8ef8x4e32xb898xc23fcee3a04f
slice 106,129 has a lesion

TO USE: SLICE 157, 158
%}
%currentFolder='D:/DATA/SPINE_LESIONS_GENERATED_DATA_SET_old/2dbbde86x8ef8x4e32xb898xc23fcee3a04f/';

%{
another example: 3b186cb7xd17ax43d8xbb62x597a42342edb
Slide 111,159 has large lesions
Slide 190 has an especially large lesion
%}
%currentFolder='D:/DATA/SPINE_LESIONS_GENERATED_DATA_SET_old/3b186cb7xd17ax43d8xbb62x597a42342edb/';

%{
another one: 3ba57e08x84a0x4d49x8205x57a79d6cad98
slice 97 has lesion

TO USE: SLICE 97, 98
%}
%currentFolder='D:/DATA/SPINE_LESIONS_GENERATED_DATA_SET_old/3ba57e08x84a0x4d49x8205x57a79d6cad98/';

currentFolder=strcat(originalDataFolder,currentPtOrigDataFolder);
patientFullFilePath=strcat(predictionFolder,currentPtPredFile);
patientData=load(patientFullFilePath);
predVolume = patientData.predictionVolume;

boneFile='DCM_DATA_BONE_SEG_MASK.mat';
boneFileFull = strcat(currentFolder,boneFile);
load(boneFileFull)
lesionFile='DCM_DATA_PNT_FILE_LESION_SEG_MASK.mat';
lesionFileFull=strcat(currentFolder,lesionFile);
load(lesionFileFull);
rawData='DCM_DATA.mat';
rawDataFull=strcat(currentFolder,rawData);
load(rawDataFull);

lesionMaskVolume2 = flip(lesionMaskVolume,3); %convert between coord systems
lesionInds = find(lesionMaskVolume2>0);
boneInds = find(boneStructure>0);
boneMaskAtLesions = boneStructure(lesionInds);
numberLesionPixelsInBone = length(find(boneMaskAtLesions>0));

dcmDataWithLesionsUpped = dcmArrayHU;
dcmDataWithLesionsUpped(lesionInds)=2000;

figure
imagesc(dcmArrayHU(rowRange,colRange,sliceNum))
colormap gray
colorbar

figure
imagesc(dcmDataWithLesionsUpped(rowRange,colRange,sliceNum))
colormap gray
colorbar

figure
imagesc(predVolume(rowRange,colRange,sliceNum))
colormap jet
colorbar


%h1=imtool3D(dcmDataWithLesionsUpped);
%setWindowLevel(h1,1500,500);
%h2=imtool3D(dcmArrayHU);
%setWindowLevel(h2,1500,500);

