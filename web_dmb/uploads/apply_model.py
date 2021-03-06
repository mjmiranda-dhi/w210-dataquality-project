from . import model_functions
import pandas as pd
from sklearn.ensemble import IsolationForest
import os

def run(input_file_path):
    print("INPUT FILE PATH", input_file_path, os.path.exists(input_file_path))

    # we may want to pass read_csv settings to user
    # get delimiter? escape character?
    input_df = pd.read_csv(input_file_path)
    print('Read file of shape: {0}'.format(input_df.shape))


def run_full(input_file_path):
    #input_file_path = '' #path to users file

    # we may want to pass read_csv settings to user
    # get delimiter? escape character?
    input_df = pd.read_csv(input_file_path, quotechar="\"")
    print('Read file of shape: {0}'.format(input_df.shape))

    # summary_df contains one record per column in input
    # SZ_ values summarize number of records associated w/ each unique value
    summary_df = model_functions.generate_col_summary(input_df)

    # copy the input dataframe and append columns we will use as features
    # more feature-generating functions could be added here
    feature_df = input_df.copy(deep=True)
    feature_df = model_functions.generate_size_features(summary_df, feature_df)
    feature_df = model_functions.generate_cumulative_size(summary_df, feature_df)

    # isolation forest model applied
    get_est_contamination = .025 #get from user input
    n_estimators = 100 #adjust based on input size. more is better

    iForest = IsolationForest(n_estimators=n_estimators, \
                          bootstrap=True, contamination=get_est_contamination)

    # training variables are any columns to the right of the original input
    train_variables = feature_df.iloc[:,input_df.shape[1]:].fillna(0)
    iForest.fit(train_variables)
    # write the model prediction and score to columns in the dataframe
    feature_df['i_PREDICT'] = iForest.predict(train_variables)
    feature_df['i_DECS'] = iForest.decision_function(train_variables)

    # we may want to remove the features we generated before dropping to csv
    #to_file_path = '../tmp/output.csv'
    to_file_path = 'uploads/static/img/output.csv'
    feature_df.to_csv(to_file_path)