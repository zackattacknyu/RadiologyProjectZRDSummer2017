fileNumber=161;

initPath='D:\DATA\PET_Spine_Lesions\PET CT Spine Cases 2015\';
specificPath='Case_5_PETCT\\PET-CT\\Case5_PETR\\';
fullFilePath=strcat(initPath,specificPath,'I0000',num2str(fileNumber),'.dcm');

dicomData=dicomread(fullFilePath);

imagesc(dicomData)
colorbar


