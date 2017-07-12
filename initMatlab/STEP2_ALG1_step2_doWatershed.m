%possible numbers are:
% 18, 34, 35, 55, 67
%currentNumber='55';
%folderPath='D:\DATA\SpineCTScans_childrenUnder5_RawMat\';
%fileName=strcat('rawDCM_',currentNumber,'.mat');

folderPath='D:\DATA\PET_CT_SCANS_MAT_FILES';
fileName='PET_CT_Spine_Cases_2015_DONE_cases_11-21_Case_11_PETCT_78815_CT.mat';

fullFilePath=strcat(folderPath,'\',fileName);
dcmArrayHUx = load(fullFilePath);
dcmArrayHU = dcmArrayHUx.dcmArrayHU;


labels=watershed(dcmArrayHU);
imtool3D(labels)

%%

%specific to 55
%(305,405)
%(227,260)