dim_df = #input file into pandas df

# creates a dateframe of fields sorted by count of unique values
sum_df = pd.DataFrame.from_dict({column: len(dim_df[column].unique()) for column in dim_df.columns}, orient='index')
sum_df.reset_index(inplace=True)
sum_df.columns = ['FIELDS','UNQ_VALUES']
sum_df.sort_values('UNQ_VALUES', inplace=True, ascending=False)
sum_df.reset_index(inplace=True, drop=True)

# counts the number of null entries by field
sum_df['NA_VALUES'] = sum_df.FIELDS.apply(lambda x: dim_df[x].isnull().sum())

# iterates from 'bottom-up'
# prints field relationships that are > 95% complete but < 100%
for i in sum_df.index:
#     print(sum_df.iloc[i,0])
    for j in sum_df.index:
        if j > i:
            unique_pairs  = dim_df.groupby(sum_df.iloc[i,0])[sum_df.iloc[j,0]].nunique(dropna=False)
            perc = 1 - ((unique_pairs > 1).sum() / sum_df.iloc[i,1])
            # print('{0} - {1}: {2}'.format(sum_df.iloc[i,0],sum_df.iloc[j,0], perc))
            if (perc < 1 ) & (perc > .95):
            	print('{0} - {1}: {2}'.format(sum_df.iloc[i,0],sum_df.iloc[j,0], perc))