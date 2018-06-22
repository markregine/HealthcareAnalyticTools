import pandas as pd
import numpy as np
 
## -------------------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------------------

path_to_data = r'C:\Users\Mark\Desktop\BXA\github\HealthcareAnalyticTools\data\\'

# Another change. 


## -------------------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------------------

## ---- Pharmacy Related Lookups ----

### ---- Drug Lookups ----

#### ---- JCodes ----
def Read_JCodeRxLookUp(path=path_to_data + "JCode List.xlsx", Return='NoDups'):
    """ Returns The JCodeRxLookUp table  
    -------------------------------------  
    Return: Some JCodes are duplicated, do you want 'Dups' or 'NoDups'? Default is 'NoDups'.  
    -------------------------------------  
    """

    df = pd.read_excel(path)
    print("NumRecs: \n", df.shape)
    print("Is the JCode unique: \n" + str(df['JCode'].is_unique))
    
    ## Dtypes
    df['JCode'] = df['JCode'].str.strip()
    
    ## Rename Columns
    df.rename(columns={'JCode_Description':'JCodeRxName'}, inplace=True)
    
    ## Select columns for indication, if it needs an underscore, add one

    cols_df = pd.Series(df.columns)

    m = cols_df.str.contains('Indication', case=False)

    indication_columns_orig = cols_df[m]
    indication_columns_new = cols_df[m].str.replace(" ", "_")

    rename = dict(zip(indication_columns_orig, indication_columns_new))
    df.rename(columns=rename, inplace=True)
    
    ## Join the Indications into one Column
    def join_indication_columns(r):
        r = r.tolist()
        l = [i for i in r if i != '']
        j = ' | '.join(l)
        return j

    df['IndicationsJCode'] = df[indication_columns_new]\
                                .fillna('')\
                                .apply(lambda c: c.str.strip())\
                                .apply(join_indication_columns, axis=1)
    
    print("Key dfJCodeLookup column names:\n", ['JCode', 'IndicationsJCode'])
    
    Dups = df[df.duplicated('JCode', keep=False)].sort_values('JCode').copy()
    NoDups = df[~df.index.isin(Dups.index)].copy()
    
    if Return == 'Dups':
        return Dups
    elif Return == 'NoDups':
        return NoDups


#### ---- First Data Base ----
def Read_FDB(path=path_to_data + "FDB_Base.xlsx"):

    dfFDB = pd.read_excel(path, sheet_name='FirstDatabankMedicationBASE')
    print("NumRecs: \n", dfFDB.shape)
    print("Is the NDC unique: \n" + str(dfFDB['NDC'].is_unique))
    
    ## Dtype for NDC
    dfFDB['NDC'] = dfFDB['NDC'].astype(str).str.strip().str.zfill(11)
    
    ## Rename Drug Columns
    dfFDB.rename(columns={'BrandNM':'DrugNameFDB', 'GenericNM':'GenericNameFDB', 'AverageWholesalePriceAMT':'AvgWholesalePriceFDBAmt'}, inplace=True)

    ## Select columns for indication, if it needs an underscore, add one

    cols_dfFDB = pd.Series(dfFDB.columns)

    m = cols_dfFDB.str.contains('Indication', case=False)

    indication_columns_orig = cols_dfFDB[m]
    indication_columns_new = cols_dfFDB[m].str.replace(" ", "_")

    rename = dict(zip(indication_columns_orig, indication_columns_new))
    dfFDB.rename(columns=rename, inplace=True)
    
    ## Join the Indications into one Column
    def join_indication_columns(r):
        r = r.tolist()
        l = [i for i in r if i != '']
        j = ' | '.join(l)
        return j

    dfFDB['IndicationsFDB'] = dfFDB[indication_columns_new].fillna('').apply(join_indication_columns, axis=1)
    
    print("Key dfFDB column names:\n", ['NDC', 'DrugNameFDB', 'GenericNameFDB', 'IndicationsFDB', 'AvgWholesalePriceFDBAmt'])
    
    return dfFDB


## -------------------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------------------


## ---- ICD Specific Functions ----

