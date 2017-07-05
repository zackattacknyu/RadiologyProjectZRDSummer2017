saveDirectory = 'D:\DATA\PET_CT_SCANS_MAT_FILES\';

textFileWithDirs = 'D:\dev\PET_CT_Data_Directories.txt';
numLines=179;

ff2=fopen(textFileWithDirs,'r');
allDirs=cell(1,numLines);
tline='a';
index=1;
while(tline~=-1)
    tline=fgetl(ff2);
    allDirs{1,index}=tline;
    index=index+1;
end
allDirs=allDirs(1:end-1);
fclose(ff2);
%%
warning('off','all')
%check file 55 later
for i=56:length(allDirs)
    
    currentdir = allDirs{1,i};
    clearvars -except currentdir allDirs saveDirectory i
    
    fprintf(strcat('Now processing file ',num2str(i),...
        ' of ',num2str(size(allDirs,2)),'\n'));

    [ ~,~,dcmArrayHU,~,~,~ ] = ...
        getDCMFolderData_multiChannel( currentdir );
    
    saveStr = currentdir(27:end);
    saveStr = strrep(saveStr,' ','_');
    saveStr = strrep(saveStr,'\','_');
    
    newFileName = strcat(saveDirectory,saveStr,'.mat');
    save(newFileName,'dcmArrayHU');


end