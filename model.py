import numpy as np
import pandas as pd
import joblib as joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PowerTransformer, LabelEncoder
from lightgbm import LGBMRegressor


def train():

    seed = 0

    df = pd.read_csv('listings.csv')

    train, test = train_test_split(df, test_size=0.2, random_state=seed, shuffle=True)

    # Drop unnecessary columns
    train = train[['neighbourhood_group', 'neighbourhood', 'room_type', 'minimum_nights', 'price']]
    test = test[['neighbourhood_group', 'neighbourhood', 'room_type', 'minimum_nights', 'price']]

    # Power Transform
    X_train = train.drop(['price'], axis=1)
    y_train = train['price'].values

    X_test = test.drop(['price'], axis=1)
    y_test= test['price'].values

    num_cols = X_train._get_numeric_data().columns.tolist()

    pt = PowerTransformer(method='yeo-johnson')

    X_train[num_cols]= pt.fit_transform(X_train[num_cols])
    X_test[num_cols]= pt.transform(X_test[num_cols])

    # saving transformer first
    joblib.dump(pt.fit(y_train.reshape(-1, 1)), 'powerTransform.joblib')

    y_train = pt.fit_transform(y_train.reshape(-1, 1))
    y_test = pt.transform(y_test.reshape(-1, 1))

    # Label Encoder
    le = LabelEncoder()

    cat_cols_train = X_train.select_dtypes(include=['string', 'object']).columns.tolist()

    cat_cols_test = X_test.select_dtypes(include=['string', 'object']).columns.tolist()

    for col in cat_cols_train:

        joblib.dump(le.fit(X_train[col].astype('string')), 'le_{}.joblib'.format(col))

        X_train[col] = le.fit_transform(X_train[col].astype('string'))


    # I fit the test dataset because it contains previously unseen labels in the train dataset
    for col in cat_cols_test:
        X_test[col] = le.fit_transform(X_test[col].astype('string'))

    # Outliers
    X_train['price'] = y_train.ravel().tolist()

    X_train.drop(X_train[(X_train['price']<-4)].index, inplace=True)

    y_train = X_train['price']

    X_train.drop('price', axis=1, inplace=True)

    # Model
    X_train = X_train.values

    y_train = y_train.values

    model = LGBMRegressor(max_depth=10, num_leaves=20, random_state=0)

    model.fit(X_train,y_train)

    joblib.dump(model, "model.joblib")

def predict(param1, param2, param3, param4):

    le_neighbourhood = joblib.load('le_neighbourhood.joblib')
    le_neighbourhood_group = joblib.load('le_neighbourhood_group.joblib')
    le_room_type = joblib.load('le_room_type.joblib')


    input_data = {'neighbourhood_group': [param1], 'neighbourhood': [param2],
             'room_type': [param3], 'minimum_nights': [param4]}

    input_data_df = pd.DataFrame(data=input_data)

    input_data_le = {'param2': le_neighbourhood.transform(input_data_df ['neighbourhood'])[0],
                     'param1': le_neighbourhood_group.transform(input_data_df ['neighbourhood_group'])[0],
                     'param3': le_room_type.transform(input_data_df ['room_type'])[0]}


    model = joblib.load("model.joblib")


    predictions = model.predict([[input_data_le['param1'],input_data_le['param2'],input_data_le['param3'],param4]])

    pt = joblib.load('powerTransform.joblib')

    predictions = pt.inverse_transform(predictions.reshape(-1,1))

    predictions = np.around(predictions,2).ravel().tolist()[0]

    return predictions