def Read_ICD_9_Lookup():
	"""  
	Returns dfICD9Lookup  
	"""
	#Prep ICD 9 Lookup ---
	dfICD9Lookup = pd.read_pickle(path_to_data + "dfICD9LookUp.pkl")
	dfICD9Lookup = dfICD9Lookup.apply(lambda c: c.str.strip()).copy()
	print("Is the ICD 9 Code in dfICD9Lookup unique:\n", dfICD9Lookup.set_index('ICD9').index.is_unique )
	return dfICD9Lookup


def Read_ICD_10_Lookup():
	"""  
	Returns dfICD10Lookup  
	"""
	#Prep ICD 10 Lookup ---
	dfICD10Lookup = pd.read_pickle(path_to_data + "dfICD10LookUp.pkl")
	dfICD10Lookup = dfICD10Lookup.apply(lambda c: c.str.strip()).copy()
	print("Is the ICD 10 Code in dfICD10Lookup unique:\n", dfICD10Lookup.set_index('ICD10').index.is_unique )
	return dfICD10Lookup


def Read_ICD9_to_ICD10():
	"""  
	Returns dfICD9_to_ICD10  
	"""
	#Prep ICD9 to ICD10 ---
	dfICD9_to_ICD10 = pd.read_pickle(path_to_data + "dfICD9_to_ICD10.pkl")
	    #Dtype and strip
	dfICD9_to_ICD10 = dfICD9_to_ICD10.apply(lambda c: c.str.strip()).copy()
	    #Add Extra zeros to ICD 9 codes
	dfICD9_to_ICD10['ICD9'] = \
	    np.where(dfICD9_to_ICD10['ICD9'].str.len() == 5, dfICD9_to_ICD10['ICD9'], 
	        np.where(dfICD9_to_ICD10['ICD9'].str.len() == 4, dfICD9_to_ICD10['ICD9'] + '0', 
	            np.where(dfICD9_to_ICD10['ICD9'].str.len() == 3, dfICD9_to_ICD10['ICD9'] + '00', 'MarkRegine')))

	print("Make sure all ICD9s have a length of 5:\n", dfICD9_to_ICD10['ICD9'].str.len().value_counts())
	print("Note: ICD10's are of varing length")
	return dfICD9_to_ICD10



def Read_ICD10_to_ICD9():
	"""  
	Returns dfICD10_to_ICD9  
	"""
	#Prep ICD10 to ICD9 ----
	dfICD10_to_ICD9 = pd.read_pickle(path_to_data + "dfICD10_to_ICD9.pkl")

	    #Dtype and strip
	dfICD10_to_ICD9 = dfICD10_to_ICD9.apply(lambda c: c.str.strip()).copy()
	    #Add Extra zeros to ICD9 codes
	dfICD10_to_ICD9['ICD9'] = \
	    np.where(dfICD10_to_ICD9['ICD9'].str.len() == 5, dfICD10_to_ICD9['ICD9'], 
	        np.where(dfICD10_to_ICD9['ICD9'].str.len() == 4, dfICD10_to_ICD9['ICD9'] + '0', 
	            np.where(dfICD10_to_ICD9['ICD9'].str.len() == 3, dfICD10_to_ICD9['ICD9'] + '00', 'MarkRegine')))

	print("Make sure all ICD9s have a length of 5:\n", dfICD10_to_ICD9['ICD9'].str.len().value_counts())
	print("Note: ICD10's are of varing length")
	return dfICD10_to_ICD9



