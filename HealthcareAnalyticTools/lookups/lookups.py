"""
_____________________________________________________________________________________________
|                                                                                           |
|       datasets package: repository for lookup/crosswalk tables required by other modules  |
|                                                                                           |
| Part of the HealthcareAnalytics package                                                   |
|       A full applied guide to the entire package may soon be available at:                |
|       https://github.com/markregine/HealthcareAnalyticTools                               |
|                                                                                           |
|___________________________________________________________________________________________|

CONTENTS

get_
ICD9_lookup.pkl
ICD10_lookup.pkl
ICD9_to_ICD10_conversion_table.pkl
ICD10_to_ICD9_conversion_table.pkl

See http://some_website for a full guide to all the package features
"""

import pandas as pd
from pkg_resources import resource_filename
import os

def get_ICD9_lookup():
	df = pd.read_pickle(resource_filename('HealthcareAnalyticTools', 'lookups/ICD9_lookup.pkl'))
	return df

def get_ICD10_lookup():
	return pd.read_pickle(resource_filename('HealthcareAnalyticTools', "lookups/ICD10_lookup.pkl"))

def get_ICD9_to_ICD10_conversion_table():
	return pd.read_pickle(resource_filename('HealthcareAnalyticTools', "lookups/ICD9_to_ICD10_conversion_table.pkl"))

def get_ICD10_to_ICD9_conversion_table():
	return pd.read_pickle(resource_filename('HealthcareAnalyticTools', "lookups/ICD10_to_ICD9_conversion_table.pkl"))

def get_cwd():
	os.chdir(os.path.dirname(__file__))
	print(os.getcwd())