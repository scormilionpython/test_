import pandas as pd
from pandas_profiling import ProfileReport
from pandas.io.json import json_normalize


def Data_profiling(df):
    
    #USES panda profiling excluding correlation related(otherwise will be slow) 
    #Return 3 Type of information
    #1. summary_header : contains overall information about the DataFrame
    
    #2. summary_statistic_numeric : contains for each column that's considered numeric
    #show information related to "several type of quantile/percentile",Mean,Std,Varance,
    #Min,Max, Skewness,Kurtosis in essence property of it's distribution of the data
    
    #3. summary_statistic_categorical : contains for each column that's considered categorical column
    #show information about a. Distinct count item. b. Each 1 column, count of each categorical data
    #c.Each 1 column, show frequency/ratio of each categorical data
    
    
    
    profile = ProfileReport(df, minimal=True) 
    

    
    # Access the overall summary as a DataFrame
    summary_df = profile.description_set['table']
    # Assuming summary_df contains the original DataFrame with the "types" key
    flattened_df = json_normalize(summary_df)
    flattened_df = flattened_df.T
    
    #RENAME
    new_names = {'n_var': 'Number of variables', 'n': 'Number of observations',
                 'n_cells_missing':'Missing cells','types.Numeric':'Types-Numeric',
                 'types.Categorical':'Types-Categorical'}
    flattened_df.rename(index=new_names, inplace=True)
    
    #TAKE ONLY CERTAIN DATA
    index_values = ['Number of variables', 'Number of observations','Missing cells',
                    'Types-Numeric','Types-Categorical']
    flattened_df = flattened_df.loc[index_values]
    flattened_df.reset_index(inplace=True)
    
    flattened_df.rename(columns={'index': 'Item',0:'Value'}, inplace=True)
    flattened_df['Type']= 'Header'
    
    lv_col_name = ['Type','Item','Value']
    summary_header =flattened_df[lv_col_name]
    
    
    variable_summaries_df = profile.description_set['variables']
    
    summary_statistic_numeric = pd.DataFrame()
    summary_statistic_categorical = pd.DataFrame()
    for variables_name in variable_summaries_df:

        
        #variables_name = 'spindleOverride'
        #categorical :
        #variables_name = 'programNumber'  
        variables_data = variable_summaries_df[variables_name]
        
        if '5%' in variables_data :
            #NUMERIC
            variables_data_flatten = json_normalize(variables_data)
            variables_data_flatten = variables_data_flatten.T
            
            #RENAME
            new_names = {'5%': '5-th percentile', '25%': 'Q1',
                         '50%':'Median','75%':'Q3',
                         '95%':'95-th percentile','min': 'Minimum',
                         'max':'Maximum','mean':'Mean','std':'Std','variance':'Variance',
                         'skewness':'Skewness','kurtosis':'Kurtosis'}
            variables_data_flatten.rename(index=new_names, inplace=True) 
            
            #TAKE ONLY CERTAIN DATA
            index_values = ['5-th percentile','Q1',
                              'Median','Q3',
                              '95-th percentile','Minimum',
                              'Maximum','Mean','Std','Variance',
                              'Skewness','Kurtosis']
            variables_data_flatten = variables_data_flatten.loc[index_values]
            variables_data_flatten.reset_index(inplace=True)
            variables_data_flatten.rename(columns={'index': 'Item',0:'Value'}, inplace=True)
            variables_data_flatten['Column_name']= variables_name 
            variables_data_flatten['Data Type'] = 'Numeric'
            lv_col_name = ['Column_name','Data Type','Item','Value']
            variables_data_flatten = variables_data_flatten[lv_col_name]
            
            summary_statistic_numeric = summary_statistic_numeric.append(variables_data_flatten, ignore_index=True)
            
        else:

            #CATEGORICAL
            lv_Distinct = variables_data['n_distinct']
            lv_value = pd.DataFrame(variables_data['value_counts_without_nan'])
            lv_value.reset_index(inplace=True)
            lv_value.rename(columns={'index': 'Item', variables_name: 'Count'}, inplace=True)       
            lv_total_count = lv_value['Count'].sum()
            
            lv_value_detail = lv_value[0:10]
            if len(lv_value[10:]) > 0 :
                
               lv_item = 'Other values '+ "(" +str(len(lv_value[10:]))  +")"
               lv_count = lv_value[10:]['Count'].sum()
               new_row = {'Item': lv_item, 'Count': lv_count} 
               new_row = pd.DataFrame(new_row, index=[0])
               
               lv_value_detail = lv_value_detail.append(new_row, ignore_index=True)
               
            lv_value_detail['Frequency (%)']  = lv_value_detail['Count'] /  lv_total_count * 100
                
             
            lv_value_detail_stacked = pd.melt(lv_value_detail, id_vars=['Item'], value_vars=['Count', 'Frequency (%)'], var_name='Value_type', value_name='Value') 
            
            #Add distinct item
            new_row = {'Item': 'Distinct', 'Value_type': 'Distinct','Value' :lv_Distinct} 
            new_row = pd.DataFrame(new_row, index=[0])
            lv_value_detail_stacked = new_row.append(lv_value_detail_stacked, ignore_index=True)
            
            lv_value_detail_stacked['Column_name']  = variables_name
            lv_value_detail_stacked['Data Type'] = 'Categorical'
            #Rearrange the column
            lv_col_name = ['Column_name','Data Type','Item','Value_type','Value']
            lv_value_detail_stacked = lv_value_detail_stacked[lv_col_name]
            summary_statistic_categorical = summary_statistic_categorical.append(lv_value_detail_stacked, ignore_index=True)

    return summary_header, summary_statistic_numeric, summary_statistic_categorical







############ HOW TO USE THE FUNCTION

# Load your DataFrame
df = pd.read_csv('df_cms_pms.csv',sep=",") 
summary_header, summary_statistic_numeric, summary_statistic_categorical  = Data_profiling(df)


