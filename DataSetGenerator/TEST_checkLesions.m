currentFolder='D:/DATA/SPINE_LESIONS_GENERATED_DATA_SET_old/0affd33ex0270x4491x8dcbxca07f616f217/';

%{
In slice 128, there seems to be lesion and the shape of the lesion mask
    appears to be correct, however the location of the lesion mask appears
    incorrect. 
TODO: CHECK the row, column coord system in pnt files
%}


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

lesionInds = find(lesionMaskVolume>0);
boneInds = find(boneStructure>0);
boneMaskAtLesions = boneStructure(lesionInds);
numberLesionPixelsInBone = length(find(boneMaskAtLesions>0));

dcmDataWithLesionsUpped = dcmArrayHU;
dcmDataWithLesionsUpped(lesionInds)=2000;



imtool3D(dcmDataWithLesionsUpped)
imtool3D(dcmArrayHU)

dcmDataWithBonesUpped = dcmArrayHU;
dcmDataWithBonesUpped(boneInds)=2000;
imtool3D(dcmDataWithBonesUpped);

%%
initFolder='D:\DATA\PET_Spine_Lesions\PET CT Spine Cases 2015\';
initPtFolder='Case_23_PETCT\78815-\CT\';
firstDCM='IM-0001-43091568-0001.dcm';
fullFilePath1 = strcat(initFolder,initPtFolder,firstDCM);
info=dicominfo(fullFilePath1);

%%

%{
Note: This DOES NOT work. It is not a matter of flipping the up-down coords.
Need to do more investigation into why there's an
offset
%}
dcmDataWithLesionsUpped2 = dcmArrayHU;
%dcmDataWithLesionsUpped2(flipud(lesionMaskVolume)>0)=2000;

%Pixel Spacing is 1.3672
%seeing if that is part of the reason for the offset
for sli = 1:size(lesionMaskVolume,3)
    for row=1:size(lesionMaskVolume,1)
       for col=1:size(lesionMaskVolume,2)
            if(lesionMaskVolume(row,col,sli)>0)
               rowN = floor(row/1.3672);
               colN = floor(col/1.3672);
               dcmDataWithLesionsUpped2(rowN,colN,sli)=2000;
            end
       end
    end
end
imtool3D(dcmDataWithLesionsUpped2);