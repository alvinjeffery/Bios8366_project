import pandas as pd
import numpy as np
import seaborn as sb
import api_rxnorm
import os
import re
import config
from collections import defaultdict
from bs4 import BeautifulSoup
from sklearn import preprocessing

def load_agg_data():
    """
    Read in aggregate data
    """
    if config.print_status:
        print('Loading original, aggregated data')
    agg_source_data = pd.read_csv(config.in_file,
                                  delimiter=config.delim, 
                                  na_values=config.missing, 
                                  dtype={'VUID': object,
                                         'counts': float,
                                         'NDC': object,
                                         'DrugWithDose': object,
                                         'PharmacyOrderableItem': object,
                                         'DrugNameWithoutdose': object,
                                         'Sta3n': float, 
                                         'year_min': float, 
                                         'year_max': float,
                                         'DrugClassification': object, 
                                         'StrengthNumeric': float, 
                                         'DrugUnit': object, 
                                         'DosageForm': object,
                                         'MedicationRoute': object, 
                                         'qty_min':float,'qty_q05':float,'qty_q25':float,'qty_mean':float,
                                         'qty_sd':float, 'qty_median':float, 'qty_q75':float,'qty_q95':float,'qty_max':float,
                                         'days_supply_min':float,'days_supply_q05':float,'days_supply_q25':float, 
                                         'days_supply_mean':float,'days_supply_sd':float,'days_supply_median':float,
                                         'days_supply_q75':float,'days_supply_q95':float,'days_supply_max':float, 
                                         'refills_min':float,'refills_q05':float,'refills_q25':float,'refills_mean':float, 
                                         'refills_sd':float,'refills_median':float,'refills_q75':float,'refills_q95':float,
                                         'refills_max':float,
                                         'price_min':float,'price_q05':float,'price_q25':float,'price_mean':float,'price_sd':float,
                                         'price_median':float,'price_q75':float,'price_q95':float,'price_max':float})

    if config.print_status:
        print('Original, aggregated data loaded')
    return agg_source_data

def vuid2rxcui():
    """
    Creates a .csv file containing the results of the RxNorm API
    Allows calls to be made only once & can be merged onto data cube
    Input: aggregated source data as a dataframe
    Output: CSV file with all unique VUIDs and corresponding RxNorm CUIs
    """
    if os.path.exists('./vuid_to_rxcui.csv'):
        if config.print_status:
            print('VUIDs already created in .csv file')
        return None
    
    # load data & find unique values
    df = load_agg_data()
    vuids = df.VUID.unique()
    
    if config.print_status:
        print('Initiating API requests for VUIDs')
    # make iterable list of URLs to send to api
    urls = api_rxnorm.make_url_requests(vuids, 'vuid')
    results = api_rxnorm.async_calls(urls)
    
    # clean up & store in CSV
    vuid_to_rxcui = defaultdict(list)

    for result in results:
        # extract digits numeric results
        digits = re.findall(b'\d+', result)
        vuid = int(digits[0])
        # could be multiple rxcuis for a single vuid
        cuis = []
        for d in digits[1:]:
            cuis.append(int(d))
        vuid_to_rxcui[vuid] = cuis

    vuid_to_rxcui = pd.DataFrame.from_dict(vuid_to_rxcui, orient='index')
    vuid_to_rxcui.reset_index(inplace=True)
    assert(len(vuid_to_rxcui) == len(vuids)-1)
    # make enough column names for all extra placeholders
    cnames = ['vuid']
    for i in range(1, vuid_to_rxcui.shape[1]):
        cnames.append('rxcui'+str(i))
    vuid_to_rxcui.columns = cnames
    
    if config.print_status:
        print('API requests for VUID to RxCUI Complete.')
        print('Initiating API requests for generic & brand RxCUIs...')

    # search for generic & brand names
    rxcui_brand_generic = api_rxnorm.getBrandGeneric(vuid_to_rxcui, cui_col='rxcui1')
    
    # coerce from dictionary to dataframe to allow merge
    df = pd.DataFrame.from_dict(rxcui_brand_generic, orient='index')
    df.rename(columns={0: 'rxcui1_brand', 1: 'rxcui1_generic'}, inplace=True)
    df['rxcui1'] = df.index.astype(float)
    
    # merge & save
    vuid_to_rxcui = vuid_to_rxcui.merge(df, how='left', on='rxcui1')
    vuid_to_rxcui.to_csv('./vuid_to_rxcui.csv')
    
    if config.print_status:
        print('All API requests for VUIDs complete')

