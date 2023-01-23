import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
import pickle
from sklearn import metrics

#import Data
Data = pd.read_csv('houseprices.csv')

# check if there are any Null values
Data.isnull().sum()
# drop some unnecessary columns
Data = Data.drop('date', axis=1)
Data = Data.drop('id', axis=1)
Data = Data.drop('zipcode', axis=1)
Data = Data.drop('lat', axis=1)
Data = Data.drop('long', axis=1)
Data = Data.drop('yr_renovated', axis=1)

X = Data.drop('price', axis=1).values
y = Data['price'].values
# splitting Train and Test
X_train, X_val_and_test, Y_train, Y_val_and_test = train_test_split(X, y, test_size=0.3)
X_val, X_test, Y_val, Y_test = train_test_split(X_val_and_test, Y_val_and_test, test_size=0.5)


# fit the scaler and transform the data
s_scaler = StandardScaler()
X_train = s_scaler.fit_transform(X_train.astype(np.float))
X_test = s_scaler.transform(X_test.astype(np.float))
X_val = s_scaler.transform(X_val.astype(np.float))

# create template for neural net
model = Sequential([
    Dense(19, activation='relu', input_shape=(14,)),
    Dense(19, activation='relu'),
    Dense(19, activation='relu'),
    Dense(1),
])
# add the optimizer and loss function(mean squared error)
model.compile(optimizer='Adam', loss='mse')
# fit/train the model
model.fit(x=X_train, y=Y_train,
          validation_data=(X_val, Y_val),
          batch_size=128, epochs=350)


# save the model into a seperate file
model.save(os.path.join(".", "neuralnetwork.h5"))
# save the scaler into a seperate file
pickle.dump(s_scaler, open('scaler.pkl', 'wb'))

model.summary()
# get predictions from test data
y_pred = model.predict(X_test)

# caluclate accuracy score
print('VarScore:', metrics.explained_variance_score(Y_test, y_pred))
