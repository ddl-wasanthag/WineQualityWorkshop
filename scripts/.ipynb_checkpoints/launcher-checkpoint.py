import h2o
from h2o.automl import H2OAutoML
import json
import pickle 
import pandas as pd
import random
import sklearn
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error
import os
import sys
 
#Launcher values to set
# split 70 - sys.argv[1]
# max_models=10 - sys.argv[2], max_runtime_secs=30 - sys.argv[3], sort_metric="r2" - sys.argv[4]
 
 
#Set train test split. (set default to 70 in the launcher)
n = int(sys.argv[1])
 
 
#read in data then split into train and test
 
path = str('/domino/datasets/local/{}/WineQualityData.csv'.format(os.environ.get('DOMINO_PROJECT_NAME')))
data = pd.read_csv(path)
print('Read in {} rows of data'.format(data.shape[0]))
 
#Find all pearson correlations of numerical variables with quality
corr_values = data.corr().sort_values(by = 'quality')['quality'].drop('quality',axis=0)
 
#Keep all variables with above a 8% pearson correlation
important_feats=corr_values[abs(corr_values)>0.08]
 
#Get data set up for model training and evaluation
 
#Drop NA rows
data = data.dropna(how='any',axis=0)
#Split df into inputs and target
data = data[list(important_feats.keys())+['quality']]
 
train = data[0:round(len(data)*n/100)]
test = data[train.shape[0]:]
 
print('H2O version -{}'.format(h2o.__version__))
 
#initailize local h2o
h2o.init()
 
 
#Convert data to h2o frames
hTrain = h2o.H2OFrame(train)
hTest = h2o.H2OFrame(test)
 
# Identify predictors and response
x = hTrain.columns
y = "quality"
x.remove(y)
 
# Isolate target vasriable
hTrain[y] = hTrain[y]
hTest[y] = hTest[y]
 
# Run AutoML for 5 base models (limited to 1 min max runtime)
print('Training autoML model...')
aml = H2OAutoML(max_models=int(sys.argv[2]), max_runtime_secs=int(sys.argv[3]), sort_metric=sys.argv[4])
aml.train(x=x, y=y, training_frame=hTrain)
 
 
# sns.histplot(np.array(aml.leader.predict(hTest)))
print('Evaluating model on validation data...')
best_gbm = aml.get_best_model(criterion = 'mse', algorithm = 'gbm') 
preds = best_gbm.predict(hTest)
print(best_gbm.r2(xval=True))
#View performance metrics and save them to domino stats!
r2 = round(best_gbm.r2(xval=True),3)
mse = round(best_gbm.mse(xval=True),3)
print("R2 Score: ", r2)
print("MSE: ", mse)
 
#Code to write R2 value and MSE to dominostats value for population in experiment manager
with open('dominostats.json', 'w') as f:
    f.write(json.dumps({"R2": r2,
                       "MSE": mse}))
 
#Write results to dataframe for viz    
results = pd.DataFrame({'Actuals':test.quality, 'Predictions': preds.as_data_frame()['predict']})
 
print('Creating visualizations...')
#Scatterplot
fig1, ax1 = plt.subplots(figsize=(10,6))
plt.title('H2o Actuals vs Predictions Scatter Plot')
sns.regplot( 
    data=results,
    x = 'Actuals',
    y = 'Predictions',
    order = 3)
plt.savefig('/mnt/visualizations/h2o_actual_v_pred_scatter.png')
 
#Histogram
fig2, ax2 = plt.subplots(figsize=(10,6))
plt.title('h2o Actuals vs Predictions Histogram')
plt.xlabel('Quality')
sns.histplot(results, bins=6, multiple = 'dodge', palette = 'coolwarm')
plt.savefig('/mnt/visualizations/h2o_actual_v_pred_hist.png')
 
#Saving trained model to serialized pickle object 
h2o.save_model(best_gbm, path ='/mnt/models')
 
print('Script complete!')