# convert VUIDs to RxCUIs - only need to execute once
#vuid2rxcui()

def ndc2rxcui():
    """
    Creates a .csv file containing the results of the RxNorm API
    Allows calls to be made only once & can be merged onto data cube
    Input: aggregated source data as a dataframe
    Output: CSV file with the unique NDCs that had a corresponding RxNorm CUI
    """
    if os.path.exists('./ndc_to_rxcui.csv'):
        if config.print_status:
            print('NDCs already created in .csv file')
        return None

    # load data & find unique values
    df = load_agg_data()
    ndcs = df.NDC.unique()
    
    if config.print_status:
        print('Initiating API requests for NDCs')
    
    # make iterable list of URLs to send to api
    urls = api_rxnorm.make_url_requests(ndcs, 'ndc')
    results = api_rxnorm.async_calls(urls)
    
    # clean up & store in CSV
    ndc_to_rxcui = defaultdict(list)

    for result in results:
        # extract digits numeric results
        try:
            # find first instance of any NDC number (assumes one is always present)
            pat = re.compile(b'\d+(-\d+)*')
            ndc = pat.search(result)[0].decode("utf-8")
        
            # find the corresponding RxNorm CUI 
            # assumes only 1 RxCUI present & that it falls after the NDC (which is always present)
            pat = re.compile(b'\d+')
            cui = int(pat.search(result, 47)[0])
        except:
            continue

        # add to dictionary
        ndc_to_rxcui[ndc] = cui

    ndc_to_rxcui = pd.DataFrame.from_dict(ndc_to_rxcui, orient='index')
    ndc_to_rxcui.reset_index(inplace=True)
    ndc_to_rxcui.columns = ['ndc', 'rxcui']
    
    if config.print_status:
        print('API requests for NDC to RxCUI Complete.')
        print('Initiating API requests for generic & brand RxCUIs...')
    
    # search for generic & brand names
    rxcui_brand_generic = api_rxnorm.getBrandGeneric(ndc_to_rxcui, cui_col='rxcui')
    
    # coerce from dictionary to dataframe to allow merge
    df = pd.DataFrame.from_dict(rxcui_brand_generic, orient='index')
    df.rename(columns={0: 'rxcui_brand', 1: 'rxcui_generic'}, inplace=True)
    df['rxcui'] = df.index.astype(float)
    
    # merge & save
    ndc_to_rxcui = ndc_to_rxcui.merge(df, how='left', on='rxcui')
    ndc_to_rxcui.to_csv('./ndc_to_rxcui.csv')
    
    if config.print_status:
        print('All API requests for NDCs complete')

# convert NDCs to RxCUIs - only need to execute once
#ndc2rxcui()

