import model_functions
import pandas as pd
from sklearn.ensemble import IsolationForest

input_file_path = 'master_products_5per_error.csv' #path to users file

# we may want to pass read_csv settings to user
# get delimiter? escape character?
raw_df = pd.read_csv(input_file_path)
print('Read file of shape: {0}'.format(raw_df.shape))

# only using the hierarchy columns for evaluation
hier_cols = [col for col in raw_df.columns if 'train_level' in col]

input_df = raw_df[hier_cols].copy(deep=True)
                                  
# summary_df contains one record per column in input
# SZ_ values summarize number of records associated w/ each unique value
summary_df = model_functions.generate_col_summary(input_df)

# copy the input dataframe and append columns we will use as features
# more feature-generating functions could be added here
feature_df = input_df.copy(deep=True)
feature_df = model_functions.generate_tfidf_features(summary_df, feature_df)
feature_df = model_functions.generate_size_features(summary_df, feature_df)
feature_df = model_functions.generate_cumulative_size(summary_df, feature_df)

# isolation forest model applied
get_est_contamination = .05 #get from user input
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
to_file_path = 'output.csv'
feature_df.to_csv(to_file_path, index=False)

blend_df = raw_df.merge(feature_df, how='inner', left_index=True, right_index=True)
blend_df['train_result'] = blend_df.train_status == 'Correct Record'
                                  
prec = blend_df[(blend_df.train_result == False) & (blend_df.i_PREDICT == -1)].shape[0] / blend_df[(blend_df.i_PREDICT == -1)].shape[0]
print('Precision: {0}%'.format(round(100*prec)))

recall = blend_df[(blend_df.train_result == False) & (blend_df.i_PREDICT == -1)].shape[0] / blend_df[(blend_df.train_result == False)].shape[0]
print('Recall {0}%'.format(round(100*recall)))

f_score = 2 * ((prec * recall) / (prec + recall))
print('F-Score: {0}'.format(round(100*f_score)))                                  
