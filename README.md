# Bios8366 Final Project: Data Cleaning, Pre-Processing, & Analysis Pipeline  

**Group Members:** Alvin Jeffery, Kim Kondratieff, Patrick Wu  

Student name in parentheses indicates the student who took primary responsibility for the notebook.  

## 1. Create Cohort (Kim)  
> We removed pediatric and psychiatric patients because they are not eligible for the CMS readmission penalty.  

Code File: `base_table_creation.ipynb`  

| Input                                 | Output(s)                 |
| ---                                   | ---                       |
| `FONNESBECK_ADT_20151202.csv`         | `adt_cms_final.pkl`       |
| `FONNESBECK_phenotype_20151202.csv`   |                           |
| `FONNESBECK_CPT_20151202.csv`         |                           |  

## 2. Clean Phenotype, Medications, ICD, and CPT (Alvin)  
> Major cleaning steps include mapping medications to medication classes with RxNorm API calls through helper functions and counted for each day.  Converting strings to classes reduced the total number of potential features and allowed similar to medications to be collapsed into the same group.  ICD and CPT codes were rolled up to chapters (categories) and counted for each day.  

Code File: `cpt_icd_meds_phenotype_preprocessing.ipynb`  

| Input                                   | Output(s)                         |
| ---                                     | ---                               |
| `FONNESBECK_phenotype_20151202.csv`     | `phenotype.pkl`                   |
| `FONNESBECK_ICD9_20151202.csv`          | `icd_wide.pkl`                    |
| `FONNESBECK_CPT_20151202.csv`           | `cpt_wide.pkl`                    |
| `FONNESBECK_MED_20151202.csv`           | `med_classes_final_ruids.pkl`     |  


## 3. Clean Labs, BMI, and BPs (Patrick)  
HTML files of the notebooks below are found in `reports` folder.  

> `adt_cms_final.pkl` = output from `base_table_creation.ipynb` that contains cohort information. `labs_cleaned.csv` = has columns ['ruid','lab_name','lab_date','lab_value','visit_id','hospital_day'] for 19 top labs by total count. I identified outliers in the original labs contained in `FONNESBECK_LAB_20151202.csv` by looking at the 1%, 99% of values, distribution, and looking at normal values in adults. Outliers were converted to 'NaN' for imputation in `impute.ipynb`.    

Code File: `labs_bmi_bp_data_preprocessing.ipynb`   
  
| Input                                         | Output(s)                 |
| ---                                           | ---                       |
| `FONNESBECK_LAB_20151202.csv`                 | `labs.csv`                |
| `adt_cms_final.pkl`                           |                           |

> From the cleaned 19 labs from `labs_bmi_bp_data_preprocessing.ipynb`, this notebook extracts 6 summary stats (5th percentile, 95th percentile, median, first measurement at visit, last measurement at visit, and standard deviation) that were used as predictor variables in the statistical models. This notebook also preprocesses BMI and pregnancy_indicator values before extracting last entries for each measurement at visit. Last, this notebook preprocesses blood pressure values and extracts the same 6 summary stats as was done for the labs. Note that we decided not to use the EGFR data, as it is the value is calculated with measured Creatinine levels and is thus highly correlated. 

Code File: `labs_bmi_bp_data_preprocessing_2.ipynb`

| Input                                         | Output(s)                 |
| ---                                           | ---                       |
| `labs_cleaned.csv`                            | `labs.csv`                |
| `FONNESBECK_BMI_20151202.csv`                 |                           |
| `adt_cms_final.pkl`                           |                           |
| `FONNESBECK_BP_20151202.csv`                  |                           |
| `labs.csv`                                    |                           |    

## 4. Merge All Predictors onto Cohort (Alvin)  
> Thie notebook combines the work from (1), (2), and (3) above into a single flat-file for descriptive statistics, imputation, and analysis.  

Code File: `merging.ipynb`  
  
| Input                             | Output(s)                 |
| ---                               | ---                       |
| `adt_cms_final.pkl`               | `merged.csv`              |
| `phenotype.pkl`                   |                           |
| `icd_wide.pkl`                    |                           |
| `cpt_wide.pkl`                    |                           |
| `med_classes_final_ruids.pkl`     |                           |
| `labs.csv`                        |                           |  

## 5. Descriptive Statistics (Patrick)  
> HTML of notebook is found in `reports` folder.  

> This notebook takes non-imputed values from `merged.csv`, and extracts descriptive statistics (min, max, quartiles, median, mean, etc.) for predictor variables used in the statistical models. 

Code File: `nonimputed_data_summary_statistics.ipynb`

| Input                             | Output(s)                 |
| ---                               | ---                       |
| `merged.csv`                      | Report Only (see notebook)|  


## 6. Imputation (Alvin)  
> This R-based notebook uses `Hmisc::transcan()` to provide a single imputation of the data.  There is also a review of potentially redundant variables that could be exluded in the regression analysis.  

Code File: `impute.ipynb`

| Input                             | Output(s)                 |
| ---                               | ---                       |
| `merged.csv`                      | `train_imputed.csv`       |
|                                   | `valid_imputed.csv`       |  
|                                   | `test_imputed.csv`        |  

## 7. Analysis-Bayesian Regression (Kim)  
> This notebook explores several PyMC3 logistic regression model using the built-in GLM function, examining various variable subsets and their utility in predicting 30-day readmissions. Variable selection is performed using domain knowledge and the redundancy analysis carried out in the imputation notebook.

Code File: `bayesian_regression_model.ipynb`  

| Input                           | Output(s)                 |
| ---                             | ---                       |
| `train_imputed.csv`             | Report Only               |
| `valid_imputed.csv`             |                           |
| `test_imputed.csv`              |                           |  


## 8. Analysis-Machine Learning (Alvin)  
> Using hyperopt and a cross-validated manual grid search to explore the ideal classification algorithm(s) and best hyperparameters, this notebook identifies potential machine learning approaches for predicting 30-day readmissions.  

Code File: `machine_learning.ipynb`  

| Input                           | Output(s)                 |
| ---                             | ---                       |
| `train_imputed.csv`             | Report Only               |
| `valid_imputed.csv`             |                           |
| `test_imputed.csv`              |                           |  


