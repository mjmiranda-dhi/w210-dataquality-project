import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

def generate_col_summary(dim_df):
	sum_df = pd.DataFrame.from_dict({column: len(dim_df[column].unique()) for column in dim_df.columns}, orient='index')
	sum_df.reset_index(inplace=True)
	sum_df.columns = ['FIELDS','UNQ_VALUES']
	sum_df.sort_values('UNQ_VALUES', inplace=True, ascending=False)
	sum_df.reset_index(inplace=True, drop=True)
	sum_df['NA_VALUES'] = sum_df.FIELDS.apply(lambda x: dim_df[x].isnull().sum())
	try:
		sum_df['AVG_SPACE_SPLIT'] = sum_df.FIELDS.apply(lambda x: dim_df[x].fillna('_').apply(lambda x: len(x.split(' '))).mean())
	except:
		pass
	size_desc_cols = []
	for column in dim_df.groupby(sum_df.iloc[0].FIELDS).size().describe().index.tolist():
	    new_col = "SZ_"+column
	    sum_df[new_col] = 0.0
	    size_desc_cols.append(new_col)

	sum_df[size_desc_cols] = sum_df.FIELDS.apply(lambda x: dim_df.groupby(x).size().describe())

	return sum_df

def generate_size_features(summary_df, feature_df):
	# for every field value, count number of associated records
	for i, field_name in enumerate(summary_df.FIELDS):
		# feature only meaningful for fields with more than 1 unique value
		if summary_df.ix[i,'UNQ_VALUES'] > 1:
			# normalize by median
			size_series = (feature_df.groupby(field_name).size()).fillna(0) - summary_df.ix[i,'SZ_50%']
			# only outliers below the median will be helpful
			size_series.loc[(size_series > 0),]  = 0
			# join to feature df
			size_df = size_series.to_frame(name=field_name + '_SIZE')
			feature_df = feature_df.merge(size_df, how='left',left_on=field_name, right_index=True)
	return feature_df

def generate_cumulative_size(summary_df, feature_df):
	start = 0
	for i, field_name in enumerate(summary_df.FIELDS):
		field_list = summary_df.FIELDS[start:i+1].tolist()
		if summary_df['UNQ_VALUES'][i] == feature_df.shape[0]:
			start = start + 1
		elif len(field_list) < summary_df.index.max():
			print(field_list, summary_df.FIELDS[i+1])
			size_series = feature_df.groupby(field_list)[summary_df.FIELDS[i+1]].nunique(dropna=False)
			series_med = size_series.median()
			size_series = (size_series).fillna(0) - series_med
			# print(size_series.max())
			size_series.loc[(size_series < 0),]  = 0
			# print(size_series.max())
			size_df = size_series.to_frame(name='{0}-{1}_SIZE'.format(field_list[0],field_list[-1]))
			feature_df = feature_df.merge(size_df, how='left',left_on=field_list, right_index=True)   
	return feature_df

def generate_tfidf_features(summary_df, feature_df):
	pca = PCA(n_components=2)
	for i, field_name in enumerate(summary_df.FIELDS):
	#         print(field_name)
		if i == 0:
	#         if summary_df.ix[i,'AVG_SPACE_SPLIT'] > 1:
		    tfidf = TfidfVectorizer()
		    tfidf_array = tfidf.fit_transform(feature_df[field_name]).toarray()
	#             print(np.isinf(tfidf_array).sum())
	#             tfidf_array[np.isnan(tfidf_array)] = 0
		    pca_array  = pca.fit_transform(tfidf_array)
	#             print(pca.explained_variance_ratio_)
		    feature_df = feature_df.merge(pd.DataFrame(pca_array), how='inner', left_index=True,
						  right_index=True)
	return feature_df	
