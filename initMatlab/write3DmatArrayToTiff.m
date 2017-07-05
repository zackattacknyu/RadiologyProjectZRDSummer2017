function [] = write3DmatArrayToTiff( dcmArrayHU,fullFilePath )
%WRITE3DMATARRAYTOTIFF Summary of this function goes here
%   Detailed explanation goes here

curImg = reshape(dcmArrayHU(:,:,1),size(dcmArrayHU,1),size(dcmArrayHU,2));
imwrite(curImg,fullFilePath)
for ii=2:size(dcmArrayHU,3)
    curImg = reshape(dcmArrayHU(:,:,ii),size(dcmArrayHU,1),size(dcmArrayHU,2));
    imwrite(curImg,fullFilePath,'WriteMode','append')
end

end