def pharmaorder2rxcui():
    """
    Creates a .csv file containing the results of the RxNorm API
    Allows calls to be made only once & can be merged onto data cube
    Input: aggregated source data as a dataframe
    Output: CSV file with the unique PharmacyOderableItems that had a corresponding RxNorm CUI
    """
    if os.path.exists('./pharmaorder_to_rxcui.csv'):
        if config.print_status:
            print('PharmacyOrderables already created in .csv file')
        return None

    # load data & find unique values
    df = load_agg_data()
    orderables = df.PharmacyOrderableItem.unique()
    
    if config.print_status:
        print('Initiating API requests for PharmacyOrderableItems')
    
    # make iterable list of URLs to send to api
    urls = api_rxnorm.make_url_requests(orderables, 'string')
    results = api_rxnorm.async_calls(urls)
    
    # clean up & store in CSV
    pharmaorder_to_rxcui = defaultdict(dict)

    for result in results:
        soup = BeautifulSoup(result, 'xml')
        cui_all = soup.find_all('rxcui')
        cui = set([])
        for c in cui_all:
            cui.add(int(c.get_text()))
        # add to dictionary
        pharmaorder = soup.find('inputTerm').get_text()
        pharmaorder_to_rxcui[pharmaorder] = cui

    pharmaorder_to_rxcui = pd.DataFrame.from_dict(pharmaorder_to_rxcui, orient='index')
    pharmaorder_to_rxcui.reset_index(inplace=True)
    # make enough column names for all extra placeholders
    cnames = ['pharmaorder']
    for i in range(1, pharmaorder_to_rxcui.shape[1]):
        cnames.append('rxcui'+str(i))
    pharmaorder_to_rxcui.columns = cnames
    
    if config.print_status:
        print('API requests for PharmacyOrderableItems to RxCUI Complete.')
        print('Initiating API requests for generic & brand RxCUIs...')

    # search for generic & brand names
    rxcui_brand_generic = api_rxnorm.getBrandGeneric(pharmaorder_to_rxcui, cui_col='rxcui1')
    
    # coerce from dictionary to dataframe to allow merge
    df = pd.DataFrame.from_dict(rxcui_brand_generic, orient='index')
    df.rename(columns={0: 'rxcui1_brand', 1: 'rxcui1_generic'}, inplace=True)
    df['rxcui1'] = df.index.astype(float)
    
    # merge & save
    pharmaorder_to_rxcui = pharmaorder_to_rxcui.merge(df, how='left', on='rxcui1')
    pharmaorder_to_rxcui.to_csv('./pharmaorder_to_rxcui.csv')
    
    if config.print_status:
        print('All API requests for PharamcyOrderableItems complete')

# convert PharmacyOrderableItems to RxCUIs - only need to execute once
#pharmaorder2rxcui()

def structured_elements2rxcui():
    """
    Creates a .csv file containing the results of the RxNorm API
    Allows calls to be made only once & can be merged onto data cube
    Input: aggregated source data as a dataframe
    Output: CSV file with the unique combination of ingredient/strength/unit/form that had a corresponding RxNorm CUI
    """
    
    if os.path.exists('./structured_elements_to_rxcui.csv'):
        if config.print_status:
            print('Structured Elements already created in .csv file')
        return None

    # load data & find unique values
    df = load_agg_data()
    structured_elements = df[['DrugNameWithoutDose', 'StrengthNumeric', 'DrugUnit', 'DosageForm']].drop_duplicates()
    search_terms = api_rxnorm.make_string(structured_elements)
    
    if config.print_status:
        print('Initiating API requests for Structured Elements')
    
    # make iterable list of URLs to send to api
    urls = api_rxnorm.make_url_requests(search_terms, 'string')
    results = api_rxnorm.async_calls(urls)

    # clean up & store in CSV
    structured_elements_to_rxcui = defaultdict(dict)

    for result in results:
        soup = BeautifulSoup(result, 'xml')
        cui_all = soup.find_all('rxcui')
        cui = set([])
        for c in cui_all:
            cui.add(int(c.get_text()))
        # add to dictionary
        unique_combo = soup.find('inputTerm').get_text()
        structured_elements_to_rxcui[unique_combo] = cui

    structured_elements_to_rxcui = pd.DataFrame.from_dict(structured_elements_to_rxcui, orient='index')
    structured_elements_to_rxcui.reset_index(inplace=True)
    # make enough column names for all extra placeholders
    cnames = ['unique_combo']
    for i in range(1, structured_elements_to_rxcui.shape[1]):
        cnames.append('rxcui'+str(i))
    structured_elements_to_rxcui.columns = cnames
    
    if config.print_status:
        print('API requests for Structured Elements to RxCUI Complete.')
        print('Initiating API requests for generic & brand RxCUIs...')

    # search for generic & brand names
    rxcui_brand_generic = api_rxnorm.getBrandGeneric(structured_elements_to_rxcui, cui_col='rxcui1')
    
    # coerce from dictionary to dataframe to allow merge
    df = pd.DataFrame.from_dict(rxcui_brand_generic, orient='index')
    df.rename(columns={0: 'rxcui1_brand', 1: 'rxcui1_generic'}, inplace=True)
    df['rxcui1'] = df.index.astype(float)
    
    # merge & save
    structured_elements_to_rxcui = structured_elements_to_rxcui.merge(df, how='left', on='rxcui1')
    structured_elements_to_rxcui.to_csv('./structured_elements_to_rxcui.csv')
    
    if config.print_status:
        print('All API requests for Structured Elements complete')

