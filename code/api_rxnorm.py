# This file contains helper functions for making calls to the RxNorm API
# No authentication or API keys are needed for accessing the API

# for information on how string matching is performed:
# https://rxnav.nlm.nih.gov/RxNormApproxMatch.html
# https://rxnav.nlm.nih.gov/RxNormNorm.html

import config
import requests
import numpy as np
import re
from bs4 import BeautifulSoup
import asyncio
from aiohttp import ClientSession
from collections import defaultdict

def coerce_numeric(text):
    """
    Helper function
    Coerce StrengthNumeric to Text, keeping NaNs intact
    """
    if np.isnan(text):
        return np.NaN
    else:
        return str(text)


def coerce_nulls(text):
    """
    Helper function
    Make np.NaN values blank strings. Add '%20' in spaces for HTML query.
    """
    # need try-except because np.isnan() won't evaluate on non-missing strings
    try:
        if np.isnan(text):
            return str('')
    except:
        return str('%20'.join(text.split())) + '%20'


def make_string(df):
    """
    Forms a searchable term from the structured data elements.
    Input: A dataframe containing DrugNameWithoutDose, StrengthNumeric, DrugUnit, & DosageForm
    Output: A list containing a Single string for all unique elements with spaces formatted for HTML
    """
    df['full'] = df['DrugNameWithoutDose'].map(coerce_nulls) + \
                 df['StrengthText'].map(coerce_nulls) + \
                 df['DrugUnit'].map(coerce_nulls) + \
                 df['DosageForm'].map(coerce_nulls)
    
    return df['full'].tolist()


def make_url_requests(unique_terms, type, max_cuis=config.num_cuis):
    """
    Makes a list of all desired URL requests for passing to async
    Input: a list of unique values with the corresponding type of API call ('ndc', 'vuid')
    Output: list of strings containing all of the URL API requests to make
    """
    urls = []
    for term in unique_terms:
        try:
            # prevent erroneous text from being added/searched by ensure at least 1 digit present
            if type in set(['ndc', 'vuid']) and len(re.findall('\d', term)) > 0:
                urls.append('https://rxnav.nlm.nih.gov/REST/rxcui.json?idtype=' + str(type).upper() + '&id=' + str(term))
            
            elif type == 'string':
                urls.append('https://rxnav.nlm.nih.gov/REST/approximateTerm?term=' + str(term) + '&maxEntries=' + str(max_cuis))

            elif type == 'cui':
                term = int(term)
                urls.append('https://rxnav.nlm.nih.gov/REST/rxcui/' + str(term) + '/related?tty=SCD+SBD')
                
            elif type == 'cui2class':
                term = int(term)
                urls.append('https://rxnav.nlm.nih.gov/REST/rxclass/class/byRxcui.xml?rxcui=' + str(term) + '&relaSource=MeSH')

        except:
            continue
    return urls


def async_calls(urls):
    """
    Helper function to take a set of URL strings & perform asynchronous (rather than sequential)
    API calls. Significantly increases speed of calls (optimistically, to the time it takes for 
    the longest request)
    Input: unique URLs for request
    Output: output (e.g., JSON, XML) from API requests
    """
    async def fetch(url, session):
        async with session.get(url) as response:
            return await response.read()

    async def run(urls):
        tasks = []
        async with ClientSession() as session:
            for url in urls:
                task = asyncio.ensure_future(fetch(url, session))
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks)
        return responses

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(urls))
    results = loop.run_until_complete(future)
    
    return results


def getRxCUI(term, type, max_cuis=config.num_cuis):
    """
    Convert search term (whether VUID, NDC, or string) to the RxCUI.
    RxCUIs are unique by ingredients, strengths, & dose forms.
    For string searches, the default is specified in the config.py file
    Input: a search term, a search type ('ndc', 'vuid', or 'string')
    Ouput: a single RxCUI integer for NDC input; a set of unique RxCUI integers for a String or VUID inputs
    """

    if type == 'ndc' or type =='vuid':
        # NDC and VUID only return 1-7 rxcui's & in JSON format
        url = 'https://rxnav.nlm.nih.gov/REST/rxcui.json?idtype=' + str(type).upper() + '&id=' + str(term)
        response = requests.get(url, headers={'Accept': 'application/json',})
        try:
            cui = int(response.json()['idGroup']['rxnormId'][0])
        except:
            cui = np.NaN

    elif type == 'string':
        # String search can return multiple rxcui's, and they come in XML format
        url = 'https://rxnav.nlm.nih.gov/REST/approximateTerm?term=' + str(term) + '&maxEntries=' + str(max_cuis)
        response = requests.get(url, headers={'Content-Type': 'application/xml',})
        soup = BeautifulSoup(response.text, 'html.parser') # 'xml')
        cui_all = soup.find_all('rxcui')
        cui = set([])
        for c in cui_all:
            cui.add(int(c.get_text()))

    else:
        return "Search term TYPE not specified.  Should be 1 of 'vuid', 'ndc', or 'string'."

    # can use RxCUI to gather ingredient, strength, & dose form
    #url = 'https://rxnav.nlm.nih.gov/REST/rxcui/' + str(cui) + '/property.json?propName=RxNorm%20Name'
    #response = requests.get(url, headers=headers)
    #return response.json()['propConceptGroup']['propConcept'][0]['propValue']

    return cui

# testing...
#print(getRxCUI('4002168', 'vuid'))
#print(getRxCUI('0115-1404-08', 'ndc'))
#print(getRxCUI('Pyridostigmine Bromide 180 MG Extended Release Oral Tablet', 'string'))


def getBrandGeneric(term_to_rxcui, cui_col):
    """
    Reverse-call rxcui's so that brand names can have an associated generic name.
    Input: dataframe of terms (e.g., VUID, NDC) mapped to rxcuis, the column containing the CUI to map
    Output: dictionary with key being original term and a list containing the brand CUI & generic CUI
    """
    rxcui_brand_generic = defaultdict(list)
    cuis = term_to_rxcui[cui_col].unique()
    urls = make_url_requests(cuis, 'cui')
    results = async_calls(urls)
    
    for result in results:
        soup = BeautifulSoup(result, 'xml')
    
        # store the searched CUI
        cui_orig = soup.rxcui.get_text()
    
        # store brand CUI (SBD) and generic CUI (SCD)
        rxcui_brand = None
        rxcui_generic = None 
        synonyms = soup.find_all('conceptGroup')
        for syn in synonyms:
            if syn.tty.get_text() == 'SBD':
                try:
                    rxcui_brand = syn.rxcui.get_text()
                except:
                    pass
            elif syn.tty.get_text() == 'SCD':
                try:
                    rxcui_generic = syn.rxcui.get_text()
                except:
                    pass

        # add to dictionary
        rxcui_brand_generic[cui_orig] = [rxcui_brand, rxcui_generic]
    
    return rxcui_brand_generic

    
def getDrugClasses(term):
    pass