def Extract_Dx_Regardless_of_ICD_Version(df, list_of_icds_to_search_for, Version=9, DxNumber='All'):
    """ ---------------------------------  
    This will search the medical df for ICDs of interest regardless of ICD version used.  
    Required that the dfMed table has a column (col name 'ICDversion' of type str) indicating the ICDversion == '9'|'0'  
    Currently this only uses the fields Dx1, Dx2, Dx3 (see function code). Ammend function if needed.  
    Dependancies: dfICD9_to_ICD10 & dfICD10_to_ICD9
    Returns a DataFrame. 
    ----  
    df: dfMed.  
    list_of_icds_to_search_for: ex. ['25000', '49300'].  
    Version: The version of ICD codes listed above.  
    DxNumber: primary('1'), secondary('2'), tertiary('3'), and '12', ...  
    -------------------------------------  
    """
    ## Takes the medical and melts it
    t = df[['ICDversion', 'Dx1', 'Dx2', 'Dx3']].reset_index(drop=False).copy()  ## IF you change to include all pd.Series(dfMed.columns).str.startswith Dx[0-9] then you have to change below too!
    t.rename(columns={'index':'index_orig'}, inplace=True)
    tt = pd.melt(t, id_vars=['index_orig', 'ICDversion'], value_vars=['Dx1', 'Dx2', 'Dx3']).copy()
    print("this should be == to the number of dx columns and then the number of records times the number of dx cols:\n",  tt['index_orig'].value_counts().sort_values().value_counts())
    print("vc of IDCversions in the data set:\n", tt['ICDversion'].value_counts())

    if Version == 9:
        ## if searching for an ICD9, look in ICD9s 
        df9s = tt.query("ICDversion == '9'").copy()
        if DxNumber == 'All':
            index_values = df9s.loc[df9s.value.isin(list_of_icds_to_search_for), 'index_orig']  
        elif DxNumber == '1':
            index_values = df9s.loc[(df9s.value.isin(list_of_icds_to_search_for)) & (df9s['variable'] == 'Dx1'), 'index_orig'] 
        elif DxNumber == '12':
            index_values = df9s.loc[(df9s.value.isin(list_of_icds_to_search_for)) & ((df9s['variable'] == 'Dx1') | (df9s['variable'] == 'Dx2')), 'index_orig']            
        r1 = df.loc[index_values, :]

        ## if searching for an ICD9, look in ICD10s 
        # return a list of ICD10s that link to the ICD9 searching for
        ICD10s_to_find_in_medical = dfICD9_to_ICD10.loc[dfICD9_to_ICD10.ICD9.str.strip().str.contains('|'.join(list_of_icds_to_search_for)), 'ICD10']
        print(ICD10s_to_find_in_medical)
        # select recs from med where verison is 10
        df10s = tt.query("ICDversion == '0'").copy()
        if DxNumber == 'All':        
            index_values = df10s.loc[df10s.value.isin(ICD10s_to_find_in_medical), 'index_orig']
        elif DxNumber == '1':
            index_values = df10s.loc[(df10s.value.isin(ICD10s_to_find_in_medical)) & (df10s['variable'] == 'Dx1'), 'index_orig']
        elif DxNumber == '12':
            index_values = df10s.loc[(df10s.value.isin(ICD10s_to_find_in_medical)) & ((df10s['variable'] == 'Dx1') | (df10s['variable'] == 'Dx2')), 'index_orig'] 
        r2 = df.loc[index_values, :]
        r = pd.concat([r1, r2])
        return r
    
    if Version == 10:
        ## if searching for an ICD10, look in ICD10s 
        df10s = tt.query("ICDversion == '0'").copy()
        if DxNumber == 'All':
            index_values = df10s.loc[df10s.value.isin(list_of_icds_to_search_for), 'index_orig']  
        elif DxNumber == '1':
            index_values = df10s.loc[(df10s.value.isin(list_of_icds_to_search_for)) & (df10s['variable'] == 'Dx1'), 'index_orig'] 
        elif DxNumber == '12':
            index_values = df10s.loc[(df10s.value.isin(list_of_icds_to_search_for)) & ((df10s['variable'] == 'Dx1') | (df10s['variable'] == 'Dx2')), 'index_orig']            
        r1 = df.loc[index_values, :]
        
        ## if searching for an ICD10, look in ICD9s 
        # return a list of ICD9s that link to the ICD10 searching for
        ICD9s_to_find_in_medical = dfICD10_to_ICD9.loc[dfICD10_to_ICD9['ICD10'].str.strip().isin(list_of_icds_to_search_for), 'ICD9']
        print(ICD9s_to_find_in_medical)
        # select recs from med where verison is 9
        df9s = tt.query("ICDversion == '9'").copy()
        if DxNumber == 'All':        
            index_values = df9s.loc[df9s.value.isin(ICD9s_to_find_in_medical), 'index_orig']
        elif DxNumber == '1':
            index_values = df9s.loc[(df9s.value.isin(ICD9s_to_find_in_medical)) & (df9s['variable'] == 'Dx1'), 'index_orig']
        elif DxNumber == '12':
            index_values = df9s.loc[(df9s.value.isin(ICD9s_to_find_in_medical)) & ((df9s['variable'] == 'Dx1') | (df9s['variable'] == 'Dx2')), 'index_orig'] 
        r2 = df.loc[index_values, :]
        r = pd.concat([r1, r2])
        return r 