# convert Structured Elements to RxCUIs - only need to execute once
#structured_elements2rxcui()

def coerce_nulls(text):
    """
    Helper function
    Make np.NaN values blank strings. Add ' ' (i.e., actual spaces), which is different from api_rxnorm.py
    """
    # need try-except because np.isnan() won't evaluate on non-missing strings
    try:
        if np.isnan(text):
            return str('')
    except:
        return str(text) + ' '

def create_cube(size='mini'):
    """
    Use aggregated data (or mini file for testing) and combine with 
    rxcuis from API calls.
    """
    if size == 'full':
        df = load_agg_data()
    else:
        df = pd.read_pickle('./mini_df.pkl')
    
    df = df.rename(str.lower, axis='columns')
        
    # load NDCs (1 RxCUI for each NDC)
    ndc = pd.read_csv('./ndc_to_rxcui.csv', index_col='Unnamed: 0', 
                     dtype={'ndc':str, 'rxcui':float, 'rxcui_brand':float, 'rxcui_generic':float})
    ndc.rename({'rxcui': 'rxcui_ndc', 'rxcui_brand': 'rxcui_brand_ndc', 'rxcui_generic': 'rxcui_generic_ndc'}, 
                axis='columns', inplace=True)
    if config.print_status:
        print('####################################################')
        print("NDC RxCUIs loaded")
        print(ndc.head(3))
        print('####################################################')
        
    # load VUIDs (up to 7 RxCUIs per VUID)
    vuid = pd.read_csv('./vuid_to_rxcui.csv', index_col='Unnamed: 0', 
                      dtype={'vuid':str,
                             'rxcui1':float, 'rxcui2':float, 'rxcui3':float, 'rxcui4':float,
                             'rxcui5':float, 'rxcui6':float, 'rxcui7':float, 
                             'rxcui1_brand':float, 'rxcui1_generic':float})
    # keep only 1st RxCUI for now 
    vuid = vuid[['vuid', 'rxcui1', 'rxcui1_brand', 'rxcui1_generic']]
    # rename CUI for joining
    vuid.rename({'rxcui1': 'rxcui_vuid', 'rxcui1_brand': 'rxcui_brand_vuid', 'rxcui1_generic': 'rxcui_generic_vuid'}, 
                axis='columns', inplace=True)
    if config.print_status:
        print("VUID RxCUIs loaded")
        print(vuid.head(3))
        print('####################################################')

    # load PharmacyOrderableItems (up to 40 per item)
    pharma = pd.read_csv('./pharmaorder_to_rxcui.csv', index_col='Unnamed: 0', 
                         dtype={'pharmaorder':str, 'rxcui1':float, 'rxcui1_brand':float, 'rxcui1_generic':float})
    pharma = pharma[['pharmaorder', 'rxcui1', 'rxcui1_brand', 'rxcui1_generic']]
    # rename CUI for joining
    pharma.rename({'pharmaorder': 'pharmacyorderableitem', 'rxcui1': 'rxcui_pharma', 'rxcui1_brand': 'rxcui_brand_pharma', 
                    'rxcui1_generic': 'rxcui_generic_pharma'}, axis='columns', inplace=True)
    if config.print_status:
        print("PharmacyOrderableItem RxCUIs loaded")
        print(pharma.head(3))
        print('####################################################')

    # load Ingredient/Strength/Unit/Form (ISUF) (up to 26 per item)
    isuf = pd.read_csv('./structured_elements_to_rxcui.csv', index_col='Unnamed: 0', 
                       dtype={'unique_combo':str, 'rxcui1':float, 'rxcui1_brand':float, 'rxcui1_generic':float})
    isuf = isuf[['unique_combo', 'rxcui1', 'rxcui1_brand', 'rxcui1_generic']]
    # rename CUI & key
    isuf.rename({'unique_combo': 'isuf', 'rxcui1': 'rxcui_isuf', 'rxcui1_brand': 'rxcui_brand_isuf', 
                    'rxcui1_generic': 'rxcui_generic_isuf'}, axis='columns', inplace=True)
    if config.print_status:
        print("ISUF RxCUIs loaded")
        print(isuf.head(3))
        print('####################################################')
        
    # create an ISUF column for merging
    df['strengthtext'] = df['strengthnumeric'].map(api_rxnorm.coerce_numeric)
    df['isuf'] = df['drugnamewithoutdose'].map(coerce_nulls) + \
                 df['strengthtext'].map(coerce_nulls) + \
                 df['drugunit'].map(coerce_nulls) + \
                 df['dosageform'].map(coerce_nulls)

    # combine aggregated data frame with all RxNorm CUIs
    combo = df.merge(ndc, how='left', on='ndc')
    combo = combo.merge(vuid, how='left', on='vuid')
    combo = combo.merge(pharma, how='left', on='pharmacyorderableitem')
    combo = combo.merge(isuf, how='left', on='isuf')

    assert len(combo) == len(df)
    
    if config.print_status:
        print("Combo dataframe loaded")
        #print(combo.tail())
        print('####################################################')
        
    return combo
    
