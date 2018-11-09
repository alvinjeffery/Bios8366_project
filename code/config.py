## Enter the directory where you would like the intermediate output files to be stored:
out_dir = '/Volumes/AlvinSD/med_mapping/temp_files/'

## Enter the filepath where your raw source data file is located along with :
in_file = '/Volumes/AlvinSD/med_mapping/rx_outpat_aggregate.txt'

## If your data file is delimited by character(s) other than a comma, please indicate the delimeter:
delim = '\t'

write_file_source_data_cleaning = True
write_file_loinc_parsed = True
write_file_umls_cuis = True

## Enter the full filepath to your local loinc.csv file installation:
## Example: 'C:/Users/me/Documents/MyFiles/loinc.csv'
loinc_file_path = None #'YOUR_LOINC_FILE_LOCATION'

lib_loc = '/Users/AlvinMBA/anaconda/lib/R'

## Enter the name of the column in your data source that contains the TEST NAME (i.e. Creatinine):
test_col = 'DrugNameWithoutDose'
## Enter the name of the column in your data source that contains the SPECIMEN TYPE (i.e. urine):
spec_col = 'MedicationRoute'
## Enter the name of the column in your data source that contains the UNITS:
units = 'DrugUnit'
## Enter the name of the column in your data source that contains the LOINC CODE:
loinc_col = 'VUID'
min_col = 'price_min'
max_col = 'price_max'
mean_col = 'price_mean'
perc_5 = 'price_q05'
perc_25 = 'price_q25'
median_col = 'price_median'
perc_75 = 'price_q75'
perc_95 = 'price_q95'
count = 'counts'
site = 'Sta3n'

missing = ["*Missing*", "NULL"]

## Please enter a numeric rejection threshold (example: 4.0) for eliminating high frequency tokens from source data test names. 
## Default will not remove any tokens during source data pre-processing.
rejection_threshold = None

print_status = False
## Enter the integer number of CUIs to retain for each API search. Default setting will return up to 3 CUIs for each test name and each specimen type
num_cuis = 10
## Enter the integer number for minimum number of sites at which a LOINC key must be used to be retained in the labeled dataset (Default is 1, meaning that LOINC keys occurring at only 1 site are filtered out and combined with the unlabeled data for reclassification)
min_sites_per_loinc_key = 1
## Enter the minimum number of cumulative test instances per LOINC group to be retained in the labeled training data (Default is 9)
min_tests_per_loinc_group = 9
## Enter the minimum number of data instances allowed per LOINC key group in the labeled training data (Default is 2)
min_row_count_per_loinc_group = 2

## Default program setting is to fit Random Forest and One-Versus-Rest models during cross-validation, to obtain predicted labels from each model, and to provide model performance metrics obtained during cross-validation. If you do NOT want to perform CV, change the code below to "run_cv = 'N'"
run_cv = 'Y'
## Enter the integer number of cross-validation folds (default is 5-fold)
n_splits = 5
## Enter the integer number of trials for hyperparameter tuning (default is 200)
tuning_evals = 200

