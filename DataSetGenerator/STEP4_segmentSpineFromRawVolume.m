%{
This takes the raw data .mat files and segments out the bones.
It makes a max of everything with > 200 HU
It then takes the largest connected component of pixels 
    and that is considered the bone
%}

GENERATED_DATA_PATH='D:\DATA\SPINE_LESIONS_GENERATED_DATA_SET\';
patientFolders = dir(GENERATED_DATA_PATH);
for folderIndex=1:length(patientFolders)
    folderIndex
    folderName=patientFolders(folderIndex).name;
   if(length(folderName)>4)
       
       currentFolderPath=strcat(GENERATED_DATA_PATH,folderName);
       
       warning('off','all');
       filePathMAT = strcat(currentFolderPath,'\DCM_DATA.mat');
       
       if(exist(filePathMAT,'file'))
          
           dcmArrayHUx = load(filePathMAT);
            dcmArrayHU = dcmArrayHUx.dcmArrayHU;

            thresholdForBone=200;
            bonePixels=double(dcmArrayHU>thresholdForBone);

            boneStructure=getLargestComponentImage(bonePixels);
            
            filePathMAT2 = strcat(currentFolderPath,'\DCM_DATA_BONE_SEG_MASK.mat');
            save(filePathMAT2,'boneStructure');
           
           
       end
       

   end
end