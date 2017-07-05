
%for the PET/CT data

folderOfFiles='D:\DATA\PET_CT_SCANS_MAT_FILES\';

outputFolder = 'D:\DATA\PET_CT_SCANS_TIFF_FILES\';

%open mat file data of PET or CT
allMatFiles = dir(folderOfFiles);

for ii = 1:length(allMatFiles)
    ii
    
    fullPath=strcat(folderOfFiles,allMatFiles(ii).name);
    
    if(strcmp( fullPath(end-3:end) , '.mat' ))
        
        fileData = load(fullPath);
        dcmArrayHU = fileData.dcmArrayHU;
        
        fileNameWoExtension = allMatFiles(ii).name(1:end-4);
        outputFileFullPath = strcat(outputFolder,fileNameWoExtension,'_tiffVolume.tif');

        writeMATarrayToTiff( dcmArrayHU,outputFileFullPath )
        
    end
    
    

end