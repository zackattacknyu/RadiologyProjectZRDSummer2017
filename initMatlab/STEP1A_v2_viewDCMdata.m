
%for the PET/CT data

%{
folderPath='D:\DATA\PET_CT_SCANS_MAT_FILES\';
currentFile=...
    'Anonymized_-_1307756_78815-PS_PET-CT_Tumor_Image_Skull-Thi_FDG_PET-CT_FUSED_-_501.mat';
fullPath = strcat(folderPath,currentFile);
%}

%open mat file data of PET or CT
[filename,pathname]=uigetfile('*.mat','Select MAT file of PET/CT block');
fullPath=strcat(pathname,'/',filename);
fileData = load(fullPath);
dcmArrayHU = fileData.dcmArrayHU;

if(numel(size(dcmArrayHU))==3)
    imtool3D(dcmArrayHU)
    %write TIFF file
    curImg = reshape(dcmArrayHU(:,:,1),size(dcmArrayHU,1),size(dcmArrayHU,2));
    imwrite(curImg,'sampleTiff.tif')
    for ii=2:size(dcmArrayHU,3)
        curImg = reshape(dcmArrayHU(:,:,ii),size(dcmArrayHU,1),size(dcmArrayHU,2));
        imwrite(curImg,'sampleTiff.tif','WriteMode','append')
    end
elseif(numel(size(dcmArrayHU))==4)
    for ii=1:size(dcmArrayHU,3)
       dcmArrayHUchannel = dcmArrayHU(:,:,ii,:);
       dcmArrayHUchannel = reshape(dcmArrayHUchannel,...
           size(dcmArrayHU,1),size(dcmArrayHU,2),size(dcmArrayHU,4));
       imtool3D(dcmArrayHUchannel);
    end
end
