predictionFolder='D:\DATA\SPINAL_LESIONS_RESULTS\';

pt9file = 'Patient_9_Prediction.mat';
pt12file = 'Patient_12_Prediction.mat';
pt22file = 'Patient_22_Prediction.mat';
pt58file = 'Patient_58_Prediction.mat';

currentPtFile = pt22file;

patientFullFilePath=strcat(predictionFolder,currentPtFile);
patientData=load(patientFullFilePath);
predVolume = patientData.predictionVolume;

imtool3D(predVolume)