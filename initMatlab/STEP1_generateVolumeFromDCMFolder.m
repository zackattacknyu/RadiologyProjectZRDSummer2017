dirName = 'D:\DATA\SpineCTScans_childrenUnder5';

dcmFolders = dir(dirName);
numFolders = size(dcmFolders,1);

for i = 1:numFolders
    
    clearvars -except dcmFolders numFolders dirName i
    
    foldname = dcmFolders(i,1).name;
    curSampleFolder = strcat(dirName,'/',foldname);
    if(isempty(str2num(foldname)))
       continue; %do not include it 
    end
    
    fprintf(strcat('Now processing file ',num2str(i),' of ',num2str(numFolders),'\n'));

    %[ dcmData,dcmArray,dcmArrayHU,slope,intercept,dcmInfo ] = ...
    [ ~,~,dcmArrayHU,~,~,~ ] = ...
        getDCMFolderData( curSampleFolder );

    
    newFileName = strcat(...
        'D:/DATA/SpineCTScans_childrenUnder5_RawMat/rawDCM_',...
        foldname);
    save(newFileName,'dcmArrayHU');
    
    
    %{
    niiFileName = strcat(...
        'D:/DATA/SpineCTScans_childrenUnder5_RawMat',...
        '/niiFileRawDCM_',...
        foldname,'.nii');
    niiFixed = make_nii(dcmArrayHU);
    save_nii(niiFixed,niiFileName);
    %}
    
    

end