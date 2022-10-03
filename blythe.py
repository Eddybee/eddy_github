import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from matplotlib import pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error,r2_score
import xgboost as xgb
#Reading data
df=pd.read_csv('9-19 to 9-30 Blythe 110 Charge+Discharge Capability.csv')

#Data Preprocessing
df['Time'] = pd.to_datetime(df['Time'])
df = df.set_index('Time')
df.interpolate(method='linear', inplace=True)
df.dropna(how='any', axis=0, inplace=True)

#Building features
df['Day'] = df.index.day
df['Hour'] = df.index.hour
df['Minute'] = df.index.minute
#df['Second'] = df.index.second
df.isnull().sum()

#Building ML model
X = df.drop(['Charge Capability (MW)','Discharge (MW)'],axis=1)
y = df[['Charge Capability (MW)','Discharge (MW)']]

X_train,X_test = X.iloc[:-(350),:].values,X.iloc[-(350):,:].values
y_train, y_test =y.iloc[:-(350)].values,y.iloc[-(350):].values

print(X_test)
regressor=RandomForestRegressor()
regressor.fit(X_train,y_train)
y_pred= regressor.predict(X_test)

#Metrics
mae  = mean_absolute_error(y_test, y_pred)
mse  = mean_squared_error(y_test, y_pred)
r2   = r2_score(y_test,y_pred)
rmse = np.sqrt(mse)

y_pred= pd.DataFrame(y_pred)
#y_pred.to_csv('predictionss.csv')

#Plotting
predictions = pd.DataFrame(y_pred)
predictions.columns=['Charge','Discharge']
plt.plot(predictions, color='green')
plt.plot(y_test,color='red')
plt.title('Charge and Discharge Prediction')
plt.xlabel('Time')
plt.ylabel('Charge and Discharge Capability (MW)')
plt.legend(['Predicted Charge','Predicted Discharge','Actual Charge','Actual Discharge'], loc='upper left')
plt.show()





