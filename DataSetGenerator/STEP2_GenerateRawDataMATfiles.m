%{
This will generate the raw data volumes for all the patient
    data sets created in Step 1

This must be done first as the segmentation volumes will use 
    information about volume size obtained in this step
%}

GENERATED_DATA_PATH='D:\DATA\SPINE_LESIONS_GENERATED_DATA_SET\';
patientFolders = dir(GENERATED_DATA_PATH);
for folderIndex=1:length(patientFolders)
    folderIndex
    folderName=patientFolders(folderIndex).name;
   if(length(folderName)>4)
       
       currentFolderPath=strcat(GENERATED_DATA_PATH,folderName);
       
       %obtain the file path to the raw DCM data
      textFileWithRawDataLocation=strcat(currentFolderPath,'\FullPathToDataLocation.txt');
      txtFileId = fopen(textFileWithRawDataLocation);
      txtFile1=textscan(txtFileId,'%s','Delimiter','\n');
      currentPathOfRawDCMentry=txtFile1{1,1};
      currentPathOfRawDCM=currentPathOfRawDCMentry{1};
      fclose(txtFileId);
      
      %generate the .mat file with dcm data
      warning('off','all');
      [ ~,~,dcmArrayHU,~,~,dcmInfoArray ] = getDCMFolderData_multiChannel( currentPathOfRawDCM );
      filePathMAT = strcat(currentFolderPath,'\DCM_DATA.mat');
      save(filePathMAT,'dcmArrayHU');
      %save(filePathMAT,'dcmArrayHU','dcmInfoArray');
   end
end