function [] = writeMATarrayToTiff( dcmArrayHU,fullFilePath )
%WRITEMATARRAYTOTIFF Summary of this function goes here
%   Detailed explanation goes here

if(numel(size(dcmArrayHU))==3)
    %write TIFF file
    write3DmatArrayToTiff(dcmArrayHU,fullFilePath);
elseif(numel(size(dcmArrayHU))==4)
    pathWoExtension = fullFilePath(1:end-4);
    for ii=1:size(dcmArrayHU,3)
       currentFullPath = strcat(pathWoExtension,'_channel',num2str(ii),'.tif');       
       dcmArrayHUchannel = dcmArrayHU(:,:,ii,:);
       dcmArrayHUchannel = reshape(dcmArrayHUchannel,...
           size(dcmArrayHU,1),size(dcmArrayHU,2),size(dcmArrayHU,4));
       write3DmatArrayToTiff(dcmArrayHUchannel,currentFullPath);
    end
end

end

