## Enter the directory where you would like the intermediate output files to be stored:
out_dir = '../data/'

## Enter the filepath where your raw source data file is located along with :
#in_file = '/Volumes/AlvinSD/med_mapping/rx_outpat_aggregate.txt'

## If your data file is delimited by character(s) other than a comma, please indicate the delimeter:
#delim = '\t'

write_file_source_data_cleaning = True
write_file_loinc_parsed = True
write_file_umls_cuis = True

## Enter the full filepath to your local loinc.csv file installation:
## Example: 'C:/Users/me/Documents/MyFiles/loinc.csv'
loinc_file_path = None #'YOUR_LOINC_FILE_LOCATION'

lib_loc = '/Users/AlvinMBA/anaconda/lib/R'

missing = ["*Missing*", "NULL"]

print_status = True

## Enter the integer number of CUIs to retain for each API search. Default setting will return up to 3 CUIs for each test name and each specimen type
num_cuis = 10

## For larger calls to RxNorm API, set mini-batch sizes
batch_size = int(1e4)


