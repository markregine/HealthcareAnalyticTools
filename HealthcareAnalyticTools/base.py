import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#from zepid.calc.utils import (risk_ci, incidence_rate_ci, risk_ratio, risk_difference, number_needed_to_treat,
#                              odds_ratio, incidence_rate_difference, incidence_rate_ratio, sensitivity, specificity)


#########################################################################################################
# Raw Data Cleaning
#########################################################################################################

def print_hello():
	print('hello')

def get_df():
	return pd.DataFrame({'first':list('mark'), 'last':list('regi')})