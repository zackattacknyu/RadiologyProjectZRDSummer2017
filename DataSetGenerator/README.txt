This contains matlab and python code
To generate the data set, the scripts must be run in the step order specified.
As of now, they are put into "D:\DATA\GENERATED_DATA_SET" 

"STEP1_..." generates the UUIDs for all patients with paint files
	It also generates text files describing the data locations
	
"STEP2_..." takes all those patients and makes a .mat file
	of all the raw HU data 
	
"STEP3_..." generates the segmented volume .mat file. The dimensions
	are the same as the raw HU data and each voxel says whether or not
	there is a lesion

"step4_..." does the same thing as step 3 but says whether or not there 
	is a bone voxel 

"STEP5_..." resaves the files from STEP3 using Matlab. This will 
	considerably lower the space that the data set uses
	
	
The file "TEST_checkLesions.mat" will show the 3D volume of the CT
	data and the lesions
The file "TEST_checkPredictions.mat" will show the 3D volume of the 
	cancer scores
NOTE: Before using these, you must add the folder "imtool3D" 
	to the path by right clicking on it in Matlab and selecting 
	"Add to Path"

The file "RESULT_FIGURES_showPredictionSlices.mat" 
	generates the pictures of the slices with 
	CT data, overlay of tumor, and prediction score. 