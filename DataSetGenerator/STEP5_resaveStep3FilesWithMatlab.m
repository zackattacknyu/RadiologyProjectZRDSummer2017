%{
This takes the .mat files generated in python
    for the segmentation volume and resaves them

The space use goes from 600 MB to 240 KB in one example
    when doing the change
%}

GENERATED_DATA_PATH='D:\DATA\SPINE_LESIONS_GENERATED_DATA_SET\';
patientFolders = dir(GENERATED_DATA_PATH);
for folderIndex=1:length(patientFolders)
    folderIndex
    folderName=patientFolders(folderIndex).name;
   if(length(folderName)>4)
       
       currentFolderPath=strcat(GENERATED_DATA_PATH,folderName);
       
       warning('off','all');
       filePathMAT = strcat(currentFolderPath,'\DCM_DATA_SEGMENTATION_VOLUME.mat');
       
       if(exist(filePathMAT,'file'))
          
           segArrayX = load(filePathMAT);
            lesionMaskVolume = segArrayX.segVolume;
            
            filePathMAT2 = strcat(currentFolderPath,'\DCM_DATA_PNT_FILE_LESION_SEG_MASK.mat');
            save(filePathMAT2,'lesionMaskVolume');
            
            delete(filePathMAT);
           
           
       end
       

   end
end