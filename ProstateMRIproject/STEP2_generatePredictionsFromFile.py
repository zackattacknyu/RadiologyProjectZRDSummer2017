import os
import xgboost as xgb
import DataSetLogic
import numpy as np
from sklearn import cross_validation

FOLDER_PATH = "/home/exx/Documents/workspace/zachworkspace/GENERATED_FILES_FOR_ROU"
DATA_FILE_NAME='FINAL_DATA_SET.npy'
FULL_FILE_PATH = os.path.join(FOLDER_PATH,DATA_FILE_NAME)

MISSING_DATA_FLOAT_VALUE = DataSetLogic.MISSING_DATA_FLOAT_VALUE

dataFromExcel = np.load(FULL_FILE_PATH)


"""
TO CHANGE:
    PUT WHICHEVER FEATURES YOU WANT TO CONSIDER INTO HERE
"""
featureColumns = [0,1,9,10,14]
columnToPredict = 35


Xdata = np.zeros((dataFromExcel.shape[0],len(featureColumns)))
for colIndex in range(len(featureColumns)):
    Xdata[:,colIndex]=dataFromExcel[:,featureColumns[colIndex]]

yData = dataFromExcel[:,columnToPredict]

validRows0 = np.where(yData!=MISSING_DATA_FLOAT_VALUE)
validRows = validRows0[0]

yDataValid = yData[validRows]
xDataValid = Xdata[validRows,:]

trn_x, val_x, trn_y, val_y = cross_validation.train_test_split(
    xDataValid, yDataValid, random_state=42, stratify=yDataValid,test_size=0.20)

#Traditional Classifier Below
#
# clf = xgb.XGBClassifier(max_depth=30,missing=MISSING_DATA_FLOAT_VALUE,
#                        n_estimators=1500,
#                        min_child_weight=9,
#                        learning_rate=0.05,
#                        nthread=8,
#                        subsample=0.80,
#                        colsample_bytree=0.80,
#                        seed=4242)
# clf.fit(trn_x, trn_y, eval_set=[(val_x, val_y)], verbose=True,
#     eval_metric='mae', early_stopping_rounds=100)

#Regression prediction
#   This provides us a score
clf = xgb.XGBRegressor(max_depth=30,missing=MISSING_DATA_FLOAT_VALUE,
                       n_estimators=1500,
                       min_child_weight=9,
                       learning_rate=0.05,
                       nthread=8,
                       subsample=0.80,
                       colsample_bytree=0.80,
                       seed=4242)
clf.fit(trn_x, trn_y, eval_set=[(val_x, val_y)], verbose=True,
    eval_metric='mae', early_stopping_rounds=100)
