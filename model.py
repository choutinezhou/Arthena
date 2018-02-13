def predict(testFileName):
    
    import pickle
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import LabelEncoder
    import xgboost as xgb

    # load the model
    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))

    # identify features
    features=['artist_birth_year', 'artist_death_year', 'artist_name',
           'artist_nationality', 'auction_date', 'category', 'currency', 'edition',
           'estimate_high', 'estimate_low', 'location', 'materials',
           'measurement_depth_cm', 'measurement_height_cm', 'measurement_width_cm',
           'title', 'year_of_execution']

    #load the test file
    testFileName = input('Enter test file name:')
    testFile=pd.read_csv(testFileName+".csv", encoding="latin-1",engine='python')

    # clean the test data with prices above $0
    tempTest = testFile[pd.notnull(testFile['hammer_price'])]
    cleanTest=tempTest.loc[tempTest['hammer_price'] > 0]

    X_test=cleanTest.loc[:,features]
    y_test=cleanTest[["hammer_price"]]

    # encoding categorical variables to factors
    import warnings
    warnings.filterwarnings("ignore")

    label_encoder = dict()

    for feature in (X_test.select_dtypes(include=['object']).columns):
        print('encoding feature: {}'.format(feature))
        label_encoder[feature] = LabelEncoder()
        label_encoder[feature].fit(X_test[feature].astype(str))
        X_test.loc[:, feature]  = label_encoder[feature].transform(X_test[feature].astype(str))

    # run model
    dtest = xgb.DMatrix(X_test,feature_names=features)

    xgb_pred = loaded_model.predict(dtest)

    # transform the results from log to the hammer price 
    # df_1['log_price'] = np.log(df_1.hammer_price)
    y_pred=np.exp(xgb_pred)


    errorScore=np.sqrt(((y_pred - y_test.values) ** 2).mean())
    print("Root Mean Squared error: %.2f"
          % errorScore)
