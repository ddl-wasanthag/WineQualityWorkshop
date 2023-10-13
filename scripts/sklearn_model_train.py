import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import json
import os

#Read in data
path = str('/domino/datasets/local/{}/WineQualityData.csv'.format(os.environ.get('DOMINO_PROJECT_NAME')))
df = pd.read_csv(path)
print('Read in {} rows of data'.format(df.shape[0]))

#rename columns to remove spaces
for col in df.columns:
    df.rename({col: col.replace(' ', '_')}, axis =1, inplace = True)

#Create is_red variable to store red/white variety as int    
df['is_red'] = df.type.apply(lambda x : int(x=='red'))

#Find all pearson correlations of numerical variables with quality
corr_values = df.corr().sort_values(by = 'quality')['quality'].drop('quality',axis=0)

#Keep all variables with above a 8% pearson correlation
important_feats=corr_values[abs(corr_values)>0.08]

#Get data set up for model training and evaluation

#Drop NA rows
df = df.dropna(how='any',axis=0)
#Split df into inputs and target
X = df[important_feats.keys()]
y = df['quality'].astype('float64')
#Create 70/30 train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#initiate and fit Gradient Boosted Classifier
print('Training model...')
gbr = GradientBoostingRegressor(loss='ls',learning_rate = 0.15, n_estimators=75, criterion = 'mse')
gbr.fit(X_train,y_train)

#Predict test set
print('Evaluating model on test data...')
preds = gbr.predict(X_test)

#View performance metrics and save them to domino stats!
print("R2 Score: ", round(r2_score(y_test, preds),3))
print("MSE: ", round(mean_squared_error(y_test, preds),3))

#Code to write R2 value and MSE to dominostats value for population in experiment manager
with open('/mnt/dominostats.json', 'w') as f:
    f.write(json.dumps({"R2": round(r2_score(y_test, preds),3),
                       "MSE": round(mean_squared_error(y_test,preds),3)}))

#Write results to dataframe for visualizations
results = pd.DataFrame({'Actuals':y_test, 'Predictions':preds})

print('Creating visualizations...')
#Add visualizations and save for inspection
fig1, ax1 = plt.subplots(figsize=(10,6))
plt.title('Sklearn Actuals vs Predictions Scatter Plot')
sns.regplot( 
    data=results,
    x = 'Actuals',
    y = 'Predictions',
    order = 3)
plt.savefig('/mnt/artifacts/sklearn_actual_v_pred_scatter.png')

fig2, ax2 = plt.subplots(figsize=(10,6))
plt.title('Sklearn Actuals vs Predictions Histogram')
plt.xlabel('Quality')
sns.histplot(results, bins=6, multiple = 'dodge', palette = 'coolwarm')
plt.savefig('/mnt/artifacts/sklearn_actual_v_pred_hist.png')

#Saving trained model to serialized pickle object 

import pickle 

# save best model
file = '/mnt/models/sklearn_gbm.pkl'
pickle.dump(gbr, open(file, 'wb'))

print('Script complete!')