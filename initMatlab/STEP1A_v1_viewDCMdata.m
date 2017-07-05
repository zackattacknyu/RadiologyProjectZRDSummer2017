%possible numbers are:
% 18, 34, 35, 55, 67
currentNumber='55';

folderPath='D:\DATA\SpineCTScans_childrenUnder5_RawMat\';

fileName=strcat('rawDCM_',currentNumber,'.mat');
fullFilePath=strcat(folderPath,'\',fileName);
dcmArrayHUx = load(fullFilePath);
dcmArrayHU = dcmArrayHUx.dcmArrayHU;


imtool3D(dcmArrayHU);