def prepare_features(df):
    """
    Separate numeric & categorical columns. 
    Encode categorical columns. 
    """
    # all available features
    cols = list(df.columns)
    if config.print_status:
        print('####################################################')
        print("Available columns include: ")
        print(cols)
        print('####################################################')
    
    # specify numeric columns
    numeric_cols = list(cols)
    exclude = ['vuid', 'ndc', 'drugnamewithdose', 'pharmacyorderableitem', 'drugnamewithoutdose', 'strengthtext',
              'sta3n', 'drugclassification', 'strengthnumeric', 'drugunit', 'dosageform', 'medicationroute', 'isuf', 
              'rxcui_ndc', 'rxcui_vuid', 'rxcui_pharma', 'rxcui_isuf', 
              'rxcui_brand_ndc', 'rxcui_generic_ndc', 'rxcui_brand_vuid', 'rxcui_generic_vuid', 
              'rxcui_brand_pharma', 'rxcui_generic_pharma', 'rxcui_brand_isuf', 'rxcui_generic_isuf']
    [numeric_cols.remove(e) for e in exclude]
    if config.print_status:
        print("Numeric columns include: ")
        print(numeric_cols)
        print('####################################################')
    
    # encode categorical variables
    cat_cols = ['vuid', 'ndc', 'sta3n', 'drugnamewithdose', 'pharmacyorderableitem', 
                'isuf', 'drugnamewithoutdose', 'drugunit', 'dosageform', 
                'medicationroute', 'drugclassification', 
                'rxcui_ndc', 'rxcui_vuid', 'rxcui_pharma', 'rxcui_isuf', 
                'rxcui_brand_ndc', 'rxcui_generic_ndc', 'rxcui_brand_vuid', 'rxcui_generic_vuid', 
                'rxcui_brand_pharma', 'rxcui_generic_pharma', 'rxcui_brand_isuf', 'rxcui_generic_isuf']
    cat_cols_encoded = [c + '_encoded' for c in cat_cols]

    # store encoder data for interpretation later on, if needed
    d = defaultdict(preprocessing.LabelEncoder)

    for col in cat_cols:
        # copy original into new column
        df[col + '_encoded'] = df[col]
        # replace missing values with text to ensure they are encoded as well
        df[col + '_encoded'].replace(np.NaN, 'MISSING', inplace=True)
        # coerce to string
        df[col + '_encoded'] = df[col + '_encoded'].apply(str)
        # add encoding
        df[col + '_encoded'] = d[col].fit_transform(df[col + '_encoded'])
        
    if config.print_status:
        print("Categorical columns that are encoded include: ")
        print(cat_cols_encoded)
        print('####################################################')
    
    # set standard deviations to 0 on rows where count = 1 and a mean is present
    for col in ['qty', 'days_supply', 'refills', 'price']:
        mean = col + '_mean'
        sd = col + '_sd'
        df[sd] = df.apply(lambda x: 0.0 \
                          if (np.isnan(x[sd]) and ~np.isnan(x[mean]) and x['counts']==1.0) \
                          else x[sd], axis=1)
    
    return df, numeric_cols, cat_cols_encoded