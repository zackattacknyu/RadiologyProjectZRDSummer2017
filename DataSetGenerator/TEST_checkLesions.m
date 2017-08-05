%MAKE WINDOW 1500, MAKE LEVEL 500 to see the contrast

%{
In slice 128, there seems to be lesion and the shape of the lesion mask
    appears to be correct, however the location of the lesion mask appears
    incorrect. 
%fixed now
%slice 127-129
%Patient 22
%}
%currentFolder='D:/DATA/SPINE_LESIONS_GENERATED_DATA_SET_old/0affd33ex0270x4491x8dcbxca07f616f217/';

%{
In slice 180 of the CT scan in this folder there is a large lesion
%}
%currentFolder='D:/DATA/SPINE_LESIONS_GENERATED_DATA_SET_old/1ca9e9efxab7ax4b2fxa0fbx1565ecb72c5d/';

%{
another example: 2dbbde86x8ef8x4e32xb898xc23fcee3a04f
slice 106,129 has a lesion

TO USE: SLICE 157, 158
%}
currentFolder='D:/DATA/SPINE_LESIONS_GENERATED_DATA_SET_old/2dbbde86x8ef8x4e32xb898xc23fcee3a04f/';

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

boneFile='DCM_DATA_BONE_SEG_MASK.mat';
boneFileFull = strcat(currentFolder,boneFile);
load(boneFileFull)
lesionFile='DCM_DATA_PNT_FILE_LESION_SEG_MASK.mat';
lesionFileFull=strcat(currentFolder,lesionFile);
load(lesionFileFull);
%imtool3D(boneStructure);
%imtool3D(lesionMaskVolume);
rawData='DCM_DATA.mat';
rawDataFull=strcat(currentFolder,rawData);
load(rawDataFull);
%imtool3D(dcmArrayHU);

lesionMaskVolume2 = flip(lesionMaskVolume,3); %convert between coord systems
lesionInds = find(lesionMaskVolume2>0);
boneInds = find(boneStructure>0);
boneMaskAtLesions = boneStructure(lesionInds);
numberLesionPixelsInBone = length(find(boneMaskAtLesions>0));

dcmDataWithLesionsUpped = dcmArrayHU;
dcmDataWithLesionsUpped(lesionInds)=2000;



h1=imtool3D(dcmDataWithLesionsUpped);
setWindowLevel(h1,1500,500);
h2=imtool3D(dcmArrayHU);
setWindowLevel(h2,1500,500);

dcmDataWithBonesUpped = dcmArrayHU;
dcmDataWithBonesUpped(boneInds)=2000;
%imtool3D(dcmDataWithBonesUpped);

%%
initFolder='D:\DATA\PET_Spine_Lesions\PET CT Spine Cases 2015\';
initPtFolder='Case_23_PETCT\78815-\CT\';
firstDCM='IM-0001-43091568-0001.dcm';
fullFilePath1 = strcat(initFolder,initPtFolder,firstDCM);
info=dicominfo(fullFilePath1);

%%
%flipping the slice coordinates to see if that is the problem
%   IT WAS THE PROBLEM!
%{
numSlice=size(lesionMaskVolume,3);
for sli = 1:size(lesionMaskVolume,3)
    for row=1:size(lesionMaskVolume,1)
       for col=1:size(lesionMaskVolume,2)
            if(lesionMaskVolume(row,col,sli)>0)
               dcmDataWithLesionsUpped2(row,col,numSlice-sli+1)=2000;
            end
       end
    end
end
imtool3D(dcmDataWithLesionsUpped2);
%}