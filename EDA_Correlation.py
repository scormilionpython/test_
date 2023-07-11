import pandas as pd
import numpy as np

def calculate_correlations_numeric(df, column_reference):
    correlations = []
    
    for column in df.columns:
        
        #only count if it's numeric
        if column != column_reference and df[column].dtype != 'object':
            
            #try to use 2 method correlation, only return the best

            pearson_corr = df[column].corr(df[column_reference], method='pearson')
            spearman_corr = df[column].corr(df[column_reference], method='spearman')
            
            # Select the correlation with the higher absolute value
            max_corr = max(abs(pearson_corr), abs(spearman_corr))
            # Replace NaN values with zero
            max_corr = np.nan_to_num(max_corr, nan=0)            
            
            
            correlations.append({'Column': column, 'Correlation': max_corr})
    
    return pd.DataFrame(correlations)



####### Example how to use

column_reference = 'pms_idleTime_2'
df = pd.read_csv('df_cms_pms.csv',sep=",") 

corr_result = calculate_correlations_numeric(df,column_reference)


